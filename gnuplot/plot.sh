if [ ! -d "pic" ]; then
  mkdir pic
fi

if [ ! -d "pic/shk" ]; then
  mkdir pic/shk
fi

if [ ! -d "pic/blast" ]; then
  mkdir pic/blast
fi

if [ ! -d "pic/shk/number_density" ]; then
  mkdir pic/shk/number_density
fi
gnuplot plot_scripts/gnuplot/D.gpt
mv *.png pic/shk/number_density/

if [ ! -d "pic/shk/temperature" ]; then
  mkdir pic/shk/temperature
fi
gnuplot plot_scripts/gnuplot/Temp.gpt
mv *.png pic/shk/temperature/

if [ ! -d "pic/shk/momentum_x" ]; then
  mkdir pic/shk/momentum_x
fi
gnuplot plot_scripts/gnuplot/MomX.gpt
mv *.png pic/shk/momentum_x/

if [ ! -d "pic/shk/energy_density" ]; then
mkdir pic/shk/energy_density
fi
gnuplot plot_scripts/gnuplot/E.gpt
mv *.png pic/shk/energy_density/

if [ ! -d "pic/shk/proper_number_density" ]; then
mkdir pic/shk/proper_number_density
fi
gnuplot plot_scripts/gnuplot/n.gpt
mv *.png pic/shk/proper_number_density/

if [ ! -d "pic/shk/Ux" ]; then
mkdir pic/shk/Ux
fi
gnuplot plot_scripts/gnuplot/Ux.gpt
mv *.png pic/shk/Ux/

if [ ! -d "pic/shk/pressure" ]; then
mkdir pic/shk/pressure
fi
gnuplot plot_scripts/gnuplot/pres.gpt
mv *.png pic/shk/pressure/

if [ ! -d "pic/shk/Lorentz_factor" ]; then
mkdir pic/shk/Lorentz_factor
fi
gnuplot plot_scripts/gnuplot/LorentzFac.gpt
mv *.png pic/shk/Lorentz_factor/
