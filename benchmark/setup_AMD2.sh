#!/bin/bash

WorkPath="${PWD}"
GPU_ARCH=PASCAL
SRC=""
BIN=""
SHA1=""


declare -a DEVICE=("gpu" "cpu")
declare -a OVERLAP=("o" "x")
declare -a PRECISION=("single" "double")
declare -a FMA=("o" "x")

# check necessary files
if [ ! -d "${WorkPath}/input" ]; then
  printf "No input file!\n"
  exit 1
fi

if [ ! -d "${WorkPath}/bin" ];then
   mkdir $WorkPath/bin
fi

   for d in "${DEVICE[@]}"
do for f in "${FMA[@]}"
do for p in "${PRECISION[@]}"
do for t in "${TIMING[@]}"
do

   DIR="${SHA1}_${d}.timsol_${t}.${p}.fma_${f}"

   if [ ! -d "${WorkPath}/bin/${DIR}" ];then
    mkdir -p "${WorkPath}/bin/${DIR}"
   fi

#  modify Makefile
   if [ "${d}" = "gpu" ]; then 
     sed -i "s/^#*SIMU_OPTION *+= *-DGPU/SIMU_OPTION += -DGPU/"                                   ${SRC}/Makefile
     sed -i "s/^#*SIMU_OPTION *+= *-DGPU_ARCH=${GPU_ARCH}/SIMU_OPTION += -DGPU_ARCH=${GPU_ARCH}/" ${SRC}/Makefile
   else
     sed -i "s/^#*SIMU_OPTION *+= *-DGPU/#SIMU_OPTION += -DGPU/"                                   ${SRC}/Makefile
     sed -i "s/^#*SIMU_OPTION *+= *-DGPU_ARCH=${GPU_ARCH}/#SIMU_OPTION += -DGPU_ARCH=${GPU_ARCH}/" ${SRC}/Makefile
   fi

   if [ "${p}" = "single" ]; then 
     sed -i "s/^#*SIMU_OPTION *+= *-DFLOAT8/#SIMU_OPTION += -DFLOAT8/"                             ${SRC}/Makefile
   else
     sed -i "s/^#*SIMU_OPTION *+= *-DFLOAT8/SIMU_OPTION += -DFLOAT8/"                              ${SRC}/Makefile
   fi

   if [ "${t}" = "x" ]; then 
     sed -i "s/^#*SIMU_OPTION *+= *-DTIMING_SOLVER/#SIMU_OPTION += -DTIMING_SOLVER/"               ${SRC}/Makefile
   else
     sed -i "s/^#*SIMU_OPTION *+= *-DTIMING_SOLVER/SIMU_OPTION += -DTIMING_SOLVER/"                ${SRC}/Makefile
   fi

   if [ "${f}" = "x" ]; then 
     sed -i "s/^#*SIMU_OPTION *+= *-DFUSED_MULTIPLY_ADD/#SIMU_OPTION += -DFUSED_MULTIPLY_ADD/"     ${SRC}/Makefile
   else
     sed -i "s/^#*SIMU_OPTION *+= *-DFUSED_MULTIPLY_ADD/SIMU_OPTION += -DFUSED_MULTIPLY_ADD/"      ${SRC}/Makefile
   fi

#  compile
   cd ${SRC}
   make clean
   make -j ${thread_make} 

# move binary and Makefile to the corresponding directories
   mv ${BIN}/gamer    "${WorkPath}/bin/${DIR}"
   cp ${SRC}/Makefile "${WorkPath}/bin/${DIR}"
   cd ${WorkPath}

done
done
done
done

######################### Run! ##############################
   for d in "${DEVICE[@]}"
do for f in "${FMA[@]}"
do for p in "${PRECISION[@]}"
do for t in "${TIMING[@]}"
do
        cd ${WorkPath}

        DIR="${SHA1}_${d}.timsol_${t}.${p}.fma_${f}"

        if [ -d "$DIR" ]; then
          cd    "$DIR"
#          rm -rf *
        else
          mkdir  "$DIR"
          cd     "$DIR"
        fi

        ln -s "$WorkPath/bin/$DIR/gamer" $WorkPath/$DIR

        cp $DIR/input/Input__* $DIR

        if [ "${d}" = "gpu" ]; then 
          sed -i "s/^OMP_NTHREAD.*/OMP_NTHREAD                    8/"            $WorkPath/${DIR}/Input__Parameter
          sed -i "s/^FLU_GPU_NPGROUP.*/FLU_GPU_NPGROUP              448/"        $WorkPath/${DIR}/Input__Parameter
        else
          sed -i "s/^OMP_NTHREAD.*/OMP_NTHREAD                   16/"            $WorkPath/${DIR}/Input__Parameter
          sed -i "s/^FLU_GPU_NPGROUP.*/FLU_GPU_NPGROUP              224/"        $WorkPath/${DIR}/Input__Parameter
        fi

        cp $SRC/Makefile $WorkPath/$DIR     

        mpirun -np 2 -map-by numa:pe=8 --report-bindings ./gamer >& log &
        wait $!        

        cd ${WorkPath}

        printf "${d},timing solver_${t}, ${p}, fma_${f} is running...\n"
        printf "Done!\n\n"
done
done
done
done
