#!/bin/bash

declare -a NODE=()
declare -a GPU=()

################ INPUT AREA ###################################

NFILES=4
START_STEP=61
END_STEP=71


NODE[0]=1
NODE[1]=8
NODE[2]=64
NODE[3]=512

GPU[0]=1
GPU[1]=8
GPU[2]=64
GPU[3]=512

declare -a FILES=()

FILES[0]='rank0001/Record__Performance'
FILES[1]='rank0008/Record__Performance'
FILES[2]='rank0064/Record__Performance'
FILES[3]='rank0512/Record__Performance'

START_LINE=
END_LINE=

################################################################

# if ( START_STEP < 1 ) then...
# if (END_STEP+1 > line) in file then ...
# if (START_STEP > END_STEP) then ...
# if (#NODE[] != #FILE[]) then...

AVG_OverallPerf=()
AVG_PerfPerRank=()


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
printf '#%19s%3d%s%3d%6s\n' "Avg_Range: " ${START_STEP} "-" ${END_STEP} "Steps"
printf '#%19s%20s%20s%20s\n' "Number_of_Nodes" "Number_of_GPUs" "AVG_Perf_Overall" "AVG_Perf_PerRank"
printf '#%80s\n' "========================================================================================"

for ((idx=0;idx<${NFILES};idx++))
do
  printf '%20d%20d' ${NODE[$idx]} ${GPU[$idx]}
  printf '%20.2e%20.2e\n' ${AVG_OverallPerf[$idx]}  ${AVG_PerfPerRank[$idx]}
done
