#!/bin/bash

Posi_Max=50
Posi_Min=50
CutAxis="z"
DumpIDMin=$1
DumpIDMax=$2
Zoom=4
AxisUnit="kpc"
NumSlice=1
File="eps"
Title="nan"
Axis=1
TimeStamp=1
UserTime=1
TimeUnit=" L/\$c$"
Cbr=1
Offset="0.0,5.0,0.0"


# =======  proper mass density
CbrMax="nan"
CbrMin="nan"
NameCbr="default"
LogScale=1
LinThresh=-1
Grid=0
NormalizedConst=1

#python plot_scripts/slice.py -f proper_mass_density -sx $Posi_Min -ex $Posi_Max -st $DumpIDMin -et $DumpIDMax -l $LogScale -z $Zoom -nx $NumSlice -g $Grid -p $CutAxis -title $Title -axunit $AxisUnit -namecbr $NameCbr -fileformat $File -linthesh $LinThresh -max $CbrMax -min $CbrMin -normalconst $NormalizedConst -axis $Axis -timestamp $TimeStamp -usertime $UserTime -timeunit $TimeUnit -cbr $Cbr -Offset $Offset

# =======  temperature
CbrMax="nan"
CbrMin="nan"
NameCbr="default"
LogScale=1
LinThresh=-1
Grid=0

#python plot_scripts/slice.py -f temperature_sr      -sx $Posi_Min -ex $Posi_Max -st $DumpIDMin -et $DumpIDMax -l $LogScale -z $Zoom -nx $NumSlice -g $Grid -p $CutAxis -title $Title -axunit $AxisUnit -namecbr $NameCbr -fileformat $File -linthesh $LinThresh -max $CbrMax -min $CbrMin -normalconst $NormalizedConst -axis $Axis -timestamp $TimeStamp -usertime $UserTime -timeunit $TimeUnit -cbr $Cbr -Offset $Offset

# =======  pressure
CbrMax="nan"
CbrMin="nan"
NameCbr="default"
LogScale=1
LinThresh=-1
Grid=0
NormalizedConst=1

#python plot_scripts/slice.py -f pressure_sr          -sx $Posi_Min -ex $Posi_Max -st $DumpIDMin -et $DumpIDMax -l $LogScale -z $Zoom -nx $NumSlice -g $Grid -p $CutAxis -title $Title -axunit $AxisUnit -namecbr $NameCbr -fileformat $File -linthesh $LinThresh -max $CbrMax -min $CbrMin -normalconst $NormalizedConst -axis $Axis -timestamp $TimeStamp -usertime $UserTime -cbr $Cbr -Offset $Offset

# =======  Lorentz factor
CbrMax="nan"
CbrMin="nan"
NameCbr="$\gamma$"
LogScale=0
LinThresh=-1
Grid=0

python plot_scripts/slice.py -f Lorentz_factor      -sx $Posi_Min -ex $Posi_Max -st $DumpIDMin -et $DumpIDMax -l $LogScale -z $Zoom -nx $NumSlice -g $Grid -p $CutAxis -title $Title -axunit $AxisUnit -namecbr $NameCbr -fileformat $File -linthesh $LinThresh -max $CbrMax -min $CbrMin -normalconst $NormalizedConst -axis $Axis -timestamp $TimeStamp -usertime $UserTime -timeunit $TimeUnit -cbr $Cbr -Offset $Offset
#python plot_scripts/slice.py -f Bernoulli_constant   -sx $Posi_Min -ex $Posi_Max -st $DumpIDMin -et $DumpIDMax -l $LogScale -z $Zoom -nx $NumSlice -g $Grid -p $CutAxis -title $Title -axunit $AxisUnit -namecbr $NameCbr -fileformat $File -linthesh $LinThresh -max $CbrMax -min $CbrMin -normalconst $NormalizedConst -axis $Axis -timestamp $TimeStamp -usertime $UserTime -timeunit $TimeUnit -cbr $Cbr -Offset $Offset
#python plot_scripts/slice.py -f specific_enthalpy_sr -sx $Posi_Min -ex $Posi_Max -st $DumpIDMin -et $DumpIDMax -l $LogScale -z $Zoom -nx $NumSlice -g $Grid -p $CutAxis -title $Title -axunit $AxisUnit -name4br $NameCbr -fileformat $File -linthesh $LinThresh -max $CbrMax -min $CbrMin -normalconst $NormalizedConst -axis $Axis -timestamp $TimeStamp -usertime $UserTime -timeunit $TimeUnit -cbr $Cbr -Offset $Offset

# =======  synchrotron map
CbrMax="nan"
CbrMin="nan"
NameCbr="default"
LogScale=0
LinThresh=-1
Grid=0

#python plot_scripts/projection.py -f synchrotron_emissivity -stheta 0 -etheta 0 -sphi 0 -ephi 0 -nx $NumSlice -st $DumpIDMin -et $DumpIDMax -l $LogScale -z $Zoom -axis $Axis -timestamp $TimeStamp -usertime $UserTime -timeunit $TimeUnit -cbr $Cbr -Offset $Offset


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
