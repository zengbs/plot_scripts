#!/bin/bash

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

WorkPath="${PWD}"
SRC="/work1/Tseng/benchmark/src"
BIN="/work1/Tseng/benchmark/bin"
SHA1="1b57cac"


declare -a DEVICE=("gpu" "cpu")
declare -a OVERLAP=("o" "x")
declare -a PRECISION=("single" "double")
declare -a FMA=("o" "x")

# check necessary files
if [ ! -d "${WorkPath}/input" ]; then
  printf "No input file!\n"
  exit 1
fi


if [ ! -f "submit_gpu_openmpi-1.4.3.job" ]; then
  printf "No submit file!\n"
  exit 1
fi


if [ ! -d "${WorkPath}/bin" ];then
   mkdir $WorkPath/bin
fi
   for d in "${DEVICE[@]}"
do for f in "${FMA[@]}"
do for p in "${PRECISION[@]}"
do for t in "${OVERLAP[@]}"
do

   DIR="${SHA1}_${d}.overlap_${t}.${p}.fma_${f}"

   if [ ! -d "${WorkPath}/bin/${DIR}" ];then
    mkdir -p "${WorkPath}/bin/${DIR}"
   fi

#  modify Makefile
   if [ "${d}" = "gpu" ]; then 
     sed -i "s/^.*SIMU_OPTION *+= *-DGPU/SIMU_OPTION += -DGPU/"                                   ${SRC}/Makefile
     sed -i "s/^.*SIMU_OPTION *+= *-DSERIAL/#SIMU_OPTION += -DSERIAL/"                            ${SRC}/Makefile
     sed -i "s/^.*SIMU_OPTION *+= *-DLOAD_BALANCE=HILBERT/SIMU_OPTION += -DLOAD_BALANCE=HILBERT/"   ${SRC}/Makefile
   else
     sed -i "s/^#*SIMU_OPTION *+= *-DGPU/#SIMU_OPTION += -DGPU/"                                   ${SRC}/Makefile
     sed -i "s/^.*SIMU_OPTION *+= *-DSERIAL/SIMU_OPTION += -DSERIAL/"                            ${SRC}/Makefile
     sed -i "s/^.*SIMU_OPTION *+= *-DLOAD_BALANCE=HILBERT/#SIMU_OPTION += -DLOAD_BALANCE=HILBERT/"   ${SRC}/Makefile
   fi

   if [ "${p}" = "single" ]; then 
     sed -i "s/^#*SIMU_OPTION *+= *-DFLOAT8/#SIMU_OPTION += -DFLOAT8/"                             ${SRC}/Makefile
   else
     sed -i "s/^#*SIMU_OPTION *+= *-DFLOAT8/SIMU_OPTION += -DFLOAT8/"                              ${SRC}/Makefile
   fi

   if [ "${t}" = "x" ]; then 
     sed -i "s/^#*SIMU_OPTION *+= *-DTIMING_SOLVER/SIMU_OPTION += -DTIMING_SOLVER/"               ${SRC}/Makefile
   else
     sed -i "s/^#*SIMU_OPTION *+= *-DTIMING_SOLVER/#SIMU_OPTION += -DTIMING_SOLVER/"                ${SRC}/Makefile
   fi

   if [ "${f}" = "x" ]; then 
     sed -i "s/^#*SIMU_OPTION *+= *-DFUSED_MULTIPLY_ADD/#SIMU_OPTION += -DFUSED_MULTIPLY_ADD/"     ${SRC}/Makefile
   else
     sed -i "s/^#*SIMU_OPTION *+= *-DFUSED_MULTIPLY_ADD/SIMU_OPTION += -DFUSED_MULTIPLY_ADD/"      ${SRC}/Makefile
   fi

#  compile
   cd ${SRC}
   make clean
   make -j 3

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
do for t in "${OVERLAP[@]}"
do
        cd ${WorkPath}

        DIR="${SHA1}_${d}.overlap_${t}.${p}.fma_${f}"

        if [ -d "$DIR" ]; then
          cd    "$DIR"
          rm -rf *
        else
          mkdir  "$DIR"
          cd     "$DIR"
        fi


        ln -s "$WorkPath/bin/$DIR/gamer" "$WorkPath/$DIR"

        cp "${WorkPath}"/input/Input__* "$WorkPath/$DIR"
        cp "${WorkPath}"/submit_${d}_openmpi-1.4.3.job "$WorkPath/$DIR"

        if [ "${d}" = "gpu" ]; then 
          sed -i "s/^OMP_NTHREAD.*/OMP_NTHREAD                    3/"            $WorkPath/$DIR/Input__Parameter
          cp $WorkPath/submit_gpu_openmpi-1.4.3.job                                        $WorkPath/$DIR/
        else
          sed -i "s/^OMP_NTHREAD.*/OMP_NTHREAD                    6/"            $WorkPath/$DIR/Input__Parameter
          cp $WorkPath/submit_cpu_openmpi-1.4.3.job                                        $WorkPath/$DIR/
        fi

        cd $WorkPath/$DIR
        JobID=$( GetJobID qsub submit_${d}_openmpi-1.4.3.job )
        printf "${SubWorkPath} is running...\n"
        WaitForHULK $JobID


        cd ${WorkPath}

        printf "${d},overlap_${t}, ${p}, fma_${f} is running...\n"
        printf "Done!\n\n"
done
done
done
done
