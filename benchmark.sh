#!/bin/bash

declare -a device=("gpu")
declare -a precision=("single" "double")
#declare -a numa=("PE" "SPAN" "OVERSUBSCRIBE" "NOOVERSUBSCRIBE")
declare -a numa=("PE")

cores=16

process=(2 4 8 16 32)
threads=(32 16 8 4 2 1)

#if [ -f summary.csv ]; then
# rm summary.csv
#fi
#
#printf '%s\n' device precision process "# of threads per process" "-map-by numa:" performance | paste -sd ',' >> summary.csv
####################### Process == 1 #################################
#
#   for d in "${device[@]}"
#do for p in "${precision[@]}"
#do for t in "${threads[@]}"
#do
#   t0=$( printf %02d ${t} )
#
#  if  (( "${t}" == 16 )) || (( "${t}" == 32 )); then
#        if [ -d "${d}.${p}.process_01.thread_${t0}" ]; then
#          cd     ${d}.${p}.process_01.thread_${t0}
#          rm -rf *
#        else
#          mkdir  ${d}.${p}.process_01.thread_${t0}
#          cd     ${d}.${p}.process_01.thread_${t0}
#        fi
#
#        ln -s ../bin/${d}.${p}.mpi_x/gamer .
#        
#        cp ../input/Input__* .
#        sed -i "s/^OMP_NTHREAD *.*/OMP_NTHREAD                   ${t}/" Input__Parameter
#        ln -s ../restart/${p}/RESTART .
#
#        ./gamer >& log &
#        echo "${d}, ${p}, process=01, thread=${t0} is running..."
#      
#        PID=$!
#        wait $PID
#        perf=`cat Record__Performance | awk 'FNR == 3 {print $7}'`
#        printf '%s\n' ${d} ${p} 1 ${t} - ${perf} | paste -sd ',' >> ../summary.csv
#        printf "Done!\n\n"
#        cd ../
#  fi
#
#done
#done
#done

###################### Process > 1 #################################

   for d in "${device[@]}"
do for p in "${precision[@]}"
do for n in "${process[@]}"
do for t in "${threads[@]}"
do for i in "${numa[@]}"
do
   nt=$(( n*t ))
   n0=$( printf %02d ${n} )
   t0=$( printf %02d ${t} )
  nt0=$( printf %02d ${nt} )


  if  (( "${nt}" == 16 )) || (( "${nt}" == 32 )); then
        if [ -d "${d}.${p}.process_${n0}.thread_${t0}.numa_${i}" ]; then
          cd     ${d}.${p}.process_${n0}.thread_${t0}.numa_${i}
          rm -rf *
        else
          mkdir  ${d}.${p}.process_${n0}.thread_${t0}.numa_${i}
          cd     ${d}.${p}.process_${n0}.thread_${t0}.numa_${i}
        fi

        ln -s ../bin/${d}.${p}.mpi_o/gamer .
        
        cp ../input/Input__* .
        sed -i "s/^OMP_NTHREAD *.*/OMP_NTHREAD                   ${t}/" Input__Parameter
        ln -s ../restart/${p}/RESTART .

        if [ ${i} == "PE" ] && (( "$((${cores}/${n}))" >= 1 )); then
          mpirun -np ${n} -map-by numa:pe=$((${cores}/${n})) --report-bindings  ./gamer >& log &
          echo "${d}, ${p}, process=${n0}, thread=${t0}, numa:pe=$((${cores}/${n})) is running..."
          PID=$!
          wait $PID
          perf=`cat Record__Performance | awk 'FNR == 3 {print $7}'`
          printf '%s\n' ${d} ${p} ${n} ${t} "pe=$((${cores}/${n}))" ${perf} | paste -sd ',' >> ../summary.csv
#        elif [ ${i} != "PE" ]; then
#          mpirun -np ${n} -map-by numa:${i} --report-bindings  ./gamer >& log &
#          echo "${d}, ${p}, process=${n0}, thread=${t0}, numa:${i} is running..."
#          PID=$!
#          wait $PID
#          perf=`cat Record__Performance | awk 'FNR == 3 {print $7}'`
#          printf '%s\n' ${d} ${p} ${n} ${t} ${i} ${perf} | paste -sd ',' >> ../summary.csv
        fi
      
        printf "Done!\n\n"
        cd ../
  fi

####################################################################

done
done
done
done
done
