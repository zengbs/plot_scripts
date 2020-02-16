#!/bin/bash

Posi_Max=0.5
Posi_Min=0.5


CutAxis="x"

DumpIDMax=0
DumpIDMin=0

CbrMax="nan"
CbrMin="nan"

LogScale=1
LinThresh=-1
Zoom=1
Grid=0

AxisUnit="AU"                 # code_length, pc, kpc, Mpc, AU
Title="default"
NameCbr="default"
NumSlice=1
File="png"

NormalizedConst=1999999999

python plot_scripts/slice.py -f temperature_sr -sx $Posi_Min -ex $Posi_Max -st $DumpIDMin -et $DumpIDMax -l $LogScale -z $Zoom -nx $NumSlice -g $Grid -p $CutAxis -title $Title -axunit $AxisUnit -namecbr $NameCbr -fileformat $File -linthesh $LinThresh -max $CbrMax -min $CbrMin -normalconst $NormalizedConst

# proper_mass_density
# pressure_sr
# temperature_sr
# Lorentz_factor
# 4_velocity_x
# 4_velocity_y
# 4_velocity_z
# momentum_x
# momentum_y
# momentum_z
# total_energy_per_volume





#python plot_scripts/slice.py -f proper_number_density    -sx 80 -ex 80 -st $1 -et $2 -l 1 -z 4 -nx 1 -g 0 -p y 
#python plot_scripts/slice.py -f Lorentz_factor           -sx 80 -ex 80 -st $1 -et $2 -l 1 -z 1 -nx 1 -g 0 -p y
#python plot_scripts/slice.py -f pressure_sr              -sx 80 -ex 80 -st $1 -et $2 -l 1 -z 1 -nx 1 -g 0 -p y 
#python plot_scripts/slice.py -f temperature_sr           -sx 80 -ex 80 -st $1 -et $2 -l 1 -z 4 -nx 1 -g 0 -p y
#
#
#
#python plot_scripts/projection.py -f synchrotron_emissivity -stheta 0 -etheta 0 -sphi 0 -ephi 0 -nx 1 -st $1 -et $2 -l 0 -z 1
