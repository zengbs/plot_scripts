#!/bin/bash
for ((i=0;i<=20;i=i+1)) do
 name=$(printf %06d ${i} )
 convert x_slice/Data_${name}_*.png z_slice/Data_${name}_*.png +append ${name}.png
done
