
import os
import sys
import re
import siliconcompiler

####################################################
# PDK Setup
####################################################

def setup_platform(chip):

    foundry = 'skywater'
    process = 'skywater130'

    rev = 'v0_0_2'

    stackup = '5M1LI'
    # TODO: eventualy support hs libtype as well
    libtype = 'hd'

    node = 130

    # TODO: dummy numbers, only matter for cost estimation
    wafersize = 300
    hscribe = 0.1
    vscribe = 0.1
    edgemargin = 2

    pdkdir = '/'.join(['third_party/foundry',
                       foundry,
                       process,
                       'pdk',
                       rev])


    #if you are calling this file, you are in asic mode
    chip.set('mode','asic')

    # process name
    chip.set('pdk','foundry', foundry)
    chip.set('pdk','process', process)
    chip.set('pdk','node', node)
    chip.set('pdk','rev', rev)
    chip.set('pdk','stackup', stackup)
    chip.set('pdk','wafersize', wafersize)
    chip.set('pdk','edgemargin', edgemargin)
    chip.set('pdk','hscribe', hscribe)
    chip.set('pdk','vscribe', vscribe)

    # Values chosen based on
    # https://github.com/The-OpenROAD-Project/OpenROAD-flow-scripts/blob/59ad47a1325239b578bf1c2b3cf6617e44d05d47/flow/platforms/sky130hd/tapcell.tcl
    chip.set('pdk','tapmax', 14)
    chip.set('pdk','tapoffset', 2)

    # APR tech file
    chip.set('pdk','aprtech',stackup, libtype, 'lef',
             pdkdir+'/apr/sky130_fd_sc_hd.tlef')

    # Routing Grid Definitions

    # TODO: what should the SC-internal name of the LI layer be?
    chip.set('pdk','grid', stackup, 'm6', 'name', 'li1')
    chip.set('pdk','grid', stackup, 'm6', 'xoffset', 0.23)
    chip.set('pdk','grid', stackup, 'm6', 'xpitch',  0.46)
    chip.set('pdk','grid', stackup, 'm6', 'yoffset', 0.17)
    chip.set('pdk','grid', stackup, 'm6', 'ypitch',  0.34)
    chip.set('pdk','grid', stackup, 'm6', 'adj', 1.0)

    chip.set('pdk','grid', stackup, 'm1', 'name', 'met1')
    chip.set('pdk','grid', stackup, 'm1', 'xoffset', 0.17)
    chip.set('pdk','grid', stackup, 'm1', 'xpitch',  0.34)
    chip.set('pdk','grid', stackup, 'm1', 'yoffset', 0.17)
    chip.set('pdk','grid', stackup, 'm1', 'ypitch',  0.34)
    chip.set('pdk','grid', stackup, 'm1', 'adj', 0.5)

    chip.set('pdk','grid', stackup, 'm2', 'name', 'met2')
    chip.set('pdk','grid', stackup, 'm2', 'xoffset', 0.23)
    chip.set('pdk','grid', stackup, 'm2', 'xpitch',  0.46)
    chip.set('pdk','grid', stackup, 'm2', 'yoffset', 0.23)
    chip.set('pdk','grid', stackup, 'm2', 'ypitch',  0.46)
    chip.set('pdk','grid', stackup, 'm2', 'adj', 0.5)

    chip.set('pdk','grid', stackup, 'm3', 'name', 'met3')
    chip.set('pdk','grid', stackup, 'm3', 'xoffset', 0.34)
    chip.set('pdk','grid', stackup, 'm3', 'xpitch',  0.68)
    chip.set('pdk','grid', stackup, 'm3', 'yoffset', 0.34)
    chip.set('pdk','grid', stackup, 'm3', 'ypitch',  0.68)
    chip.set('pdk','grid', stackup, 'm3', 'adj', 0.5)

    chip.set('pdk','grid', stackup, 'm4', 'name', 'met4')
    chip.set('pdk','grid', stackup, 'm4', 'xoffset', 0.46)
    chip.set('pdk','grid', stackup, 'm4', 'xpitch',  0.92)
    chip.set('pdk','grid', stackup, 'm4', 'yoffset', 0.46)
    chip.set('pdk','grid', stackup, 'm4', 'ypitch',  0.92)
    chip.set('pdk','grid', stackup, 'm4', 'adj', 0.5)

    chip.set('pdk','grid', stackup, 'm5', 'name', 'met5')
    chip.set('pdk','grid', stackup, 'm5', 'xoffset', 1.7)
    chip.set('pdk','grid', stackup, 'm5', 'xpitch',  3.4)
    chip.set('pdk','grid', stackup, 'm5', 'yoffset', 1.7)
    chip.set('pdk','grid', stackup, 'm5', 'ypitch',  3.4)
    chip.set('pdk','grid', stackup, 'm5', 'adj', 0.5)


####################################################
# Library Setup
####################################################
def setup_libs(chip, vendor=None):

    foundry = 'skywater'
    process = 'skywater130'
    rev = 'v0_0_2'
    libname = 'sky130hd' # not sure if this should be something else
    libtype = 'hd' # TODO: update this

    libwidth = 0.46
    libheight = 2.72

    # TODO: should I be using a different name for the corner
    corner = 'typical'

    libdir = '/'.join(['third_party/foundry',
                       foundry,
                       process,
                       'libs',
                       libname,
                       rev])

    # rev
    chip.set('stdcell',libname,'rev',rev)

    # timing
    chip.set('stdcell',libname, 'model', corner, 'nldm', 'lib',
             libdir+'/lib/sky130_fd_sc_hd__tt_025C_1v80.lib')

    chip.set('stdcell',libname, 'model', corner, 'nldm', 'lib_synth',
             libdir+'/lib/sky130_fd_sc_hd__tt_025C_1v80_synth.lib')
    # lef
    chip.set('stdcell',libname,'lef',
             libdir+'/lef/sky130_fd_sc_hd_merged.lef')
    # gds
    chip.set('stdcell',libname,'gds',
             libdir+'/gds/sky130_fd_sc_hd.gds')
    # site name
    chip.set('stdcell',libname,'site', 'unithd')
    # lib arch
    chip.set('stdcell',libname,'libtype',libtype)

    # lib site/tile/size
    chip.set('stdcell',libname,'width', libwidth)
    chip.set('stdcell',libname,'height', libheight)

    # clock buffers
    chip.add('stdcell',libname,'cells','clkbuf', 'sky130_fd_sc_hd__clkbuf_1')

    # hold cells
    chip.add('stdcell',libname,'cells','hold', 'sky130_fd_sc_hd__buf_1')

    # filler
    chip.add('stdcell',libname,'cells','filler', ['sky130_fd_sc_hd__fill_1',
                                                  'sky130_fd_sc_hd__fill_2',
                                                  'sky130_fd_sc_hd__fill_4',
                                                  'sky130_fd_sc_hd__fill_8'])

    # Tapcell
    chip.add('stdcell',libname,'cells','tapcell', 'sky130_fd_sc_hd__tapvpwrvgnd_1')

    # Endcap
    chip.add('stdcell',libname,'cells','endcap', 'sky130_fd_sc_hd__decap_4')

    chip.add('stdcell',libname,'cells','ignore', [
        'sky130_fd_sc_hd__a2111o_1',
        'sky130_fd_sc_hd__a2111oi_0',
        'sky130_fd_sc_hd__a2111oi_1',
        'sky130_fd_sc_hd__a211o_1',
        'sky130_fd_sc_hd__a211oi_1',
        'sky130_fd_sc_hd__a21bo_1',
        'sky130_fd_sc_hd__a21boi_0',
        'sky130_fd_sc_hd__a21boi_1',
        'sky130_fd_sc_hd__a21o_1',
        'sky130_fd_sc_hd__a21oi_1',
        'sky130_fd_sc_hd__a221o_1',
        'sky130_fd_sc_hd__a221oi_1',
        'sky130_fd_sc_hd__a222oi_1',
        'sky130_fd_sc_hd__a22o_1',
        'sky130_fd_sc_hd__a22oi_1',
        'sky130_fd_sc_hd__a2bb2o_1',
        'sky130_fd_sc_hd__a2bb2oi_1',
        'sky130_fd_sc_hd__a311o_1',
        'sky130_fd_sc_hd__a311oi_1',
        'sky130_fd_sc_hd__a31o_1',
        'sky130_fd_sc_hd__a31oi_1',
        'sky130_fd_sc_hd__a32o_1',
        'sky130_fd_sc_hd__a32oi_1',
        'sky130_fd_sc_hd__a41o_1',
        'sky130_fd_sc_hd__a41oi_1',
        'sky130_fd_sc_hd__and2_0',
        'sky130_fd_sc_hd__and2_1',
        'sky130_fd_sc_hd__and2b_1',
        'sky130_fd_sc_hd__and3_1',
        'sky130_fd_sc_hd__and3b_1',
        'sky130_fd_sc_hd__and4_1',
        'sky130_fd_sc_hd__and4b_1',
        'sky130_fd_sc_hd__and4bb_1',
        'sky130_fd_sc_hd__buf_16',
        'sky130_fd_sc_hd__clkbuf_1',
        'sky130_fd_sc_hd__clkbuf_16',
        'sky130_fd_sc_hd__clkbuf_2',
        'sky130_fd_sc_hd__clkbuf_4',
        'sky130_fd_sc_hd__clkbuf_8',
        'sky130_fd_sc_hd__clkdlybuf4s15_1',
        'sky130_fd_sc_hd__clkdlybuf4s15_2',
        'sky130_fd_sc_hd__clkdlybuf4s18_1',
        'sky130_fd_sc_hd__clkdlybuf4s18_2',
        'sky130_fd_sc_hd__clkdlybuf4s25_1',
        'sky130_fd_sc_hd__clkdlybuf4s25_2',
        'sky130_fd_sc_hd__clkdlybuf4s50_1',
        'sky130_fd_sc_hd__clkdlybuf4s50_2',
        'sky130_fd_sc_hd__clkinv_1',
        'sky130_fd_sc_hd__clkinv_16',
        'sky130_fd_sc_hd__clkinv_2',
        'sky130_fd_sc_hd__clkinv_4',
        'sky130_fd_sc_hd__clkinv_8',
        'sky130_fd_sc_hd__clkinvlp_2',
        'sky130_fd_sc_hd__clkinvlp_4',
        'sky130_fd_sc_hd__decap_12',
        'sky130_fd_sc_hd__decap_3',
        'sky130_fd_sc_hd__decap_4',
        'sky130_fd_sc_hd__decap_6',
        'sky130_fd_sc_hd__decap_8',
        'sky130_fd_sc_hd__dfbbn_1',
        'sky130_fd_sc_hd__dfbbp_1',
        'sky130_fd_sc_hd__dfrbp_1',
        'sky130_fd_sc_hd__dfrtn_1',
        'sky130_fd_sc_hd__dfrtp_1',
        'sky130_fd_sc_hd__dfrtp_4',
        'sky130_fd_sc_hd__dfsbp_1',
        'sky130_fd_sc_hd__dfstp_1',
        'sky130_fd_sc_hd__dfxbp_1',
        'sky130_fd_sc_hd__dfxtp_1',
        'sky130_fd_sc_hd__diode_2',
        'sky130_fd_sc_hd__dlclkp_1',
        'sky130_fd_sc_hd__dlclkp_2',
        'sky130_fd_sc_hd__dlclkp_4',
        'sky130_fd_sc_hd__dlrbn_1',
        'sky130_fd_sc_hd__dlrbn_2',
        'sky130_fd_sc_hd__dlrbp_1',
        'sky130_fd_sc_hd__dlrbp_2',
        'sky130_fd_sc_hd__dlrtn_1',
        'sky130_fd_sc_hd__dlrtn_2',
        'sky130_fd_sc_hd__dlrtn_4',
        'sky130_fd_sc_hd__dlrtp_1',
        'sky130_fd_sc_hd__dlrtp_2',
        'sky130_fd_sc_hd__dlrtp_4',
        'sky130_fd_sc_hd__dlxbn_1',
        'sky130_fd_sc_hd__dlxbn_2',
        'sky130_fd_sc_hd__dlxbp_1',
        'sky130_fd_sc_hd__dlygate4sd1_1',
        'sky130_fd_sc_hd__dlygate4sd2_1',
        'sky130_fd_sc_hd__dlygate4sd3_1',
        'sky130_fd_sc_hd__dlymetal6s2s_1',
        'sky130_fd_sc_hd__dlymetal6s4s_1',
        'sky130_fd_sc_hd__dlymetal6s6s_1',
        'sky130_fd_sc_hd__ebufn_1',
        'sky130_fd_sc_hd__edfxbp_1',
        'sky130_fd_sc_hd__edfxtp_1',
        'sky130_fd_sc_hd__einvn_0',
        'sky130_fd_sc_hd__einvn_1',
        'sky130_fd_sc_hd__einvn_2',
        'sky130_fd_sc_hd__einvn_4',
        'sky130_fd_sc_hd__einvn_8',
        'sky130_fd_sc_hd__einvp_1',
        'sky130_fd_sc_hd__einvp_2',
        'sky130_fd_sc_hd__einvp_4',
        'sky130_fd_sc_hd__einvp_8',
        'sky130_fd_sc_hd__fa_4',
        'sky130_fd_sc_hd__fah_1',
        'sky130_fd_sc_hd__fahcin_1',
        'sky130_fd_sc_hd__fahcon_1',
        'sky130_fd_sc_hd__ha_1',
        'sky130_fd_sc_hd__ha_2',
        'sky130_fd_sc_hd__ha_4',
        'sky130_fd_sc_hd__inv_1',
        'sky130_fd_sc_hd__lpflow_bleeder_1',
        'sky130_fd_sc_hd__lpflow_clkbufkapwr_1',
        'sky130_fd_sc_hd__lpflow_clkbufkapwr_16',
        'sky130_fd_sc_hd__lpflow_clkbufkapwr_2',
        'sky130_fd_sc_hd__lpflow_clkbufkapwr_4',
        'sky130_fd_sc_hd__lpflow_clkbufkapwr_8',
        'sky130_fd_sc_hd__lpflow_clkinvkapwr_1',
        'sky130_fd_sc_hd__lpflow_clkinvkapwr_16',
        'sky130_fd_sc_hd__lpflow_clkinvkapwr_2',
        'sky130_fd_sc_hd__lpflow_clkinvkapwr_4',
        'sky130_fd_sc_hd__lpflow_clkinvkapwr_8',
        'sky130_fd_sc_hd__lpflow_decapkapwr_12',
        'sky130_fd_sc_hd__lpflow_decapkapwr_3',
        'sky130_fd_sc_hd__lpflow_decapkapwr_4',
        'sky130_fd_sc_hd__lpflow_decapkapwr_6',
        'sky130_fd_sc_hd__lpflow_decapkapwr_8',
        'sky130_fd_sc_hd__lpflow_inputiso0n_1',
        'sky130_fd_sc_hd__lpflow_inputiso0p_1',
        'sky130_fd_sc_hd__lpflow_inputiso1n_1',
        'sky130_fd_sc_hd__lpflow_inputiso1p_1',
        'sky130_fd_sc_hd__lpflow_inputisolatch_1',
        'sky130_fd_sc_hd__lpflow_isobufsrc_1',
        'sky130_fd_sc_hd__lpflow_isobufsrc_16',
        'sky130_fd_sc_hd__lpflow_isobufsrc_2',
        'sky130_fd_sc_hd__lpflow_isobufsrc_4',
        'sky130_fd_sc_hd__lpflow_isobufsrc_8',
        'sky130_fd_sc_hd__lpflow_isobufsrckapwr_16',
        'sky130_fd_sc_hd__lpflow_lsbuf_lh_hl_isowell_tap_1',
        'sky130_fd_sc_hd__lpflow_lsbuf_lh_hl_isowell_tap_2',
        'sky130_fd_sc_hd__lpflow_lsbuf_lh_hl_isowell_tap_4',
        'sky130_fd_sc_hd__lpflow_lsbuf_lh_isowell_4',
        'sky130_fd_sc_hd__lpflow_lsbuf_lh_isowell_tap_1',
        'sky130_fd_sc_hd__lpflow_lsbuf_lh_isowell_tap_2',
        'sky130_fd_sc_hd__lpflow_lsbuf_lh_isowell_tap_4',
        'sky130_fd_sc_hd__macro_sparecell',
        'sky130_fd_sc_hd__maj3_1',
        'sky130_fd_sc_hd__maj3_2',
        'sky130_fd_sc_hd__maj3_4',
        'sky130_fd_sc_hd__mux2i_1',
        'sky130_fd_sc_hd__mux2i_2',
        'sky130_fd_sc_hd__mux2i_4',
        'sky130_fd_sc_hd__mux4_2',
        'sky130_fd_sc_hd__mux4_4',
        'sky130_fd_sc_hd__nand2_1',
        'sky130_fd_sc_hd__nand2b_1',
        'sky130_fd_sc_hd__nand3_1',
        'sky130_fd_sc_hd__nand3b_1',
        'sky130_fd_sc_hd__nand4_1',
        'sky130_fd_sc_hd__nand4b_1',
        'sky130_fd_sc_hd__nand4bb_1',
        'sky130_fd_sc_hd__nor2_1',
        'sky130_fd_sc_hd__nor2b_1',
        'sky130_fd_sc_hd__nor3_1',
        'sky130_fd_sc_hd__nor3b_1',
        'sky130_fd_sc_hd__nor4_1',
        'sky130_fd_sc_hd__nor4b_1',
        'sky130_fd_sc_hd__nor4bb_1',
        'sky130_fd_sc_hd__o2111a_1',
        'sky130_fd_sc_hd__o2111ai_1',
        'sky130_fd_sc_hd__o211a_1',
        'sky130_fd_sc_hd__o211ai_1',
        'sky130_fd_sc_hd__o21a_1',
        'sky130_fd_sc_hd__o21ai_0',
        'sky130_fd_sc_hd__o21ai_1',
        'sky130_fd_sc_hd__o21ba_1',
        'sky130_fd_sc_hd__o21bai_1',
        'sky130_fd_sc_hd__o221a_1',
        'sky130_fd_sc_hd__o221ai_1',
        'sky130_fd_sc_hd__o22a_1',
        'sky130_fd_sc_hd__o22ai_1',
        'sky130_fd_sc_hd__o2bb2a_1',
        'sky130_fd_sc_hd__o2bb2ai_1',
        'sky130_fd_sc_hd__o311a_1',
        'sky130_fd_sc_hd__o311ai_0',
        'sky130_fd_sc_hd__o311ai_1',
        'sky130_fd_sc_hd__o31a_1',
        'sky130_fd_sc_hd__o31ai_1',
        'sky130_fd_sc_hd__o32a_1',
        'sky130_fd_sc_hd__o32ai_1',
        'sky130_fd_sc_hd__o41a_1',
        'sky130_fd_sc_hd__o41ai_1',
        'sky130_fd_sc_hd__or2_0',
        'sky130_fd_sc_hd__or2_1',
        'sky130_fd_sc_hd__or2b_1',
        'sky130_fd_sc_hd__or3_1',
        'sky130_fd_sc_hd__or3b_1',
        'sky130_fd_sc_hd__or4_1',
        'sky130_fd_sc_hd__or4b_1',
        'sky130_fd_sc_hd__or4bb_1',
        'sky130_fd_sc_hd__probe_p_8',
        'sky130_fd_sc_hd__probec_p_8',
        'sky130_fd_sc_hd__sdfbbn_1',
        'sky130_fd_sc_hd__sdfbbn_2',
        'sky130_fd_sc_hd__sdfbbp_1',
        'sky130_fd_sc_hd__sdfrbp_1',
        'sky130_fd_sc_hd__sdfrbp_2',
        'sky130_fd_sc_hd__sdfrtn_1',
        'sky130_fd_sc_hd__sdfrtp_1',
        'sky130_fd_sc_hd__sdfrtp_2',
        'sky130_fd_sc_hd__sdfrtp_4',
        'sky130_fd_sc_hd__sdfsbp_1',
        'sky130_fd_sc_hd__sdfsbp_2',
        'sky130_fd_sc_hd__sdfstp_1',
        'sky130_fd_sc_hd__sdfstp_2',
        'sky130_fd_sc_hd__sdfstp_4',
        'sky130_fd_sc_hd__sdfxbp_1',
        'sky130_fd_sc_hd__sdfxbp_2',
        'sky130_fd_sc_hd__sdfxtp_1',
        'sky130_fd_sc_hd__sdfxtp_2',
        'sky130_fd_sc_hd__sdfxtp_4',
        'sky130_fd_sc_hd__sdlclkp_1',
        'sky130_fd_sc_hd__sdlclkp_2',
        'sky130_fd_sc_hd__sdlclkp_4',
        'sky130_fd_sc_hd__sedfxbp_1',
        'sky130_fd_sc_hd__sedfxbp_2',
        'sky130_fd_sc_hd__sedfxtp_1',
        'sky130_fd_sc_hd__sedfxtp_2',
        'sky130_fd_sc_hd__sedfxtp_4',
        'sky130_fd_sc_hd__xnor2_1',
        'sky130_fd_sc_hd__xnor3_1',
        'sky130_fd_sc_hd__xnor3_2',
        'sky130_fd_sc_hd__xnor3_4',
        'sky130_fd_sc_hd__xor2_1',
        'sky130_fd_sc_hd__xor3_1',
        'sky130_fd_sc_hd__xor3_2',
        'sky130_fd_sc_hd__xor3_4'
    ])

    # TODO: should probably fill these in, but they're currently unused by
    # OpenROAD flow
    #driver
    chip.set('stdcell',libname,'driver', '')

    # tie cells
    chip.add('stdcell',libname,'cells','tie', ['sky130_fd_sc_hd__conb_1/HI',
                                               'sky130_fd_sc_hd__conb_1/LO'])

#########################
def setup_design(chip):

    chip.set('asic', 'stackup', chip.get('pdk', 'stackup')[0])
    chip.set('asic', 'targetlib', chip.getkeys('stdcell'))
    # TODO: how does LI get taken into account?
    chip.set('asic', 'minlayer', "m1")
    chip.set('asic', 'maxlayer', "m5")

    chip.set('asic', 'maxfanout', 5) # TODO: fix this
    chip.set('asic', 'maxlength', 21000)
    chip.set('asic', 'maxslew', 1.5e-9)
    chip.set('asic', 'maxcap', .1532e-12)
    chip.set('asic', 'clklayer', "m5")
    chip.set('asic', 'rclayer', "m3")
    chip.set('asic', 'hpinlayer', "m3")
    chip.set('asic', 'vpinlayer', "m2")
    chip.set('asic', 'density', 0.6) # TODO: should density be 0.6 like in OpenROAD config.mk, or 1.0

    corner = 'typical'
    # hard coded mcmm settings (only one corner!)
    chip.set('mcmm','worst','libcorner', corner)
    chip.set('mcmm','worst','pexcorner', corner)
    chip.set('mcmm','worst','mode', 'func')
    chip.set('mcmm','worst','check', ['setup','hold'])

#########################
if __name__ == "__main__":

    # File being executed
    prefix = os.path.splitext(os.path.basename(__file__))[0]
    output = prefix + '.json'

    # create a chip instance
    chip = siliconcompiler.Chip()
    # load configuration
    setup_platform(chip)
    setup_libs(chip)
    # write out result
    chip.writecfg(output)


