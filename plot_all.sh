if [ ! -d "pic" ]; then
  mkdir pic
fi
if [ ! -d "pic/slice" ]; then
  mkdir pic/slice
fi
if [ ! -d "pic/projection" ]; then
  mkdir pic/projection
fi
################## get options ####################

usage() { 
printf -- "Usage: $0\n" 
printf -- "-c           plot slice of conserved quanties\n"
printf -- "-p           plot slice of primitive quanties\n" 
printf -- "-a          plot projected primitive quanties\n" 
printf -- "-b          plot projected conserved quanties\n"
printf -- "<number1>                         start point\n" 
printf -- "<number2>                           end point\n"
printf -- "<number3>                    delta data index\n"
exit 1; 
}

start=$2
end=$3
did=$4

while getopts ":cpab" opt; 
do
    case "${opt}" in
        c)
############## slice conserved quanties  ##################
             
             if [ ! -d "pic/slice/number_density" ]; then
               mkdir pic/slice/number_density
             fi
             
             python scripts/slice/number_density.py -s $start -e $end -d $did
             mv *.png pic/slice/number_density/
             
             
             if [ ! -d "pic/slice/momentum_x" ]; then
               mkdir pic/slice/momentum_x
             fi
             
             python scripts/slice/MomX.py -s $start -e $end -d $did
             mv *.png pic/slice/momentum_x/
             
             
             if [ ! -d "pic/slice/momentum_y" ]; then
             mkdir pic/slice/momentum_y
             fi
             
             python scripts/slice/MomY.py -s $start -e $end -d $did
             mv *.png pic/slice/momentum_y/
             
             
             if [ ! -d "pic/slice/momentum_z" ]; then
             mkdir pic/slice/momentum_z
             fi
             
             python scripts/slice/MomZ.py -s $start -e $end -d $did
             mv *.png pic/slice/momentum_z/
             
             
             if [ ! -d "pic/slice/energy_density" ]; then
             mkdir pic/slice/energy_density
             fi
             
             python scripts/slice/energy.py -s $start -e $end -d $did
             mv *.png pic/slice/energy_density/ ;;
             
        p)
############## slice primitive quanties  ##################

             if [ ! -d "pic/slice/proper_number_density" ]; then
             mkdir pic/slice/proper_number_density
             fi
             
             python scripts/slice/proper_number_density.py -s $start -e $end -d $did
             mv *.png pic/slice/proper_number_density/
             
             
             if [ ! -d "pic/slice/Ux" ]; then
             mkdir pic/slice/Ux
             fi
             
             python scripts/slice/Ux.py -s $start -e $end -d $did
             mv *.png pic/slice/Ux/
             
             
             if [ ! -d "pic/slice/Uy" ]; then
             mkdir pic/slice/Uy
             fi
             
             python scripts/slice/Uy.py -s $start -e $end -d $did
             mv *.png pic/slice/Uy/
             
             
             if [ ! -d "pic/slice/Uz" ]; then
             mkdir pic/slice/Uz
             fi
             
             python scripts/slice/Uz.py -s $start -e $end -d $did
             mv *.png pic/slice/Uz/
             
             
             if [ ! -d "pic/slice/pressure" ]; then
             mkdir pic/slice/pressure
             fi
             
             python scripts/slice/pressure.py -s $start -e $end -d $did
             mv *.png pic/slice/pressure/
             
             
             if [ ! -d "pic/slice/Lorentz_factor" ]; then
             mkdir pic/slice/Lorentz_factor
             fi
             
             python scripts/slice/LorentzFactor.py -s $start -e $end -d $did
             mv *.png pic/slice/Lorentz_factor/
             
             if [ ! -d "pic/slice/temperature" ]; then
               mkdir pic/slice/temperature
             fi
             
             python scripts/slice/temperature.py -s $start -e $end -d $did
             mv *.png pic/slice/temperature/ ;;

        a)
############## projected conserved quanties  ##################
             
             if [ ! -d "pic/projection/number_density" ]; then
               mkdir pic/projection/number_density
             fi
             
             python scripts/slice/number_density.py -s $start -e $end -d $did
             mv *.png pic/projection/number_density/
             
             
             if [ ! -d "pic/projection/momentum_x" ]; then
               mkdir pic/projection/momentum_x
             fi
             
             python scripts/slice/MomX.py -s $start -e $end -d $did
             mv *.png pic/projection/momentum_x/
             
             
             if [ ! -d "pic/projection/momentum_y" ]; then
             mkdir pic/projection/momentum_y
             fi
             
             python scripts/slice/MomY.py -s $start -e $end -d $did
             mv *.png pic/projection/momentum_y/
             
             
             if [ ! -d "pic/projection/momentum_z" ]; then
             mkdir pic/projection/momentum_z
             fi
             
             python scripts/slice/MomZ.py -s $start -e $end -d $did
             mv *.png pic/projection/momentum_z/
             
             
             if [ ! -d "pic/projection/energy_density" ]; then
             mkdir pic/projection/energy_density
             fi
             
             python scripts/slice/energy.py -s $start -e $end -d $did
             mv *.png pic/projection/energy_density/ ;;
             
        b)
############## projected primitive quanties  ##################

             if [ ! -d "pic/projection/proper_number_density" ]; then
             mkdir pic/projection/proper_number_density
             fi
             
             python scripts/slice/proper_number_density.py -s $start -e $end -d $did
             mv *.png pic/projection/proper_number_density/
             
             
             if [ ! -d "pic/projection/Ux" ]; then
             mkdir pic/projection/Ux
             fi
             
             python scripts/slice/Ux.py -s $start -e $end -d $did
             mv *.png pic/projection/Ux/
             
             
             if [ ! -d "pic/projection/Uy" ]; then
             mkdir pic/projection/Uy
             fi
             
             python scripts/slice/Uy.py -s $start -e $end -d $did
             mv *.png pic/projection/Uy/
             
             
             if [ ! -d "pic/projection/Uz" ]; then
             mkdir pic/projection/Uz
             fi
             
             python scripts/slice/Uz.py -s $start -e $end -d $did
             mv *.png pic/projection/Uz/
             
             
             if [ ! -d "pic/projection/pressure" ]; then
             mkdir pic/projection/pressure
             fi
             
             python scripts/slice/pressure.py -s $start -e $end -d $did
             mv *.png pic/projection/pressure/
             
             
             if [ ! -d "pic/projection/Lorentz_factor" ]; then
             mkdir pic/projection/Lorentz_factor
             fi
             
             python scripts/slice/LorentzFactor.py -s $start -e $end -d $did
             mv *.png pic/projection/Lorentz_factor/
             
             if [ ! -d "pic/projection/temperature" ]; then
               mkdir pic/projection/temperature
             fi
             
             python scripts/slice/temperature.py -s $start -e $end -d $did
             mv *.png pic/projection/temperature/ ;;

        *)  usage ;;
    esac
done
shift $((OPTIND-1))
