SRC='/home/gamer02/Works/simd/src'
BIN='/home/gamer02/Works/simd/bin'


declare -a timesol=("o" "x")
declare -a simd=("o" "x")
declare -a optimize=("O2" "O3")

cd $BIN
rm -r simd* bin

    for t in "${timesol[@]}"
do  for s in "${simd[@]}"
do  for o in "${optimize[@]}"
do
      DIR="simd_${s}.timesol_${t}.opti_${o}"

      cp ../../Makefile $SRC

      if [ "${t}" = "o" ]; then 
        sed -i "s/^.*SIMU_OPTION *+= *-DTIMING_SOLVER/SIMU_OPTION += -DTIMING_SOLVER/"                  ${SRC}/Makefile
      else
        sed -i "s/^.*SIMU_OPTION *+= *-DTIMING_SOLVER/#SIMU_OPTION += -DTIMING_SOLVER/"                 ${SRC}/Makefile
      fi

      if [ "$s" = "o" ] && [ "$o" = "O2" ]; then
         sed -i "s/^ CXXFLAG     = -g -O2/#CXXFLAG     = -g -O2/"                                    ${SRC}/Makefile
         sed -i "s/^CXXFLAG     = -g -O3/#CXXFLAG     = -g -O3/"                                     ${SRC}/Makefile
         sed -i "s/^.*#.*pragma omp simd/#           pragma omp simd/"                                  $SRC/Main/Prepare_PatchData.cpp
      fi
                      
      if [ "$s" = "x" ] && [ "$o" = "O2" ]; then
         sed -i "s/^CXXFLAG     = -g -O2 -ftree-vectorize/#CXXFLAG     = -g -O2 -ftree-vectorize/"        ${SRC}/Makefile
         sed -i "s/^CXXFLAG     = -g -O3/#CXXFLAG     = -g -O3/"                                          ${SRC}/Makefile
         sed -i 's/^.*#.*pragma omp simd/\/\/#           pragma omp simd/'                                   $SRC/Main/Prepare_PatchData.cpp
      fi

      if [ "$o" = "O3" ]; then
         sed -i "s/^ CXXFLAG     = -g -O2/#CXXFLAG     = -g -O2/"                                         ${SRC}/Makefile
         sed -i "s/^CXXFLAG     = -g -O2 -ftree-vectorize/#CXXFLAG     = -g -O2 -ftree-vectorize/"        ${SRC}/Makefile
         sed -i "s/^.*#.*pragma omp simd/#           pragma omp simd/"                                       $SRC/Main/Prepare_PatchData.cpp
      fi

      cd $SRC
      make clean
      make -j

      cd $BIN
      mkdir -p bin/$DIR
      mv gamer bin/$DIR

      mkdir $DIR

      ln -s $BIN/RESTART $BIN/$DIR
      ln -s $BIN/Input__* $BIN/$DIR
      ln -s $BIN/bin/$DIR/gamer $DIR
      cp $SRC/Main/Prepare_PatchData.cpp $DIR
      cp $SRC/Makefile  $BIN/$DIR  

      cd $BIN/$DIR
      ./gamer >& log &
      wait $!
done
done
done
