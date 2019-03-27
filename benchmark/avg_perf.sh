#!/bin/bash
FILE='/home/Tseng/Works/benchmark/PizDaint/weak_scaling/FMA_O/rank2048/Record__Performance'
START_LINE=66
END_LINE=70

OverallPerf=()
PerfPerRank=()
Step=()

# put overall performance value into array, OverallPerf[]
while IFS= read -r line; do
    OverallPerf+=( "$line" )
done < <( sed "${START_LINE},${END_LINE}!d"  ${FILE} | awk '{print $7}' )

# put performance per rank value into array, PerfPerRank[]
while IFS= read -r line; do
    PerfPerRank+=( "$line" )
done < <( sed "${START_LINE},${END_LINE}!d"  ${FILE} | awk '{print $8}' )

# put Step into array, Step[]
while IFS= read -r line; do
    Step+=( "$line" )
done < <( sed "${START_LINE},${END_LINE}!d"  ${FILE} | awk '{print $2}' )

printf '#%19s %20s %20s\n' Step Perf_Overall Perf_PerRank

for ((i=0;i<=${END_LINE}-${START_LINE};i++))
do
  printf '%20d %20.2e %20.2e\n' ${Step[$i]} ${OverallPerf[$i]} ${PerfPerRank[$i]}
done

printf '%60s\n' "#========================================================================="
printf '#%40s %20s\n' Avg_Perf_Overall Avg_Perf_PerRank

AVG_OverallPerf=0
AVG_PerfPerRank=0

# compute average
for ((i=0;i<=${END_LINE}-${START_LINE};i++))
do
  AVG_OverallPerf=`python -c "print ${AVG_OverallPerf}+${OverallPerf[$i]}"`
  AVG_PerfPerRank=`python -c "print ${AVG_PerfPerRank}+${PerfPerRank}"`
done

AVG_OverallPerf=`python -c "print ${AVG_OverallPerf}/(${END_LINE}-${START_LINE}+1)"`
AVG_PerfPerRank=`python -c "print ${AVG_PerfPerRank}/(${END_LINE}-${START_LINE}+1)"`

printf '%40.2e %40.2e\n' $AVG_OverallPerf  $AVG_PerfPerRank
