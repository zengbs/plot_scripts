#!/bin/bash

SpeedOfLight=299792458

Posi_Max=50
Posi_Min=50
CutAxis="z"
DumpIDMin=$1
DumpIDMax=$2
Zoom=1
AxisUnit="kpc"
NumSlice=1
File="eps"
Title="nan"
Axis=0
TimeStamp=1
UserTime=1
TimeUnit=" L/\$c$"
Cbr=1
Offset="0.0,-2.5,0.0"
Width="25,19"
#Width="0,0"


# =======  proper mass density
CbrMax="nan"
CbrMin="nan"
NameCbr="\rho/\rho_{0}~$"
LogScale=1
LinThresh=-1
Grid=0
NormalizedConst=2e-25

python plot_scripts/slice.py -f proper_mass_density -sx $Posi_Min -ex $Posi_Max -st $DumpIDMin -et $DumpIDMax -l $LogScale -z $Zoom -nx $NumSlice -g $Grid -p $CutAxis -title $Title -axunit $AxisUnit -namecbr $NameCbr -fileformat $File -linthesh $LinThresh -max $CbrMax -min $CbrMin -normalconst $NormalizedConst -axis $Axis -timestamp $TimeStamp -usertime $UserTime -timeunit $TimeUnit -cbr $Cbr -Offset $Offset -Width $Width

# =======  temperature
CbrMax="nan"
CbrMin="nan"
NameCbr="k_{B}T/mc^{2}~$"
LogScale=1
LinThresh=-1
Grid=0

python plot_scripts/slice.py -f temperature_sr      -sx $Posi_Min -ex $Posi_Max -st $DumpIDMin -et $DumpIDMax -l $LogScale -z $Zoom -nx $NumSlice -g $Grid -p $CutAxis -title $Title -axunit $AxisUnit -namecbr $NameCbr -fileformat $File -linthesh $LinThresh -max $CbrMax -min $CbrMin -normalconst $NormalizedConst -axis $Axis -timestamp $TimeStamp -usertime $UserTime -timeunit $TimeUnit -cbr $Cbr -Offset $Offset -Width $Width

# =======  pressure
CbrMax="nan"
CbrMin="nan"
NameCbr="P/P_{0}~$"
LogScale=1
LinThresh=-1
Grid=0
NormalizedConst=8.987551787368177e-05
python plot_scripts/slice.py -f pressure_sr      -sx $Posi_Min -ex $Posi_Max -st $DumpIDMin -et $DumpIDMax -l $LogScale -z $Zoom -nx $NumSlice -g $Grid -p $CutAxis -title $Title -axunit $AxisUnit -namecbr $NameCbr -fileformat $File -linthesh $LinThresh -max $CbrMax -min $CbrMin -normalconst $NormalizedConst -axis $Axis -timestamp $TimeStamp -usertime $UserTime -timeunit $TimeUnit -cbr $Cbr -Offset $Offset -Width $Width


# =======  Lorentz factor
CbrMax="nan"
CbrMin="nan"
NameCbr="\gamma~$"
LogScale=0
LinThresh=-1
Grid=0

python plot_scripts/slice.py -f Lorentz_factor      -sx $Posi_Min -ex $Posi_Max -st $DumpIDMin -et $DumpIDMax -l $LogScale -z $Zoom -nx $NumSlice -g $Grid -p $CutAxis -title $Title -axunit $AxisUnit -namecbr $NameCbr -fileformat $File -linthesh $LinThresh -max $CbrMax -min $CbrMin -normalconst $NormalizedConst -axis $Axis -timestamp $TimeStamp -usertime $UserTime -timeunit $TimeUnit -cbr $Cbr -Width $Width -Offset $Offset

CbrMax="nan"
CbrMin="nan"
NameCbr="h\gamma/c^2~$"
LogScale=0
NormalizedConst=1

python plot_scripts/slice.py -f Bernoulli_constant   -sx $Posi_Min -ex $Posi_Max -st $DumpIDMin -et $DumpIDMax -l $LogScale -z $Zoom -nx $NumSlice -g $Grid -p $CutAxis -title $Title -axunit $AxisUnit -namecbr $NameCbr -fileformat $File -linthesh $LinThresh -max $CbrMax -min $CbrMin -normalconst $NormalizedConst -axis $Axis -timestamp $TimeStamp -usertime $UserTime -timeunit $TimeUnit -cbr $Cbr -Offset $Offset -Width $Width
#python plot_scripts/slice.py -f specific_enthalpy_sr -sx $Posi_Min -ex $Posi_Max -st $DumpIDMin -et $DumpIDMax -l $LogScale -z $Zoom -nx $NumSlice -g $Grid -p $CutAxis -title $Title -axunit $AxisUnit -name4br $NameCbr -fileformat $File -linthesh $LinThresh -max $CbrMax -min $CbrMin -normalconst $NormalizedConst -axis $Axis -timestamp $TimeStamp -usertime $UserTime -timeunit $TimeUnit -cbr $Cbr -Offset $Offset -Width $Width

# =======  synchrotron map
CbrMax="nan"
CbrMin="nan"
NameCbr="default"
LogScale=0
LinThresh=-1
Grid=0

#python plot_scripts/projection.py -f synchrotron_emissivity -stheta 0 -etheta 0 -sphi 0 -ephi 0 -nx $NumSlice -st $DumpIDMin -et $DumpIDMax -l $LogScale -z $Zoom -axis $Axis -timestamp $TimeStamp -usertime $UserTime -timeunit $TimeUnit -cbr $Cbr -Offset $Offset -Width $Width


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
