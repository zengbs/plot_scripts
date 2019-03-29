#!/bin/bash

WorkPath="${PWD}"
GPU_ARCH=PASCAL
thread_make=4
SRC="/scratch/snx3000/ptseng/benchmark/src"
BIN="/scratch/snx3000/ptseng/benchmark/bin"

SubmitFile="submit_daint.job"


declare -a DEVICE=("gpu cpu")
declare -a TIMING=("o" "x")
declare -a PRECISION=("single double")
declare -a FMA=("o x")

# check necessary files
if [ ! -f "${WorkPath}/${SubmitFile}" ]; then
  printf "No submit file!\n"
  exit 1
fi


if [ ! -d "${WorkPath}/input" ]; then
  printf "No input file!\n"
fi

mkdir bin

   for d in "${DEVICE[@]}"
do for f in "${FMA[@]}"
do for p in "${PRECISION[@]}"
do for t in "${TIMING[@]}"
do

#  make directories to store binary file
   if [ ! -d "${WorkPath}/bin" ];then
      mkdir bin
   fi

   if [ ! -d "${WorkPath}/bin/${d}.timsol_${t}.${p}_.fma_${f}" ];then
     mkdir -p ${WorkPath}/bin/${d}.timsol_${t}.${p}_.fma_${f}
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

   if [ "${t}" = "o" ]; then 
     sed -i "s/^#*SIMU_OPTION *+= *-DTIMING_SOLVER/#SIMU_OPTION += -DTIMING_SOLVER/"               ${SRC}/Makefile
   else
     sed -i "s/^#*SIMU_OPTION *+= *-DTIMING_SOLVER/SIMU_OPTION += -DTIMING_SOLVER/"                ${SRC}/Makefile
   fi

   if [ "${f}" = "o" ]; then 
     sed -i "s/^#*SIMU_OPTION *+= *-DFUSED_MULTIPLY_ADD/#SIMU_OPTION += -DFUSED_MULTIPLY_ADD/"     ${SRC}/Makefile
   else
     sed -i "s/^#*SIMU_OPTION *+= *-DFUSED_MULTIPLY_ADD/SIMU_OPTION += -DFUSED_MULTIPLY_ADD/"      ${SRC}/Makefile
   fi

#  compile
   cd ${SRC}
   make clean
   make -j ${thread_make} 

# move gamer to the corresponding directories
   mv ${BIN}/gamer ${WorkPath}/bin/${d}.timsol_${t}.${p}_.fma_${f}
   cd ${WorkPath}

done
done
done
done

# run on 1 node and 1 process!

if (( ${PROCESS[0]} == 1 )) && (( ${AppliedNode} == 1 ));then
  
     for d in "${DEVICE[@]}"
  do for n in "${FMA[@]}"
  do for p in "${PRECISION[@]}"
  do for t in "${TIMING[@]}"
  do for i in "${THREAD[@]}"
  do

     I=$( printf %02d ${i} )
  
     SubWorkPath=${d}.process_01.numa_${n}.${p}.timing_${t}.thread_pp_${I}
  
     if [ ! -d "${WorkPath}/${SubWorkPath}" ];then
       mkdir -p ${WorkPath}/${SubWorkPath}
     fi
       
       cp  ${WorkPath}/input/Input__* ${WorkPath}/${SubWorkPath}
  
       sed -i "s/^OMP_NTHREAD *.*/OMP_NTHREAD                   ${i}/" Input__Parameter
  
       ln -s ${WorkPath}/restart/${p}/RESTART ${WorkPath}
    
       cd ${WorkPath}/${SubWorkPath}
  
       ./gamer >& log &
  
       PID=$!

       wait ${PID}
  
       cd ${WorkPath}
  done
  done
  done
  done
  done

fi



     for d in "${DEVICE[@]}"
  do for p in "${PRECISION[@]}"
  do for t in "${TIMING[@]}"
  do

     I=$( printf %02d ${i} )
  
     SubWorkPath=${d}.node_${AppliedNode}.process_01.thread_${I}.numa_${FMA}.${p}.timing_${t}
  
     if [ ! -d "${SubWorkPath}" ];then
       mkdir -p ${SubWorkPath}
     else
#       rm -rf ${SubWorkPath}/*
     fi

     cd ${SubWorkPath}
     
     cp  ../input/Input__* .


     ln -s ../restart/${p}/RESTART . 
     ln -s ../bin/${d}.mpi_x.${p}.timing_${t}/gamer .

     sed -i "s/^OMP_NTHREAD *.*/OMP_NTHREAD                   ${i}/" Input__Parameter

     if [ "$Machine" = "hulk" ]; then
       cp ../${SubmitFile} .
       sed -i "s/^#PBS -l nodes=.*:ppn=.*/#PBS -l nodes=${AppliedNode}:ppn=${AppliedCoresPerNode}/"  ${SubmitFile}
       sed -i "s/^mpirun.*/#mpirun/"  ${SubmitFile}
       sed -i "s/^gamer.*/\.\/gamer 1>>log 2>\&1/"  ${SubmitFile}
       JobID=$( GetJobID qsub submit_hulk_openmpi-1.4.3.job )
       printf "${SubWorkPath} is running...\n"
       WaitForHULK $JobID
     elif [ "$Machine" = "amd" ]; then
       ./gamer >& log &
       PID=$!
       printf "${SubWorkPath} is running...\n"
       wait $PID
     fi

     cd ${WorkPath}
  done
  done
  done
