#!/bin/bash

#FILE1='Data_000037_x_0030.000_Slice_x_proper_number_density.png'
#FILE2='Data_000041_z_0020.000_Slice_z_proper_number_density.png'

PATH_1='proper_number_density/cut_z_20/'
FIELD_1='proper_number_density'
CUT_AXIS_1='z'

HEAD_INDEX_1=22
TAIL_INDEX_1=52
HEAD_PLACE_1=20
TAIL_PLACE_1=20


PATH_2='proper_number_density/cut_x_30/'
FIELD_2='proper_number_density'
CUT_AXIS_2='x'

HEAD_PLACE_2=30
TAIL_PLACE_2=30

DH=1.0

OUTPUT='output'

if [ ! -d "$OUTPUT" ]; then
  mkdir $OUTPUT
fi

for i in $( seq $HEAD_INDEX_1   1 $TAIL_INDEX_1 ); do
for k in $( seq $HEAD_PLACE_1 $DH $TAIL_PLACE_1 ); do

for n in $( seq $HEAD_PLACE_2 $DH $TAIL_PLACE_2 ); do

  INDEX_1=$(printf "Data_%06d" $i) 
  PLACE_1=$(printf "%08.3f"    $k)

  PLACE_2=$(printf "%08.3f"    $n)
 
  FILE_1=${INDEX_1}_${CUT_AXIS_1}_${PLACE_1}_Slice_${CUT_AXIS_1}_${FIELD_1}.png
  FILE_2=${INDEX_1}_${CUT_AXIS_2}_${PLACE_2}_Slice_${CUT_AXIS_2}_${FIELD_2}.png
  
  convert -trim ${PATH_1}${FILE_1} ${OUTPUT}/${i}_1.temp
  convert -trim ${PATH_2}${FILE_2} ${OUTPUT}/${i}_2.temp

  convert ${OUTPUT}/${i}_2.temp ${OUTPUT}/${i}_1.temp -append ${OUTPUT}/$(printf "%03d" $i).png
 
  rm ${OUTPUT}/*.temp

done
done
done
