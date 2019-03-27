DIR='/work1/Tseng/sr_hydro/gamer'
SRC='/work1/Tseng/sr_hydro/gamer/src'
SHK_INPUT='/example/test_problem/SR_Hydro/Riemann/*'
BLAST_INPUT='/example/test_problem/SR_Hydro/BlastWave/*'
TEST='/work1/Tseng/sr_hydro/gamer/bin'

SHK_NODE=3
BLAST_NODE=3

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

################# clean object files #################
##cd $SRC/src
##make clean
##cd $TEST
##
######################################################
################## get option ########################
######################################################
usage() { 
printf -- "Usage: $0\n" 
printf -- "-s  <rltvy/ideal>,<E/e>,<N steps>           shock tube test\n"
printf -- "-b  <rltvy/ideal>,<E/e>,<N steps>           blast waves test\n" 
exit 1; 
}
IFS=, # split on space characters



while getopts ":s:b:h" opt; do
    case "${opt}" in
       s ) 
       ####################################################
       ################ shock-tube test ###################
       ####################################################
              array=($OPTARG) # use the split+glob operator
              EOS=${array[0]}
              ENGY=${array[1]}
              STEP=${array[2]}

              # check parameters
              if [[ $EOS == "rltvy" ]]; then
                printf "\e[0;1;35;40mEquation of State: relativistic ideal EoS\e[0m\n"
                MACRO_EOS='RELATIVISTIC_IDEAL_GAS'
              elif [[ $EOS == "ideal" ]]; then
                printf "\e[0;1;35;40mEquation of State: classical ideal EoS\e[0m\n"
                MACRO_EOS='IDEAL_GAS'
              else
                printf "\e[0;1;35;40mYour EoS isn't supported yet!\e[0m\n"
                exit 1
              fi
              if [[ $ENGY == "E" ]]; then
              printf "\e[0;1;35;40mEnergy:                    total energy\e[0m\n"
              MACRO_ENGY='1'
              elif [[ $ENGY == "e" ]]; then
              printf "\e[0;1;35;40mEnergy: (total energy) - (rest mass energy)\e[0m\n"
              MACRO_ENGY='2'
              else
              printf "\e[0;1;35;40mYour energy isn't supported yet!\e[0m\n"
              exit 1
              fi
              if [[ $STEP > 0 ]]; then
              printf "\e[0;1;35;40mSteps: $STEP\e[0m\n"
              else
              printf "\e[0;1;35;40mStep should be greater than 0!\e[0m\n"
              exit 1
              fi

              printf "\n\e[0;1;35;40mMaking directories...\e[0m\n\n"


              if [ -d "${TEST}/pic" ]; then
                  while true; do
                      read -p "Do you wish to remove pic? (yes/no)" yn
                      case $yn in
                          [Yy]* ) rm -r ${TEST}/pic; mkdir ${TEST}/pic; break;;
                          [Nn]* ) break;;
                          * ) echo "Please answer yes or no.";;
                      esac
                  done
              else
                mkdir ${TEST}/pic
              fi
              
              if [ -d "${TEST}/shk" ]; then
                  while true; do
                      read -p "Do you wish to remove shk? (yes/no)" yn
                      case $yn in
                          [Yy]* ) rm -fr ${TEST}/shk;  mkdir ${TEST}/shk; break;;
                          [Nn]* ) break;;
                          * ) echo "Please answer yes or no.";;
                      esac
                  done
              else
                mkdir ${TEST}/shk
              fi
              
              if [ ! -d "${TEST}/shk/${EOS}_${ENGY}" ]; then
                mkdir "${TEST}/shk/${EOS}_${ENGY}"
              fi
              
              printf "\e[0;1;35;40mModifying Makefile...\e[0m\n\n"
              
              cp /work1/Tseng/data/submit_hulk_openmpi-1.4.3.job                                                  ${TEST}

              # Modify Makefile
              sed -i "s/^SIMU_OPTION += -DEOS=RELATIVISTIC_IDEAL_GAS/SIMU_OPTION += -DEOS=${MACRO_EOS}/"          ${SRC}/Makefile
              sed -i "s/^SIMU_OPTION += -DCONSERVED_ENERGY=1/SIMU_OPTION += -DCONSERVED_ENERGY=${MACRO_ENGY}/"    ${SRC}/Makefile
              # Modify submit script
              sed -i "s/^#PBS -N/#PBS -N shk\/${EOS}_${ENGY}/"                                                   ${TEST}/submit_hulk_openmpi-1.4.3.job
              sed -i "s/^#PBS -l nodes=:ppn=6/#PBS -l nodes=$SHK_NODE:ppn=6/"                                     ${TEST}/submit_hulk_openmpi-1.4.3.job
              sed -i "s/^mpirun -np/mpirun -np $((2*SHK_NODE))/"                                                  ${TEST}/submit_hulk_openmpi-1.4.3.job


              cp ${DIR}${SHK_INPUT}   $TEST
              # Modify Input__Parameter
              END_T=$( echo "0.00625"*"${STEP}"|bc)
              sed -i "s/^END_T *.*/END_T                      ${END_T}/"    $TEST/Input__Parameter
              sed -i "s/^END_STEP *.*/END_STEP                  $STEP/"     $TEST/Input__Parameter


              cd ${SRC}
              make -j 3
              cd ${TEST}
              ID=$( GetJobID qsub submit_hulk_openmpi-1.4.3.job )
              cd $TEST

              printf "\e[0;1;35;40mShock-tube test has been submitted! ID: $ID\e[0m\n\n"

              ####################################################
              ####################### Barrier ####################
              ####################################################
              printf "\e[0;1;35;40mWaitng for HULK...\e[0m\n\n"
              
              WaitForHULK $ID
              
              
              ####################################################
              ############### plot shock-tube ####################
              ####################################################
              printf "\e[0;1;35;40mPloting...\e[0m\n\n"
              
              sed -i "s/^do for \[i=0:.*\] {/do for \[i=0:$(($STEP))\] {/"      scripts/gnuplot/D.gpt
              sed -i "s/${TEST}\/shk\/.*\/bin/shk\/${EOS}_${ENGY}\/bin/"        scripts/gnuplot/D.gpt
              sed -i "s/{.*eos.*}/{\/=15${EOS}, ${ENGY}}/"                      scripts/gnuplot/D.gpt

              sed -i "s/^do for \[i=0:.*\] {/do for \[i=0:$(($STEP))\] {/"      scripts/gnuplot/E.gpt
              sed -i "s/${TEST}\/shk\/.*\/bin/shk\/${EOS}_${ENGY}\/bin/"        scripts/gnuplot/E.gpt
              sed -i "s/{.*eos.*}/{\/=15${EOS}, ${ENGY}}/"                      scripts/gnuplot/E.gpt

              sed -i "s/^do for \[i=0:.*\] {/do for \[i=0:$(($STEP))\] {/"      scripts/gnuplot/LorentzFac.gpt
              sed -i "s/${TEST}\/shk\/.*\/bin/shk\/${EOS}_${ENGY}\/bin/"        scripts/gnuplot/LorentzFac.gpt
              sed -i "s/{.*eos.*}/{\/=15${EOS}, ${ENGY}}/"                      scripts/gnuplot/LorentzFac.gpt

              sed -i "s/^do for \[i=0:.*\] {/do for \[i=0:$(($STEP))\] {/"      scripts/gnuplot/MomX.gpt
              sed -i "s/${TEST}\/shk\/.*\/bin/shk\/${EOS}_${ENGY}\/bin/"        scripts/gnuplot/MomX.gpt
              sed -i "s/{.*eos.*}/{\/=15${EOS}, ${ENGY}}/"                      scripts/gnuplot/MomX.gpt

              sed -i "s/^do for \[i=0:.*\] {/do for \[i=0:$(($STEP))\] {/"      scripts/gnuplot/n.gpt
              sed -i "s/${TEST}\/shk\/.*\/bin/shk\/${EOS}_${ENGY}\/bin/"        scripts/gnuplot/n.gpt
              sed -i "s/{.*eos.*}/{\/=15${EOS}, ${ENGY}}/"                      scripts/gnuplot/n.gpt

              sed -i "s/^do for \[i=0:.*\] {/do for \[i=0:$(($STEP))\] {/"      scripts/gnuplot/pres.gpt
              sed -i "s/${TEST}\/shk\/.*\/bin/shk\/${EOS}_${ENGY}\/bin/"        scripts/gnuplot/pres.gpt
              sed -i "s/{.*eos.*}/{\/=15${EOS}, ${ENGY}}/"                      scripts/gnuplot/pres.gpt

              sed -i "s/^do for \[i=0:.*\] {/do for \[i=0:$(($STEP))\] {/"      scripts/gnuplot/Temp.gpt
              sed -i "s/${TEST}\/shk\/.*\/bin/shk\/${EOS}_${ENGY}\/bin/"        scripts/gnuplot/Temp.gpt
              sed -i "s/{.*eos.*}/{\/=15${EOS}, ${ENGY}}/"                      scripts/gnuplot/Temp.gpt

              sed -i "s/^do for \[i=0:.*\] {/do for \[i=0:$(($STEP))\] {/"      scripts/gnuplot/Ux.gpt
              sed -i "s/${TEST}\/shk\/.*\/bin/shk\/${EOS}_${ENGY}\/bin/"        scripts/gnuplot/Ux.gpt
              sed -i "s/{.*eos.*}/{\/=15${EOS}, ${ENGY}}/"                      scripts/gnuplot/Ux.gpt
             
            
              if [ ! -d "${TEST}/pic/shk" ]; then
                mkdir ${TEST}/pic/shk
              fi
              if [[ ! -d "${TEST}/pic/shk/${EOS}_${ENGY}" ]]; then
                mkdir ${TEST}/pic/shk/${EOS}_${ENGY}
              fi
              
              if [[ ! -d "${TEST}/pic/shk/${EOS}_${ENGY}/number_density" ]]; then
                mkdir ${TEST}/pic/shk/${EOS}_${ENGY}/number_density
              fi
              gnuplot scripts/gnuplot/D.gpt
              mv *.png ${TEST}/pic/shk/${EOS}_${ENGY}/number_density/
              
              if [[ ! -d "${TEST}/pic/shk/${EOS}_${ENGY}/temperature" ]]; then
                mkdir ${TEST}/pic/shk/${EOS}_${ENGY}/temperature
              fi
              gnuplot scripts/gnuplot/Temp.gpt
              mv *.png ${TEST}/pic/shk/${EOS}_${ENGY}/temperature/
              
              if [[ ! -d "${TEST}/pic/shk/${EOS}_${ENGY}/momentum_x" ]]; then
                mkdir ${TEST}/pic/shk/${EOS}_${ENGY}/momentum_x
              fi
              gnuplot scripts/gnuplot/MomX.gpt
              mv *.png ${TEST}/pic/shk/${EOS}_${ENGY}/momentum_x/
              
              if [[ ! -d "${TEST}/pic/shk/${EOS}_${ENGY}/energy_density" ]]; then
              mkdir ${TEST}/pic/shk/${EOS}_${ENGY}/energy_density
              fi
              gnuplot scripts/gnuplot/E.gpt
              mv *.png ${TEST}/pic/shk/${EOS}_${ENGY}/energy_density/
              
              if [[ ! -d "${TEST}/pic/shk/${EOS}_${ENGY}/proper_number_density" ]]; then
              mkdir ${TEST}/pic/shk/${EOS}_${ENGY}/proper_number_density
              fi
              gnuplot scripts/gnuplot/n.gpt
              mv *.png ${TEST}/pic/shk/${EOS}_${ENGY}/proper_number_density/
              
              if [[ ! -d "${TEST}/pic/shk/${EOS}_${ENGY}/Ux" ]]; then
              mkdir ${TEST}/pic/shk/${EOS}_${ENGY}/Ux
              fi
              gnuplot scripts/gnuplot/Ux.gpt
              mv *.png ${TEST}/pic/shk/${EOS}_${ENGY}/Ux/
              
              if [[ ! -d "${TEST}/pic/shk/${EOS}_${ENGY}/pressure" ]]; then
              mkdir ${TEST}/pic/shk/${EOS}_${ENGY}/pressure
              fi
              gnuplot scripts/gnuplot/pres.gpt
              mv *.png ${TEST}/pic/shk/${EOS}_${ENGY}/pressure/
              
              if [[ ! -d "${TEST}/pic/shk/${EOS}_${ENGY}/Lorentz_factor" ]]; then
              mkdir ${TEST}/pic/shk/${EOS}_${ENGY}/Lorentz_factor
              fi
              gnuplot scripts/gnuplot/LorentzFac.gpt
              mv *.png ${TEST}/pic/shk/${EOS}_${ENGY}/Lorentz_factor/
 
              printf "\e[0;1;35;40mShock Tube Test Done!\e[0m\n\n"
              ;;
       b ) 
       ####################################################
       ################ blast waves test ##################
       ####################################################
              ;;
       * )   
              usage
              exit 1 ;;
    esac
done



####################################################
############### plot blast waves ###################
####################################################

#printf "\e[0;1;35;40mBlast Waves Test Done!\e[0m\n\n"
exit 0
