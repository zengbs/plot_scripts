#!/bin/bash

if [ -f "thread_vs_GCPUtiming.csv" ]; then
 rm thread_vs_GCPUtiming.csv
fi

for t in {32..1}
do

  t0=$( printf %02d ${t} )
  
  Flu_Pre=`cat gpu.timsol_o.thread_${t0}.numa_x/Record__Timing | awk 'FNR == 126 {print $2}'`
  Flu_Clo=`cat gpu.timsol_o.thread_${t0}.numa_x/Record__Timing | awk 'FNR == 126 {print $4}'`
 
  GPU=`cat gpu.timsol_o.thread_${t0}.numa_x/Record__Timing | awk 'FNR == 126 {print $3}'`
  CPU=`bc <<< "scale=4; $Flu_Pre+$Flu_Clo"`
 
  printf '%s\n' ${t} ${CPU} ${GPU}| paste -sd ' ' >> thread_vs_GCPUtiming.csv

done
