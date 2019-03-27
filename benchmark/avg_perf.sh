#!/bin/bash

NFILES=3
START_STEP=70
END_STEP=80

declare -a NODE=()

NODE[0]=64
NODE[1]=512
NODE[2]=2048

# if ( START_STEP < 1 ) then...
# if (END_STEP+1 > line) in file then ...
# if (START_STEP > END_STEP) then ...
# if (#NODE[] != #FILE[]) then...

declare -a FILES=()

FILES[0]='/home/Tseng/Works/benchmark/PizDaint/weak_scaling/FMA_O/rank0064/Record__Performance'
FILES[1]='/home/Tseng/Works/benchmark/PizDaint/weak_scaling/FMA_O/rank0512/Record__Performance'
FILES[2]='/home/Tseng/Works/benchmark/PizDaint/weak_scaling/FMA_O/rank2048/Record__Performance'

AVG_OverallPerf=()
AVG_PerfPerRank=()

START_LINE=$((START_STEP+1))
END_LINE=$((END_STEP+1))

for ((idx=0;idx<${NFILES};idx++))
do
   OverallPerf=()
   PerfPerRank=()

   # put overall performance into array, OverallPerf[]
   while IFS= read -r line; do
       OverallPerf+=( "$line" )
   done < <( sed "${START_LINE},${END_LINE}!d"  ${FILES[$idx]} | awk '{print $7}' )
   
   # put performance per rank into array, PerfPerRank[]
   while IFS= read -r line; do
       PerfPerRank+=( "$line" )
   done < <( sed "${START_LINE},${END_LINE}!d"  ${FILES[$idx]} | awk '{print $8}' )
   
   # compute average
   for ((i=0;i<=${END_LINE}-${START_LINE};i++))
   do
     AVG_OverallPerf[$idx]=`python -c "print ${AVG_OverallPerf[$idx]}+${OverallPerf[$i]}"`
     AVG_PerfPerRank[$idx]=`python -c "print ${AVG_PerfPerRank[$idx]}+${PerfPerRank[$i]}"`
   done

   AVG_OverallPerf[$idx]=`python -c "print ${AVG_OverallPerf[$idx]}/(${END_LINE}-${START_LINE}+1)"`
   AVG_PerfPerRank[$idx]=`python -c "print ${AVG_PerfPerRank[$idx]}/(${END_LINE}-${START_LINE}+1)"`
done

# print results
printf '#%19s%20s%20s%20s\n' "Number of Nodes" "Step Range" "AVG_Perf_Overall" "AVG_Perf_PerRank"
printf '%80s\n' "#========================================================================================"

for ((idx=0;idx<${NFILES};idx++))
do
  printf '%20d' ${NODE[$idx]}
  printf '%16d%s%3d' ${START_STEP} "-" ${END_STEP}
  printf '%20.2e%20.2e\n' ${AVG_OverallPerf[$idx]}  ${AVG_PerfPerRank[$idx]}
done

>& log
