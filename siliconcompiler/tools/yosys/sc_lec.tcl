# Script adapted from
# https://github.com/The-OpenROAD-Project/OpenLane/blob/d052a918f4a46ddbae0ad09812f6cd0b8eb4a1e5/scripts/logic_equiv_check.tcl

source ./sc_manifest.tcl
set sc_tool yosys
yosys echo on

#Handling remote/local script execution
set sc_step   [dict get $sc_cfg arg step]
set sc_index  [dict get $sc_cfg arg index]

if {[dict get $sc_cfg eda $sc_tool copy] eq True} {
    set sc_refdir "."
} else {
    set sc_refdir [dict get $sc_cfg eda $sc_tool refdir $sc_step $sc_index ]
}

set sc_mode        [dict get $sc_cfg mode]
set sc_design      [dict get $sc_cfg design]
set sc_targetlibs  [dict get $sc_cfg asic targetlib]
set lib [lindex $sc_targetlibs 0]
set sc_liberty [dict get $sc_cfg library $lib nldm typical lib]

if {[dict exists $sc_cfg eda $sc_tool "variable" $sc_step $sc_index induction_steps]} {
    set sc_induction_steps [lindex [dict get $sc_cfg eda $sc_tool "variable" $sc_step $sc_index induction_steps] 0]
} else {
    # Yosys default
    set sc_induction_steps 4
}

# Gold netlist
yosys read_liberty -ignore_miss_func $sc_liberty
if {[file exists "inputs/$sc_design.v"]} {
    set source "inputs/$sc_design.v"
} else {
    set source [lindex [dict get $sc_cfg source] 0]
}
yosys read_verilog $source

yosys proc
yosys rmports
yosys splitnets -ports
yosys hierarchy -auto-top
yosys flatten

yosys setattr -set keep 1
yosys stat
yosys rename -top gold
yosys design -stash gold

# Gate netlist
yosys read_liberty -ignore_miss_func $sc_liberty
if {[dict exists $sc_cfg read netlist $sc_step $sc_index]} {
    set netlist [lindex [dict get $sc_cfg read netlist $sc_step $sc_index] 0]
} else {
    set netlist "inputs/$design.vg"
}
yosys read_verilog $netlist

yosys proc
yosys rmports
yosys splitnets -ports
yosys hierarchy -auto-top
yosys flatten

yosys setattr -set keep 1
yosys stat
yosys rename -top gate
yosys design -stash gate

yosys design -copy-from gold -as gold gold
yosys design -copy-from gate -as gate gate

# Rebuild the database due to -stash
yosys read_liberty -ignore_miss_func $sc_liberty

yosys equiv_make gold gate equiv

yosys setattr -set keep 1
yosys prep -flatten -top equiv
yosys equiv_induct -seq $sc_induction_steps
yosys equiv_status
