#!/bin/bash
if [ ! -d "../src" ]; then
     printf "We only lock source code\n"
else
     if [ ! -f "submit_hulk_openmpi-1.4.3.job" ]; then
      printf "Please copy your submit file into $PWD\n"
    else
      qsub ./submit_hulk_openmpi-1.4.3.job
      showq
      find                 ../include/ -type f  -name '*'         -exec chmod 400  {} \; 
      find                 ../example/ -type f  -name '*'         -exec chmod 400  {} \; 
      find                     ../src/ -type f  -name '*'         -exec chmod 400  {} \; 
      find                     ../doc/ -type f  -name '*'         -exec chmod 400  {} \; 
      find                    ../tool/ -type f  -name '*'         -exec chmod 400  {} \; 
      find ../test_problem_deprecated/ -type f  -name '*'         -exec chmod 400  {} \;
      find                           . -type f  -name 'Input__*'  -exec chmod 400  {} \; 
      

      find                 ../include/ -type f  -name '*.sh'      -exec chmod 740  {} \; 
      find                 ../example/ -type f  -name '*.sh'      -exec chmod 740  {} \; 
      find                     ../src/ -type f  -name '*.sh'      -exec chmod 740  {} \; 
      find                     ../doc/ -type f  -name '*.sh'      -exec chmod 740  {} \; 
      find                    ../tool/ -type f  -name '*.sh'      -exec chmod 740  {} \; 
      find ../test_problem_deprecated/ -type f  -name '*.sh'      -exec chmod 740  {} \; 
      find                         ../ -type f  -name 'gamer'     -exec chmod 740  {} \; 
    fi
fi

exit 1
