#!/bin/bash
#
# This program is used to find which files are missed
###################################################

for idx in {0..56}
do
 file=`printf "Data_%06d\n" $idx`

 if [[ ! -f "$file" ]];then
   printf "${file}\n"
 fi

done
