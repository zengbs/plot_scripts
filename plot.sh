#!/bin/bash

SpeedOfLight=29979245800

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
Axis=1
TimeStamp=1
UserTime=1
TimeUnit=" L/\$c$"
Cbr=1
Offset="0.0,-2.75,0.0"
Width="28,16.5"
#Width="0,0"

NormalizedConst="0,0"  # "rho,pres"
Resolution=150
FigSize=-1  # the longest side in inches

# =======  proper mass density
CbrMax="nan"
CbrMin="nan"
NameCbr="\rho/\rho_{0}~$"
LogScale=1
LinThresh=-1
Grid=0

python plot_scripts/slice.py -f proper_mass_density -sx $Posi_Min -ex $Posi_Max -st $DumpIDMin -et $DumpIDMax -l $LogScale -z $Zoom -nx $NumSlice -g $Grid -p $CutAxis -title $Title -axunit $AxisUnit -namecbr $NameCbr -fileformat $File -linthesh $LinThresh -max $CbrMax -min $CbrMin -normalconst $NormalizedConst -axis $Axis -timestamp $TimeStamp -usertime $UserTime -timeunit $TimeUnit -cbr $Cbr -Offset $Offset -Width $Width -res $Resolution -FigSize $FigSize

# =======  temperature
CbrMax="nan"
CbrMin="nan"
NameCbr="k_{B}T/mc^{2}~$"
LogScale=1
LinThresh=-1
Grid=0

python plot_scripts/slice.py -f temperature_sr      -sx $Posi_Min -ex $Posi_Max -st $DumpIDMin -et $DumpIDMax -l $LogScale -z $Zoom -nx $NumSlice -g $Grid -p $CutAxis -title $Title -axunit $AxisUnit -namecbr $NameCbr -fileformat $File -linthesh $LinThresh -max $CbrMax -min $CbrMin -normalconst $NormalizedConst -axis $Axis -timestamp $TimeStamp -usertime $UserTime -timeunit $TimeUnit -cbr $Cbr -Offset $Offset -Width $Width -res $Resolution -FigSize $FigSize

NameCbr="v/c~$"
LogScale=0
LinThresh=-1
#python plot_scripts/slice.py -f 3_velocity_magnitude    -sx $Posi_Min -ex $Posi_Max -st $DumpIDMin -et $DumpIDMax -l $LogScale -z $Zoom -nx $NumSlice -g $Grid -p $CutAxis -title $Title -axunit $AxisUnit -namecbr $NameCbr -fileformat $File -linthesh $LinThresh -max $CbrMax -min $CbrMin -normalconst $NormalizedConst -axis $Axis -timestamp $TimeStamp -usertime $UserTime -timeunit $TimeUnit -cbr $Cbr -Offset $Offset -Width $Width -res $Resolution -FigSize $FigSize

# =======  pressure
CbrMax="nan"
CbrMin="nan"
NameCbr="P/P_{0}~$"
LogScale=1
LinThresh=-1
Grid=0
python plot_scripts/slice.py -f pressure_sr      -sx $Posi_Min -ex $Posi_Max -st $DumpIDMin -et $DumpIDMax -l $LogScale -z $Zoom -nx $NumSlice -g $Grid -p $CutAxis -title $Title -axunit $AxisUnit -namecbr $NameCbr -fileformat $File -linthesh $LinThresh -max $CbrMax -min $CbrMin -normalconst $NormalizedConst -axis $Axis -timestamp $TimeStamp -usertime $UserTime -timeunit $TimeUnit -cbr $Cbr -Offset $Offset -Width $Width -res $Resolution -FigSize $FigSize


# =======  Lorentz factor
CbrMax="nan"
CbrMin=1
NameCbr="\gamma~$"
LogScale=0
LinThresh=-1
Grid=0

python plot_scripts/slice.py -f Lorentz_factor      -sx $Posi_Min -ex $Posi_Max -st $DumpIDMin -et $DumpIDMax -l $LogScale -z $Zoom -nx $NumSlice -g $Grid -p $CutAxis -title $Title -axunit $AxisUnit -namecbr $NameCbr -fileformat $File -linthesh $LinThresh -max $CbrMax -min $CbrMin -normalconst $NormalizedConst -axis $Axis -timestamp $TimeStamp -usertime $UserTime -timeunit $TimeUnit -cbr $Cbr -Width $Width -Offset $Offset -res $Resolution -FigSize $FigSize

CbrMax=26.290
CbrMin=26.245
NameCbr="h\gamma/c^2~$"
LogScale=0
Cbr=1

#python plot_scripts/slice.py -f Bernoulli_constant   -sx $Posi_Min -ex $Posi_Max -st $DumpIDMin -et $DumpIDMax -l $LogScale -z $Zoom -nx $NumSlice -g $Grid -p $CutAxis -title $Title -axunit $AxisUnit -namecbr $NameCbr -fileformat $File -linthesh $LinThresh -max $CbrMax -min $CbrMin -normalconst $NormalizedConst -axis $Axis -timestamp $TimeStamp -usertime $UserTime -timeunit $TimeUnit -cbr $Cbr -Offset $Offset -Width $Width -res $Resolution -FigSize $FigSize

# =======  synchrotron map
CbrMax="nan"
CbrMin="nan"
NameCbr="default"
LogScale=0
LinThresh=-1
Grid=0

#python plot_scripts/projection.py -f synchrotron_emissivity -stheta 0 -etheta 0 -sphi 0 -ephi 0 -nx $NumSlice -st $DumpIDMin -et $DumpIDMax -l $LogScale -z $Zoom -axis $Axis -timestamp $TimeStamp -usertime $UserTime -timeunit $TimeUnit -cbr $Cbr -Offset $Offset -Width $Width -res $Resolution -FigSize $FigSize


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
