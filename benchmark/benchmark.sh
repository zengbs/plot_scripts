#!/bin/bash

#declare -a mpi=("o" "x")
declare -a device=("gpu")
declare -a timesol=("o" "x")
declare -a precision=("single" "double")
declare -a numa=("x")

cores=16

#process=(2 4 8 16 32)
#threads=(32 31 30 29 28 27 26 25 24  16 10 9 8 7 6)

if [ -f summary.csv ]; then
 rm summary.csv
fi

#printf '%s\n' device timesol threads performance | paste -sd ',' >> summary.csv
###################### Process == 1 #################################

   for d in "${device[@]}"
do for s in "${timesol[@]}"
do for t in {32..1}
do for n in "${numa[@]}"
do
   t0=$( printf %02d ${t} )

#  if  (( "${t}" == 16 )) || (( "${t}" == 32 )); then
        if [ -d "${d}.timsol_${s}.thread_${t0}.numa_${n}" ]; then
          cd     ${d}.timsol_${s}.thread_${t0}.numa_${n}
          rm -rf *
        else
          mkdir  ${d}.timsol_${s}.thread_${t0}.numa_${n}
          cd     ${d}.timsol_${s}.thread_${t0}.numa_${n}
        fi

        ln -s ../bin/${d}.single.mpi_x.timesol_${s}/gamer .
        
        cp ../input/Input__* .
        sed -i "s/^OMP_NTHREAD *.*/OMP_NTHREAD                   ${t}/" Input__Parameter
        ln -s ../restart/single/RESTART .

        ./gamer >& log &
        echo "${d},timing solver_${s} , thread=${t} is running..."
      
        PID=$!
        wait $PID
#        perf=`cat Record__Performance | awk 'FNR == 3 {print $7}'`
#        printf '%s\n' ${d} ${p} 1 ${t} - ${perf} | paste -sd ',' >> ../summary.csv
        printf "Done!\n\n"
        cd ../
#  fi

done
done
done
done

###################### Process > 1 #################################
#
#   for d in "${device[@]}"
#do for p in "${precision[@]}"
#do for n in "${process[@]}"
#do for t in "${threads[@]}"
#do for i in "${numa[@]}"
#do
#   nt=$(( n*t ))
#   n0=$( printf %02d ${n} )
#   t0=$( printf %02d ${t} )
#  nt0=$( printf %02d ${nt} )
#
#
#  if  (( "${nt}" == 16 )) || (( "${nt}" == 32 )); then
#        if [ -d "${d}.${p}.process_${n0}.thread_${t0}.numa_${i}" ]; then
#          cd     ${d}.${p}.process_${n0}.thread_${t0}.numa_${i}
#          rm -rf *
#        else
#          mkdir  ${d}.${p}.process_${n0}.thread_${t0}.numa_${i}
#          cd     ${d}.${p}.process_${n0}.thread_${t0}.numa_${i}
#        fi
#
#        ln -s ../bin/${d}.${p}.mpi_o/gamer .
#        
#        cp ../input/Input__* .
#        sed -i "s/^OMP_NTHREAD *.*/OMP_NTHREAD                   ${t}/" Input__Parameter
#        ln -s ../restart/${p}/RESTART .
#
#        if [ ${i} == "PE" ] && (( "$((${cores}/${n}))" >= 1 )); then
#          mpirun -np ${n} -map-by numa:pe=$((${cores}/${n})) --report-bindings  ./gamer >& log &
#          echo "${d}, ${p}, process=${n0}, thread=${t0}, numa:pe=$((${cores}/${n})) is running..."
#          PID=$!
#          wait $PID
#          perf=`cat Record__Performance | awk 'FNR == 3 {print $7}'`
#          printf '%s\n' ${d} ${p} ${n} ${t} "pe=$((${cores}/${n}))" ${perf} | paste -sd ',' >> ../summary.csv
#        elif [ ${i} != "PE" ]; then
#          mpirun -np ${n} -map-by numa:${i} --report-bindings  ./gamer >& log &
#          echo "${d}, ${p}, process=${n0}, thread=${t0}, numa:${i} is running..."
#          PID=$!
#          wait $PID
#          perf=`cat Record__Performance | awk 'FNR == 3 {print $7}'`
#          printf '%s\n' ${d} ${p} ${n} ${t} ${i} ${perf} | paste -sd ',' >> ../summary.csv
#        fi
#      
#        printf "Done!\n\n"
#        cd ../
#  fi
#
#####################################################################
#
#done
#done
#done
#done
#done
