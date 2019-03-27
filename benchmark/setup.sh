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
WorkPath="${PWD}"                    # working directory
NUMA=x
COMPILE=x                            #  o or x

###############################################################################
##amd
#SRC="/home/gamer/Work/benchmark/src" # source code to be compiled
#BIN="/home/gamer/Work/benchmark/bin" # binary file to be stored
#GPU_ARCH=PARSCAL
#compile_thread=32
#Machine=amd
#
#AppliedNode=1
#AppliedCoresPerNode=16 # real cores in CPU
#
#declare -i PROCESS=(1 2 4 8)
#MinProcess=${PROCESS[0]}                           # number of processes per node
#MaxProcess=${PROCESS[3]}                           # number of processes per node
#
#MinThread=1                                        # number of threads per process

###############################################################################
#hulk
GPU_ARCH=FERMI
SRC="/work1/Tseng/balance_test/src" # source code to be compiled
BIN="/work1/Tseng/balance_test/bin" # binary file to be stored
Machine=hulk
SubmitFile="submit_hulk_openmpi-1.4.3.job"
compile_thread=2 

AppliedNode=1
AppliedCoresPerNode=6 # real cores in CPU

declare -i PROCESS=(2)
MinProcess=${PROCESS[0]}                           # number of processes per node
MaxProcess=${PROCESS[1]}                           # number of processes per node

MinThread=1                                        # number of threads per process

###############################################################################



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
declare -i THREAD=()    

# Useful funtion

GetJobID()
{
  local stdout=`$@` # call the command and capture the stdout
  local id=`printf $stdout | awk -F. '{print $1}'` # get the jobid
  printf "$id"
}

WaitForHULK()
{
   shopt -s expand_aliases

   local sleep_time=1 # seconds; don't make this too short! don't want to tax system with excessive qstat calls

   #stdout=`$@` # call the command and capture the stdout
   #id=`printf $stdout | awk -F. '{print $1}'` # get the jobid

   local me=`whoami`
   local ID
   alias myqstat='qstat | grep $me'

   for ID in $@
   do
      local S=`myqstat | grep $ID | awk '{print $5}'` # check to see if job is running
	         while [[ "$S" == "R" || "$S" == "Q" ]] # while $status is runing or in qune
		 do
			 sleep $sleep_time
			 S=`myqstat | grep $ID | awk '{print $5}'`
		 done
       printf "\e[0;1;32;40mJob ID:$ID is done!\e[0m\n\n"
   done
}


# check necessary files
if [ "$Machine" = "hulk" ]; then
  if [ ! -f "${WorkPath}/${SubmitFile}" ]; then
    printf "No submit file!\n"
    exit 1
  fi
fi

if [ ! -d "${WorkPath}/input" ]; then
  printf "No input directory!\n"
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
  printf "No restart directory!\n"
  exit 1
fi

if [ "${COMPILE}" = "o" ];then
   
      for d in "${DEVICE[@]}"
   do for m in "${MPI[@]}"
   do for p in "${PRECISION[@]}"
   do for t in "${TIMING[@]}"
   do
   
   BinPath="${d}.mpi_${m}.${p}.timing_${t}"
   
   #  make directories to store binary file
      if [ ! -d "bin" ];then
         mkdir bin
      fi
   
      if [ ! -d "bin/${BinPath}" ] ; then
         mkdir  bin/${BinPath}
      else
         rm  bin/${BinPath}/*

      fi
   
   
   #  modify Makefile
      if [ "${d}" = "gpu" ]; then 
        sed -i "s/^.*SIMU_OPTION *+= *-DGPU/SIMU_OPTION += -DGPU/"                                   ${SRC}/Makefile
        sed -i "s/^.*SIMU_OPTION *+= *-DGPU_ARCH=${GPU_ARCH}/SIMU_OPTION += -DGPU_ARCH=${GPU_ARCH}/" ${SRC}/Makefile
      else
        sed -i "s/^.*SIMU_OPTION *+= *-DGPU/#SIMU_OPTION += -DGPU/"                                   ${SRC}/Makefile
        sed -i "s/^.*SIMU_OPTION *+= *-DGPU_ARCH=${GPU_ARCH}/#SIMU_OPTION += -DGPU_ARCH=${GPU_ARCH}/" ${SRC}/Makefile
      fi
   
      if [ "${m}" = "o" ]; then 
        sed -i "s/^.*SIMU_OPTION *+= *-DSERIAL/#SIMU_OPTION += -DSERIAL/"                            ${SRC}/Makefile
        sed -i "s/^.*SIMU_OPTION *+= *-DLOAD_BALANCE=HILBERT/SIMU_OPTION += -DLOAD_BALANCE=HILBERT/" ${SRC}/Makefile
        sed -i "s/^.*CXX *= *icpc/#CXX         = icpc/"                                             ${SRC}/Makefile
        sed -i "s/^.*CXX *= *\$(MPI_PATH)\/bin\/mpicxx/CXX         = \$(MPI_PATH)\/bin\/mpicxx/"     ${SRC}/Makefile
      else
        sed -i "s/^.*SIMU_OPTION *+= *-DSERIAL/SIMU_OPTION += -DSERIAL/"                            ${SRC}/Makefile
        sed -i "s/^.*SIMU_OPTION *+= *-DLOAD_BALANCE=HILBERT/#SIMU_OPTION += -DLOAD_BALANCE=HILBERT/" ${SRC}/Makefile
        sed -i "s/^.*CXX *= *icpc/CXX         = icpc/"                                             ${SRC}/Makefile
        sed -i "s/^.*CXX *= *\$(MPI_PATH)\/bin\/mpicxx/#CXX         = \$(MPI_PATH)\/bin\/mpicxx/"     ${SRC}/Makefile
      fi
   
      if [ "${p}" = "single" ]; then 
        sed -i "s/^.*SIMU_OPTION *+= *-DFLOAT8/#SIMU_OPTION += -DFLOAT8/"                             ${SRC}/Makefile
      else
        sed -i "s/^.*SIMU_OPTION *+= *-DFLOAT8/SIMU_OPTION += -DFLOAT8/"                              ${SRC}/Makefile
      fi
   
      if [ "${t}" = "o" ]; then 
        sed -i "s/^.*SIMU_OPTION *+= *-DTIMING_SOLVER/SIMU_OPTION += -DTIMING_SOLVER/"               ${SRC}/Makefile
      else
        sed -i "s/^.*SIMU_OPTION *+= *-DTIMING_SOLVER/#SIMU_OPTION += -DTIMING_SOLVER/"                 ${SRC}/Makefile
      fi
   
   #  compile
      cd ${SRC}
      make clean
      make -j ${compile_thread} 
   
   #  move gamer to the corresponding directories
      mv ${BIN}/gamer ${WorkPath}/bin/${d}.mpi_${m}.${p}.timing_${t}
      cd ${WorkPath}
   
   done
   done
   done
   done

fi
# run on 1 node and 1 process!

#if (( ${MinProcess} == 1 )) && (( ${AppliedNode} == 1 ));then
#
#if [ "$NUMA" = "o" ]; then
#  MaxThread=$AppliedCoresPerNode  # number of threads per process
#else
#  MaxThread=$((2*$AppliedCoresPerNode))  # number of threads per process
#fi
#
#for ((i=${MinThread};  i<=${MaxThread};  i++)); do  THREAD[$i]=$i; done
#  
#     for d in "${DEVICE[@]}"
#  do for p in "${PRECISION[@]}"
#  do for t in "${TIMING[@]}"
#  do for i in "${THREAD[@]}"
#  do
#
#     I=$( printf %02d ${i} )
#  
#     SubWorkPath=${d}.node_${AppliedNode}.process_01.thread_${I}.numa_${NUMA}.${p}.timing_${t}
#  
#     if [ ! -d "${SubWorkPath}" ];then
#       mkdir -p ${SubWorkPath}
#     else
#       rm -rf ${SubWorkPath}/*
#     fi
#
#     cd ${SubWorkPath}
#     
#     cp  ../input/Input__* .
#
#
#     ln -s ../restart/${p}/RESTART . 
#     ln -s ../bin/${d}.mpi_x.${p}.timing_${t}/gamer .
#
#     sed -i "s/^OMP_NTHREAD *.*/OMP_NTHREAD                   ${i}/" Input__Parameter
#
#     if [ "$Machine" = "hulk" ]; then
#       cp ../${SubmitFile} .
#       sed -i "s/^#PBS -l nodes=.*:ppn=.*/#PBS -l nodes=${AppliedNode}:ppn=${AppliedCoresPerNode}/"  ${SubmitFile}
#       sed -i "s/^mpirun.*/#mpirun/"  ${SubmitFile}
#       sed -i "s/^gamer.*/\.\/gamer 1>>log 2>\&1/"  ${SubmitFile}
#       JobID=$( GetJobID qsub submit_hulk_openmpi-1.4.3.job )
#       printf "${SubWorkPath} is running...\n"
#       WaitForHULK $JobID
#     elif [ "$Machine" = "amd" ]; then
#       ./gamer >& log &
#       PID=$!
#       printf "${SubWorkPath} is running...\n"
#       wait $PID
#     fi
#
#     cd ${WorkPath}
#  done
#  done
#  done
#  done
#
#else
# run processes >= 2 or node >=2
  
     for d in "${DEVICE[@]}"
  do for m in "${PROCESS[@]}"
  do for p in "${PRECISION[@]}"
  do for t in "${TIMING[@]}"
  do

  THREAD=()
  if [ "$NUMA" = "o" ]; then
    MaxThread=$((${AppliedCoresPerNode}/${m}))  # number of threads per process
  else
    MaxThread=$((2*$AppliedCoresPerNode/${m}))  # number of threads per process
  fi

  for ((i=${MinThread};  i<=${MaxThread};  i++)); do  THREAD[$i]=$i; done

     for j in "${THREAD[@]}"
   do

     TotalProcess=$(( ${m} * ${AppliedNode} ))

     M=$( printf %02d ${m} )                
     J=$( printf %02d ${j} )

     SubWorkPath=${d}.node_${AppliedNode}.process_${M}.thread_${J}.numa_${NUMA}.${p}.timing_${t}
  
     if [ ! -d "${SubWorkPath}" ];then
       mkdir -p ${SubWorkPath}
     else
       rm -rf ${SubWorkPath}/*
     fi

     cd ${SubWorkPath}
       
     cp  ../input/Input__* .



     ln -s ../restart/${p}/RESTART . 
     ln -s ../bin/${d}.mpi_o.${p}.timing_${t}/gamer .

     sed -i "s/^OMP_NTHREAD *.*/OMP_NTHREAD                   ${j}/" Input__Parameter
  
     if [ "$Machine" = "hulk" ]; then
       cp ../${SubmitFile} .
       sed -i "s/^#PBS -l nodes=.*:ppn=.*/#PBS -l nodes=${AppliedNode}:ppn=${AppliedCoresPerNode}/"  ${SubmitFile}
       sed -i "s/^.*gamer/#gamer/"  ${SubmitFile}
       sed -i "s/^mpirun.*/mpirun -np ${TotalProcess} -npernode ${m} -hostfile \$PBS_NODEFILE -bind-to-socket \.\/gamer 1>>log 2>\&1/"  ${SubmitFile}
       JobID=$( GetJobID qsub submit_hulk_openmpi-1.4.3.job )
       printf "${SubWorkPath} is running...\n"
       WaitForHULK $JobID
     elif [ "$Machine" = "amd" ]; then

       if [ "$NUMA" = "x" ]; then
          mpirun -np ${TotalProcess} ./gamer >& log &
       else
          mpirun -np ${TotalProcess}  --map-by numa:pe=${j}  ./gamer >& log &
       fi

       PID=$!
       printf "${SubWorkPath} is running...\n"
       wait $PID

     fi
     

     cd ${WorkPath}

  done
  done
  done
  done
  done

#fi
