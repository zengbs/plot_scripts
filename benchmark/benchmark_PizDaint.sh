#!/bin/bash

declare -a device=("gpu" "cpu")
declare -a timesol=("o" "x")
declare -a precision=("single" "double")
declare -a fma=("o x")



   for d in "${device[@]}"
do for f in "${fma[@]}"
do for p in "${precision[@]}"
do for t in "${timesol[@]}"
do
        if [ -d "${d}.timsol_${t}.${p}_.fma_${f}" ]; then
          cd     ${d}.timsol_${t}.${p}_.fma_${f}
#          rm -rf *
        else
          mkdir  ${d}.timsol_${t}.${p}_.fma_${f}
          cd     ${d}.timsol_${t}.${p}_.fma_${f}
        fi

        ln -s ../bin/${d}.timsol_${t}.${p}_.fma_${f}/gamer .
        
        cp ../input/Input__* .

        sbatch submit_daint.job

        cd ../

        printf "${d},timing solver_${t} , ${p} is running...\n"
        printf "Done!\n\n"
done
done
done
done
