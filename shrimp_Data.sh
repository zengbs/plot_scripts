#!/bin/bash
if (( $1 % 2 == 1 ))  
then
        for (( i=2 ; i < $1 ; i=i+2 )) do
          name=$(printf "Data_%06d" $i)
          rm -f "$name"
        done
else
        for (( i=1 ; i < $1 ; i=i+2 )) do
          name=$(printf "Data_%06d" $i)
          rm -f "$name"
        done
fi
