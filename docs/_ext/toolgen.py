from docutils import nodes
from sphinx.util.nodes import nested_parse_with_titles
from docutils.statemachine import ViewList
from sphinx.util.docutils import SphinxDirective
import docutils

import importlib
import pkgutil
import os
import sys

import siliconcompiler

# docutils helpers
def build_table(items):
    table = nodes.table()

    group = nodes.tgroup(cols=len(items[0]))
    table += group
    # not sure how colwidth affects things - columns seem to adjust to contents
    group += nodes.colspec(colwidth=50)
    group += nodes.colspec(colwidth=100)

    body = nodes.tbody()
    group += body

    for row in items:
        row_node = nodes.row()
        body += row_node
        for col in row:
            entry = nodes.entry()
            row_node += entry
            entry += col

    return table

def build_section(text, key):
    sec = nodes.section(ids=[nodes.make_id(key)])
    sec += nodes.title(text=text)
    return sec

def para(text):
    return nodes.paragraph(text=text)

def code(text):
    return nodes.literal(text=text)

def strong(text):
    p = nodes.paragraph()
    p += nodes.strong(text=text)
    return p

def is_leaf(schema):
    if 'defvalue' in schema:
        return True
    elif len(schema.keys()) == 1 and 'default' in schema:
        return is_leaf(schema['default'])
    return False

def flatten(cfg, prefix=()):
    flat_cfg = {}

    for key, val in cfg.items():
        if key == 'default': continue
        if 'defvalue' in val:
            flat_cfg[prefix + (key,)] = val
        else:
            flat_cfg.update(flatten(val, prefix + (key,)))

    return flat_cfg

# Main Sphinx plugin
class ToolGen(SphinxDirective):

    def process_tool(self, toolname, module):
        test_tool = getattr(module, f'test_{toolname}')

        cfg = test_tool()

        s = build_section(toolname, toolname)

        packdir = f'siliconcompiler.tools.{toolname}'
        modulename = f'.{toolname}_setup'
        toolmodule = importlib.import_module(modulename, package=packdir)
        setup_tool = getattr(toolmodule, 'setup_tool')

        docstr = setup_tool.__doc__
        if docstr:
            self.parse_rst(docstr, s)

        chip = siliconcompiler.Chip()
        flat_cfg = flatten(chip.prune(cfg))

        table = [[strong('Keypath'), strong('Value')]]
        for keys, val in flat_cfg.items():
            keypath = f'eda, {toolname}, ' + ', '.join(keys)
            if 'value' in val:
                table.append([code(keypath), code(val['value'])])
            else:
                table.append([code(keypath), code(val['defvalue'])])

        s += build_table(table)

        return s

    def run(self):

        sections = []

        sc_root = os.path.abspath(f'{__file__}/../../../')
        tools_dir = f'{sc_root}/siliconcompiler/tools'
        self.env.note_dependency(f'{sc_root}/tests/tools/test_setup.py')

        packdir = f'tests.tools'
        modulename = f'.test_setup'
        module = importlib.import_module(modulename, package=packdir)
        for attr in dir(module):
            if attr.startswith('test_'):
                toolname = attr[len('test_'):]
                self.env.note_dependency(f'{tools_dir}/{toolname}/{toolname}_setup.py')
                sections.append(self.process_tool(toolname, module))

        return sections

    def parse_rst(self, content, s):
        rst = ViewList()
        # use fake filename 'inline' for error # reporting
        for i, line in enumerate(content.split('\n')):
            # lstrip() necessary to prevent weird indentation (since this is
            # parsing docstrings which are intendented)
            rst.append(line.lstrip(), 'inline', i)
        nested_parse_with_titles(self.state, rst, s)

def setup(app):
    app.add_directive('toolgen', ToolGen)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
