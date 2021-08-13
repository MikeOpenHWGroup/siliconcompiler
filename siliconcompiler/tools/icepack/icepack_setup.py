import os
import importlib
import re
import sys
import siliconcompiler
from siliconcompiler.floorplan import *
from siliconcompiler.schema import schema_path

################################
# Setup Tool (pre executable)
################################

def setup_tool(chip, step):
    ''' Sets up default settings on a per step basis
    '''
    tool = 'icepack'
    chip.set('eda', tool, step, 'vendor', tool)
    chip.set('eda', tool, step, 'exe', tool)
    chip.add('eda', tool, step, 'format', 'cmdline')
    chip.set('eda', tool, step, 'threads', 4)
    chip.set('eda', tool, step, 'copy', 'false')

    #Get default opptions from setup
    topmodule = chip.get('design')

    options = []
    options.append("inputs/" + topmodule + ".asc")
    options.append("outputs/" + topmodule + ".bit")
    chip.add('eda', tool, step, 'option', 'cmdline', options)

################################
# Post_process (post executable)
################################
def post_process(chip, step):
    ''' Tool specific function to run after step execution
    '''
    return 0
