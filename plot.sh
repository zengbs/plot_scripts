#!/bin/bash

Posi_Max=40
Posi_Min=40
CutAxis="z"
DumpIDMin=$1
DumpIDMax=$2
Zoom=1
AxisUnit="kpc"
NumSlice=1
File="png"
Title="default"


# =======  proper mass density
CbrMax="nan"
CbrMin="nan"
NameCbr="rho(ambient)/rho(src)"
LogScale=1
LinThresh=-1
Grid=0
NormalizedConst=6e-26

python plot_scripts/slice.py -f proper_mass_density -sx $Posi_Min -ex $Posi_Max -st $DumpIDMin -et $DumpIDMax -l $LogScale -z $Zoom -nx $NumSlice -g $Grid -p $CutAxis -title $Title -axunit $AxisUnit -namecbr $NameCbr -fileformat $File -linthesh $LinThresh -max $CbrMax -min $CbrMin -normalconst $NormalizedConst

# =======  temperature
CbrMax="nan"
CbrMin="nan"
NameCbr="default"
LogScale=1
LinThresh=-1
Grid=0

#python plot_scripts/slice.py -f temperature_sr      -sx $Posi_Min -ex $Posi_Max -st $DumpIDMin -et $DumpIDMax -l $LogScale -z $Zoom -nx $NumSlice -g $Grid -p $CutAxis -title $Title -axunit $AxisUnit -namecbr $NameCbr -fileformat $File -linthesh $LinThresh -max $CbrMax -min $CbrMin -normalconst $NormalizedConst

# =======  pressure
CbrMax="nan"
CbrMin="nan"
NameCbr="P(ambient)/P(src)"
LogScale=1
LinThresh=-1
Grid=0
NormalizedConst=5.4e-6

#python plot_scripts/slice.py -f pressure_sr         -sx $Posi_Min -ex $Posi_Max -st $DumpIDMin -et $DumpIDMax -l $LogScale -z $Zoom -nx $NumSlice -g $Grid -p $CutAxis -title $Title -axunit $AxisUnit -namecbr $NameCbr -fileformat $File -linthesh $LinThresh -max $CbrMax -min $CbrMin -normalconst $NormalizedConst

# =======  Lorentz factor
CbrMax="nan"
CbrMin="nan"
NameCbr="default"
LogScale=0
LinThresh=-1
Grid=0

#python plot_scripts/slice.py -f Lorentz_factor      -sx $Posi_Min -ex $Posi_Max -st $DumpIDMin -et $DumpIDMax -l $LogScale -z $Zoom -nx $NumSlice -g $Grid -p $CutAxis -title $Title -axunit $AxisUnit -namecbr $NameCbr -fileformat $File -linthesh $LinThresh -max $CbrMax -min $CbrMin -normalconst $NormalizedConst

# =======  synchrotron map
CbrMax="nan"
CbrMin="nan"
NameCbr="default"
LogScale=0
LinThresh=-1
Grid=0

#python plot_scripts/projection.py -f synchrotron_emissivity -stheta 0 -etheta 0 -sphi 0 -ephi 0 -nx $NumSlice -st $DumpIDMin -et $DumpIDMax -l $LogScale -z $Zoom


# =======  Avalible field
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
