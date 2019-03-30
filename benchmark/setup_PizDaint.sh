#!/bin/bash

WorkPath="${PWD}"
GPU_ARCH=PASCAL
thread_make=4
SRC="/scratch/snx3000/ptseng/fma_precision/src"
BIN="/scratch/snx3000/ptseng/fma_precision/bin"

SubmitFile="submit_daint.job"


declare -a DEVICE=("gpu" "cpu")
declare -a TIMING=("o" "x")
declare -a PRECISION=("single" "double")
declare -a FMA=("o" "x")

# check necessary files
if [ ! -f "${WorkPath}/${SubmitFile}" ]; then
  printf "No submit file!\n"
  exit 1
fi


if [ ! -d "${WorkPath}/input" ]; then
  printf "No input file!\n"
  exit 1
fi

if [ ! -d "${WorkPath}/bin" ];then
   mkdir bin
fi

#   for d in "${DEVICE[@]}"
#do for f in "${FMA[@]}"
#do for p in "${PRECISION[@]}"
#do for t in "${TIMING[@]}"
#do
#
#   if [ ! -d "${WorkPath}/bin/${d}.timsol_${t}.${p}.fma_${f}" ];then
#    mkdir -p "${WorkPath}/bin/${d}.timsol_${t}.${p}.fma_${f}"
#   fi
#
##  modify Makefile
#   if [ "${d}" = "gpu" ]; then 
#     sed -i "s/^#*SIMU_OPTION *+= *-DGPU/SIMU_OPTION += -DGPU/"                                   ${SRC}/Makefile
#     sed -i "s/^#*SIMU_OPTION *+= *-DGPU_ARCH=${GPU_ARCH}/SIMU_OPTION += -DGPU_ARCH=${GPU_ARCH}/" ${SRC}/Makefile
#   else
#     sed -i "s/^#*SIMU_OPTION *+= *-DGPU/#SIMU_OPTION += -DGPU/"                                   ${SRC}/Makefile
#     sed -i "s/^#*SIMU_OPTION *+= *-DGPU_ARCH=${GPU_ARCH}/#SIMU_OPTION += -DGPU_ARCH=${GPU_ARCH}/" ${SRC}/Makefile
#   fi
#
#   if [ "${p}" = "single" ]; then 
#     sed -i "s/^#*SIMU_OPTION *+= *-DFLOAT8/#SIMU_OPTION += -DFLOAT8/"                             ${SRC}/Makefile
#     sed -i "s/^FLU_GPU_NPGROUP *224/FLU_GPU_NPGROUP              448/"                               ${WorkPath}/input/Input__Parameter
#   else
#     sed -i "s/^#*SIMU_OPTION *+= *-DFLOAT8/SIMU_OPTION += -DFLOAT8/"                              ${SRC}/Makefile
#     sed -i "s/^FLU_GPU_NPGROUP *224/FLU_GPU_NPGROUP              224/"                               ${WorkPath}/input/Input__Parameter
#   fi
#
#   if [ "${t}" = "x" ]; then 
#     sed -i "s/^#*SIMU_OPTION *+= *-DTIMING_SOLVER/#SIMU_OPTION += -DTIMING_SOLVER/"               ${SRC}/Makefile
#   else
#     sed -i "s/^#*SIMU_OPTION *+= *-DTIMING_SOLVER/SIMU_OPTION += -DTIMING_SOLVER/"                ${SRC}/Makefile
#   fi
#
#   if [ "${f}" = "x" ]; then 
#     sed -i "s/^#*SIMU_OPTION *+= *-DFUSED_MULTIPLY_ADD/#SIMU_OPTION += -DFUSED_MULTIPLY_ADD/"     ${SRC}/Makefile
#   else
#     sed -i "s/^#*SIMU_OPTION *+= *-DFUSED_MULTIPLY_ADD/SIMU_OPTION += -DFUSED_MULTIPLY_ADD/"      ${SRC}/Makefile
#   fi
#
##  compile
#   cd ${SRC}
#   make clean
#   make -j ${thread_make} 
#
## move gamer to the corresponding directories
#   mv ${BIN}/gamer    "${WorkPath}/bin/${d}.timsol_${t}.${p}.fma_${f}"
#   cp ${SRC}/Makefile "${WorkPath}/bin/${d}.timsol_${t}.${p}.fma_${f}"
#   cd ${WorkPath}
#
#done
#done
#done
#done

######################### Run! ##############################
   for d in "${DEVICE[@]}"
do for f in "${FMA[@]}"
do for p in "${PRECISION[@]}"
do for t in "${TIMING[@]}"
do
        if [ -d "${d}.timsol_${t}.${p}.fma_${f}" ]; then
          cd    "${d}.timsol_${t}.${p}.fma_${f}"
          rm -rf *
        else
          mkdir  "${d}.timsol_${t}.${p}.fma_${f}"
          cd     "${d}.timsol_${t}.${p}.fma_${f}"
        fi

        ln -s "../bin/${d}.timsol_${t}.${p}.fma_${f}/gamer" .


   if [ "${p}" = "single" ]; then 
     sed -i "s/^FLU_GPU_NPGROUP.*/FLU_GPU_NPGROUP              448/"                               ${WorkPath}/input/Input__Parameter
   else
     sed -i "s/^FLU_GPU_NPGROUP.*/FLU_GPU_NPGROUP              224/"                               ${WorkPath}/input/Input__Parameter
   fi
        cp ../input/Input__* .
    
        cp ../submit_daint.job .
        sbatch submit_daint.job

        cd ../ 

        printf "${d},timing solver_${t}, ${p}, fma_${f} is running...\n"
        printf "Done!\n\n"
done
done
done
done
