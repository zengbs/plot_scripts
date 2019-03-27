#!/bin/bash

if [ -f "thread_vs_perf.csv" ]; then
 rm thread_vs_perf.csv
fi

for t in {12..1}
do

  t0=$( printf %02d ${t} )
  
  perf=`cat gpu.timsol_x.thread_${t0}.numa_x/Record__Performance | awk 'FNR == 3 {print $7}'`
  
  printf '%s\n' ${t} ${perf} | paste -sd ' ' >> thread_vs_perf.csv

done
