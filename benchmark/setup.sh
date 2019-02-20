#!/bin/bash

# check necessary files
if [ ! -f "submit_hulk_openmpi-1.4.3.job" ]; then
  exit 1
fi

if [ ! -f "input/Input__.*" ]; then
  exit 1
fi

if [ ! -f "restart/single/RESTART" ]; then
  exit 1
fi



declare -a device=("gpu")
declare -a mpi=("o" "x")
declare -a timing_solver=("o" "x")
declare -a precision=("single")

declare -a numa=("o")

GPU_ARCH=FERMI
thread_make=32
SRC="/home/gamer/Work/benchmark/src"
BIN="/home/gamer/Work/benchmark/bin"
WorkPath="${PWD}"

MaxThread=32

mkdir bin

   for d in "${device[@]}"
do for m in "${mpi[@]}"
do for n in "${numa[@]}"
do for p in "${precision[@]}"
do for t in "${timing_solver[@]}"
do

#  make directories to store binary file
   if [ ! -d "${WorkPath}/bin" ];then
      mkdir bin
   fi

   if [ ! -d "${WorkPath}/bin/${d}.mpi_${m}.numa_${n}.${p}.timing_solver_${t}" ];then
     mkdir -p ${WorkPath}/bin/${d}.mpi_${m}.numa_${n}.${p}.timing_solver_${t}
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
   mv ${BIN}/gamer ${WorkPath}/bin/${d}.mpi_${m}.numa_${n}.${p}.timing_solver_${t}
   cd ${WorkPath}

done
done
done
done
done
