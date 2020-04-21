for i in {0..23};
do
  Name=`printf "c%02d" $i`
  cd $Name
  File=`ls -lrth Data_?????? | tail -n 1 | awk '{print $9}'`
  printf "DataName_%02d           $PWD/$File\n" $i
  cd ..
done


for i in {0..23};
do
  printf "Title_%02d             c%02d\n" $i  $i
done

for i in {0..23};
do
   printf "CutAxis_%02d                       z\n"  $i  
   printf "Coord_%02d                       150\n"  $i
   printf "Xmax_%02d                        300\n"  $i
   printf "Xmin_%02d                          0\n"  $i
   printf "Ymax_%02d                        300\n"  $i
   printf "Ymin_%02d                          0\n\n"  $i
done
