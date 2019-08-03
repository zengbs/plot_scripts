#!/bin/bash

PATH_1='cylindrical_radial_4velocity/'
FIELD_1='cylindrical_radial_4velocity'
CUT_AXIS_1='x'

HEAD_INDEX_1=0
TAIL_INDEX_1=9
HEAD_PLACE_1=49
TAIL_PLACE_1=49
##################################################

PATH_2='proper_number_density/'
FIELD_2='proper_number_density'
CUT_AXIS_2='x'

HEAD_PLACE_2=49
TAIL_PLACE_2=49

##################################################
PATH_3='pressure_sr/'
FIELD_3='pressure_sr'
CUT_AXIS_3='x'

HEAD_PLACE_3=49
TAIL_PLACE_3=49

##################################################

DH=0.5

OUTPUT='output3'

if [ ! -d "$OUTPUT" ]; then
  mkdir $OUTPUT
fi

if [[ $CUT_AXIS_1 != $CUT_AXIS_2 ]]; then
  
  for i in $( seq $HEAD_INDEX_1   1 $TAIL_INDEX_1 ); do
  for j in $( seq $HEAD_PLACE_1 $DH $TAIL_PLACE_1 ); do
  for k in $( seq $HEAD_PLACE_2 $DH $TAIL_PLACE_2 ); do
  
    INDEX_1=$(printf "Data_%06d" $i) 
    PLACE_1=$(printf "%08.3f"    $j)
    PLACE_2=$(printf "%08.3f"    $k)
   
    FILE_1=${INDEX_1}_${CUT_AXIS_1}_${PLACE_1}_Slice_${CUT_AXIS_1}_${FIELD_1}.png
    FILE_2=${INDEX_1}_${CUT_AXIS_2}_${PLACE_2}_Slice_${CUT_AXIS_2}_${FIELD_2}.png
  
    convert -trim ${PATH_1}${FILE_1} ${PATH_2}${FILE_2}  +append ${OUTPUT}/$(printf "%03d_%07.3f_%07.3f" $i $j $k).png
  
  done
  done
  done
  
else
  
  for i in $( seq $HEAD_INDEX_1   1 $TAIL_INDEX_1 ); do
  for j in $( seq $HEAD_PLACE_1 $DH $TAIL_PLACE_1 ); do
  
    INDEX_1=$(printf "Data_%06d" $i) 
    PLACE_1=$(printf "%08.3f"    $j)
    PLACE_2=$(printf "%08.3f"    $j)
   
    FILE_1=${INDEX_1}_${CUT_AXIS_1}_${PLACE_1}_Slice_${CUT_AXIS_1}_${FIELD_1}.png
    FILE_2=${INDEX_1}_${CUT_AXIS_2}_${PLACE_2}_Slice_${CUT_AXIS_2}_${FIELD_2}.png
  
    convert -trim ${PATH_1}${FILE_1} ${PATH_2}${FILE_2}  +append ${OUTPUT}/$(printf "%03d_%07.3f" $i $j ).png
  
  done
  done
  
fi
