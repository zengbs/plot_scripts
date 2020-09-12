#!/bin/bash


# Once the job `JobID` complete, submit new job immediately.

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


JobID=$1

WaitForHULK $JobID

qsub submit.job

exit
