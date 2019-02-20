#!/bin/bash

WorkPath="${PWD}"
GPU_ARCH=FERMI
thread_make=2
SRC="/home/gamer/Work/benchmark/src"
BIN="/home/gamer/Work/benchmark/bin"

MinThread=1
MaxThread=12

SubmitFile="submit_hulk_openMPI-1.4.3.job"

AppliedNode=1
AppliedThreadPerNode=6

declare -a DEVICE=("gpu")
declare -a MPI=("o" "x")
declare -a TIMING=("o" "x")
declare -a PRECISION=("single")
declare -a NUMA=("o")
declare -i PROCESS=(1 2) # number of processes per node
declare -i THREAD=()     # number of threads per process

for i in {${MinThread}..${MaxThread}}; do THREAD[$i]=$i; done

# check necessary files
if [ ! -f "${WorkPath}/${SubmitFile}" ]; then
  exit 1
fi

if [ ! -d "${WorkPath}/input" ]; then
  exit 1
fi

if [ ! -d "${WorkPath}/restart" ]; then
  exit 1
fi

mkdir bin

   for d in "${DEVICE[@]}"
do for m in "${MPI[@]}"
do for n in "${NUMA[@]}"
do for p in "${PRECISION[@]}"
do for t in "${TIMING[@]}"
do

#  make directories to store binary file
   if [ ! -d "${WorkPath}/bin" ];then
      mkdir bin
   fi

   if [ ! -d "${WorkPath}/bin/${d}.mpi_${m}.numa_${n}.${p}.timing_${t}" ];then
     mkdir -p ${WorkPath}/bin/${d}.mpi_${m}.numa_${n}.${p}.timing_${t}
   fi

#  modify Makefile
   if [ "${d}" = "gpu" ]; then 
     sed -i "s/^#*SIMU_OPTION *+= *-DGPU/SIMU_OPTION += -DGPU/"                                   ${SRC}/Makefile
     sed -i "s/^#*SIMU_OPTION *+= *-DGPU_ARCH=${GPU_ARCH}/SIMU_OPTION += -DGPU_ARCH=${GPU_ARCH}/" ${SRC}/Makefile
   else
     sed -i "s/^#*SIMU_OPTION *+= *-DGPU/#SIMU_OPTION += -DGPU/"                                   ${SRC}/Makefile
     sed -i "s/^#*SIMU_OPTION *+= *-DGPU_ARCH=${GPU_ARCH}/#SIMU_OPTION += -DGPU_ARCH=${GPU_ARCH}/" ${SRC}/Makefile
   fi

   if [ "${m}" = "o" ]; then 
     sed -i "s/^#*SIMU_OPTION *+= *-DSERIAL/#SIMU_OPTION += -DSERIAL/"                            ${SRC}/Makefile
     sed -i "s/^#*SIMU_OPTION *+= *-DLOAD_BALANCE=HILBERT/SIMU_OPTION += -DLOAD_BALANCE=HILBERT/" ${SRC}/Makefile
     sed -i "s/^#*CXX *= *icpc/#CXX         = icpc/"                                             ${SRC}/Makefile
     sed -i "s/^#*CXX *= *\$(MPI_PATH)\/bin\/mpicxx/CXX         = \$(MPI_PATH)\/bin\/mpicxx/"     ${SRC}/Makefile
   else
     sed -i "s/^#*SIMU_OPTION *+= *-DSERIAL/SIMU_OPTION += -DSERIAL/"                            ${SRC}/Makefile
     sed -i "s/^#*SIMU_OPTION *+= *-DLOAD_BALANCE=HILBERT/#SIMU_OPTION += -DLOAD_BALANCE=HILBERT/" ${SRC}/Makefile
     sed -i "s/^#*CXX *= *icpc/CXX         = icpc/"                                             ${SRC}/Makefile
     sed -i "s/^#*CXX *= *\$(MPI_PATH)\/bin\/mpicxx/#CXX         = \$(MPI_PATH)\/bin\/mpicxx/"     ${SRC}/Makefile
   fi

   if [ "${p}" = "single" ]; then 
     sed -i "s/^#*SIMU_OPTION *+= *-DFLOAT8/#SIMU_OPTION += -DFLOAT8/"                             ${SRC}/Makefile
   else
     sed -i "s/^#*SIMU_OPTION *+= *-DFLOAT8/SIMU_OPTION += -DFLOAT8/"                              ${SRC}/Makefile
   fi

   if [ "${t}" = "o" ]; then 
     sed -i "s/^#*SIMU_OPTION *+= *-DTIMING_SOLVER/#SIMU_OPTION += -DTIMING_SOLVER/"               ${SRC}/Makefile
   else
     sed -i "s/^#*SIMU_OPTION *+= *-DTIMING_SOLVER/SIMU_OPTION += -DTIMING_SOLVER/"                 ${SRC}/Makefile
   fi

#  compile
   cd ${SRC}
   make clean
   make -j ${thread_make} 

# move gamer to the corresponding directories
   mv ${BIN}/gamer ${WorkPath}/bin/${d}.mpi_${m}.numa_${n}.${p}.timing_${t}
   cd ${WorkPath}

done
done
done
done
done

# run on 1 node and 1 process!

if (( ${PROCESS[0]} == 1 )) && (( ${AppliedNode} == 1 ));then
  
     for d in "${DEVICE[@]}"
  do for n in "${NUMA[@]}"
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


# run processes >= 2 or node >=2
  
     for d in "${DEVICE[@]}"
  do for m in "${PROCESS[@]}"
  do for n in "${NUMA[@]}"
  do for p in "${PRECISION[@]}"
  do for t in "${TIMING[@]}"
  do

  if (( ${m} > 1 )) || (( ${AppliedNode} > 1 ));then

     M=$( printf %02d ${m} )                
     X=$( printf %02d ${ThreadPerProcess} )

     SubWorkPath=${d}.process_${M}.numa_${n}.${p}.timing_${t}.thread_pp_${X}
  
     if [ ! -d "${WorkPath}/${SubWorkPath}" ];then
       mkdir -p ${WorkPath}/${SubWorkPath}
     fi
       
     cp  ${WorkPath}/input/Input__* ${WorkPath}/${SubWorkPath}

     sed -i "s/^OMP_NTHREAD *.*/OMP_NTHREAD                   ${ThreadPerProcess}/" Input__Parameter

     ln -s ${WorkPath}/restart/${p}/RESTART ${WorkPath}
  
     cd ${WorkPath}/${SubWorkPath}

     sed -i "s/#PBS -l nodes=.*:ppn=.*/#PBS -l nodes=${AppliedNode}:ppn=${AppliedThreadPerNode}/"  ${SubmitFile}
     
     TotalProcess=$(( ${ProcessPerNode} * ${AppliedNode} ))

     sed -i "s/^mpirun/mpirun -np ${TotalProcess} -npernode ${ProcessPerNode} -hostfile \$PBS_NODEFILE -bind-to-socket ./gamer 1>>log 2>&1/"

     PID=$!

     wait ${PID}

     cd ${WorkPath}
  fi

  done
  done
  done
  done
  done

