import os
import importlib
import re
import shutil
import sys
import siliconcompiler

####################################################################
# Make Docs
####################################################################

def make_docs():
    '''
    OpenROAD is an automated physical design platform for
    integreated circuit design with a complete set of features
    needed to translate a synthesized netlist to a tapeout ready
    GDSII.

    Documentation:https://github.com/The-OpenROAD-Project/OpenROAD

    Sources: https://github.com/The-OpenROAD-Project/OpenROAD

    Installation: https://github.com/The-OpenROAD-Project/OpenROAD-flow-scripts

    '''

    chip = siliconcompiler.Chip()
    chip.set('arg','step','<step>')
    chip.set('arg','index','<index>')
    setup_tool(chip)

    return chip

################################
# Setup Tool (pre executable)
################################

def setup_tool(chip, mode='batch'):

    # default tool settings, note, not additive!

    tool = 'openroad'
    refdir = 'tools/'+tool
    step = chip.get('arg','step')
    index = chip.get('arg','index')

    if mode == 'show':
        clobber = True
        script = '/sc_display.tcl'
        option = "-no_init -gui"
    else:
        clobber = False
        script = '/sc_apr.tcl'
        option = "-no_init"

    # exit automatically in batch mode and not bkpt
    if (mode=='batch') & (step not in chip.get('bkpt')):
        option += " -exit"

    chip.set('eda', tool, step, index, 'exe', tool, clobber=clobber)
    chip.set('eda', tool, step, index, 'vswitch', '-version', clobber=clobber)
    chip.set('eda', tool, step, index, 'version', '0', clobber=clobber)
    chip.set('eda', tool, step, index, 'threads', os.cpu_count(), clobber=clobber)
    chip.set('eda', tool, step, index, 'option', 'cmdline', option, clobber=clobber)
    chip.set('eda', tool, step, index, 'refdir', refdir, clobber=clobber)
    chip.set('eda', tool, step, index, 'script', refdir + script, clobber=clobber)

    # defining default dictionary
    default_options = {
        'place_density': [],
        'pad_global_place': [],
        'pad_detail_place': [],
        'macro_place_halo': [],
        'macro_place_channel': []
    }

    # Setting up technologies with default values
    # NOTE: no reasonable defaults, for halo and channel.
    # TODO: Could possibly scale with node number for default, but safer to error out?
    # perhaps we should use node as comp instead?
    if chip.get('pdk','process'):
        process = chip.get('pdk','process')
        if process == 'freepdk45':
            default_options = {
                'place_density': ['0.3'],
                'pad_global_place': ['2'],
                'pad_detail_place': ['1'],
                'macro_place_halo': ['22.4', '15.12'],
                'macro_place_channel': ['18.8', '19.95']
            }
        elif process == 'asap7':
           default_options = {
                'place_density': ['0.77'],
                'pad_global_place': ['2'],
                'pad_detail_place': ['1'],
                'macro_place_halo': ['22.4', '15.12'],
                'macro_place_channel': ['18.8', '19.95']
            }
        elif process == 'skywater130':
           default_options = {
                'place_density': ['0.6'],
                'pad_global_place': ['4'],
                'pad_detail_place': ['2'],
                'macro_place_halo': ['1', '1'],
                'macro_place_channel': ['80', '80']
            }
        else:
            chip.error = 1
            chip.logger.error(f'Process {process} not supported with OpenROAD.')
    else:
        default_options = {
            'place_density': ['1'],
            'pad_global_place': ['<space>'],
            'pad_detail_place': ['<space>'],
            'macro_place_halo': ['<xspace>', '<yspace>'],
            'macro_place_channel': ['<xspace>', '<yspace>']
        }

    for option in default_options:
        if option in chip.getkeys('eda', tool, step, index, 'option'):
            chip.logger.info('User provided option %s OpenROAD flow detected.', option)
        elif not default_options[option]:
            chip.error = 1
            chip.logger.error('Missing option %s for OpenROAD.', option)
        else:
            chip.set('eda', tool, step, index, 'option', option, default_options[option], clobber=clobber)

################################
# Version Check
################################

def check_version(chip, version):
    ''' Tool specific version checking
    '''
    step = chip.get('arg','step')
    index = chip.get('arg','index')
    required = chip.get('eda', 'openroad', step, index, 'version')
    #insert code for parsing the funtion based on some tool specific
    #semantics.
    #syntax for version is string, >=string

    return 0


################################
# Post_process (post executable)
################################

def post_process(chip):
     ''' Tool specific function to run after step execution
     '''

     #Check log file for errors and statistics
     tool = 'openroad'
     step = chip.get('arg','step')
     index = chip.get('arg','index')
     design = chip.get('design')

     errors = 0
     warnings = 0
     metric = None

     with open(step + ".log") as f:
          for line in f:
               metricmatch = re.search(r'^SC_METRIC:\s+(\w+)', line)
               errmatch = re.match(r'^Error:', line)
               warnmatch = re.match(r'^\[WARNING', line)
               area = re.search(r'^Design area (\d+)', line)
               tns = re.search(r'^tns (.*)',line)
               wns = re.search(r'^tns (.*)',line)
               vias = re.search(r'^Total number of vias = (.*).',line)
               wirelength = re.search(r'^Total wire length = (.*) um',line)
               power = re.search(r'^Total(.*)',line)
               if metricmatch:
                   metric = metricmatch.group(1)
               elif errmatch:
                   errors = errors + 1
               elif warnmatch:
                   warnings = warnings +1
               elif area:
                   chip.set('metric', step, index, 'cellarea', 'real', round(float(area.group(1)),2), clobber=True)
               elif tns:
                   chip.set('metric', step, index, 'setuptns', 'real', round(float(tns.group(1)),2), clobber=True)
               elif wns:
                   chip.set('metric', step, index, 'setupwns', 'real', round(float(wns.group(1)),2), clobber=True)
               elif wirelength:
                   chip.set('metric', step, index, 'wirelength', 'real', round(float(wirelength.group(1)),2), clobber=True)
               elif vias:
                   chip.set('metric', step, index, 'vias', 'real', int(vias.group(1)), clobber=True)
               elif metric == "power":
                   if power:
                       powerlist = power.group(1).split()
                       leakage = powerlist[2]
                       total = powerlist[3]
                       chip.set('metric', step, index, 'peakpower', 'real',  float(total), clobber=True)
                       chip.set('metric', step, index, 'standbypower', 'real', float(leakage), clobber=True)

     #Setting Warnings and Errors
     chip.set('metric', step, index, 'errors', 'real',  errors , clobber=True)
     chip.set('metric', step, index, 'warnings', 'real', warnings, clobber=True)

     #Temporary superhack!rm
     #Getting cell count and net number from DEF
     if errors == 0:
          with open("outputs/" + design + ".def") as f:
               for line in f:
                    cells = re.search(r'^COMPONENTS (\d+)', line)
                    nets = re.search(r'^NETS (\d+)',line)
                    pins = re.search(r'^PINS (\d+)',line)
                    if cells:
                         chip.set('metric', step, index, 'cells', 'real', int(cells.group(1)), clobber=True)
                    elif nets:
                         chip.set('metric', step, index, 'nets', 'real', int(nets.group(1)), clobber=True)
                    elif pins:
                         chip.set('metric', step, index, 'pins', 'real', int(pins.group(1)), clobber=True)

     if step == 'sta':
          # Copy along GDS for verification steps that rely on it
          design = chip.get('design')
          shutil.copy(f'inputs/{design}.gds', f'outputs/{design}.gds')

     #Return 0 if successful
     return 0



##################################################
if __name__ == "__main__":

    chip = make_docs()
    chip.writecfg("openroad.json")
