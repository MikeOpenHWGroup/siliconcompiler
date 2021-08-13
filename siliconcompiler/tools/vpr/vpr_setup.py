
import os

import siliconcompiler
from siliconcompiler.floorplan import *
from siliconcompiler.schema import schema_path

################################
# Setup Tool (pre executable)
################################
def setup_tool(chip, step):

     tool = 'vpr'
     refdir = 'eda/vpr/'

     chip.set('eda', tool, step, 'threads', '4')
     chip.set('eda', tool, step, 'copy', 'false')
     chip.set('eda', tool, step, 'format', 'cmdline')
     chip.set('eda', tool, step, 'vendor', tool)
     chip.set('eda', tool, step, 'exe', tool)

     #TODO: this flow is broken!
     if step in ("floorplan"):
          chip.set('eda', tool, step, 'exe', tool)
     else:
          #ignore stages withh echo
          chip.set('eda', tool, step, 'exe', 'echo')

     arch = chip.get('fpga','arch')
     topmodule = chip.get('design')
     blif = "inputs/" + topmodule + ".blif"
     options = [arch, blif]

     chip.set('eda', tool, step, 'option', 'cmdline', options)

################################
# Post_process (post executable)
################################

def post_process(chip, step ):
    ''' Tool specific function to run after step execution
    '''

    #TODO: return error code
    return 0
