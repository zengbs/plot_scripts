import yt                                                                                                        
import numpy as np
import matplotlib
import matplotlib.pyplot as plt 
import derived_field as df
import unit

FileName='AxesRatio'
Field = 'pressure_sr'
NumRow=1
NumCol=1
FieldFunction, Units = unit.ChooseUnit(Field)
NumPts = 4096
f, axs = plt.subplots( NumRow, NumCol, sharex=False, sharey=False )
f.subplots_adjust( hspace=0.1, wspace=0.1 )                                                         
f.set_size_inches( 10, 5 )
   

NormalizedConst_Pres = 1e6
NormalizedConst_Dens = 1.0

# Length of ray = 0.65
TailLonggest   = [32.0000000000000,32.0000000000000,32.0000000000000] 
HeadLonggest   = [32.4596194077713,31.5403805922287,32.0000000000000] 

TailShortest   = [32.0000000000000,32.0000000000000,32.0000000000000] 
HeadShortest   = [31.7346386111985,31.7346386111985,31.4692772223970]


RayLonggestAppend = [] 
RayShortestAppend = []
TimeAppend        = []
DataNameList      = []

Min=0
Max=4

for idx in range(Min,Max):

   DataName = 'Data_000'+('%03d' % idx)
   
   DataSet  = yt.load( DataName )

   if idx == Min:
     HeadLonggest *= DataSet.length_unit
     TailLonggest *= DataSet.length_unit
     HeadShortest *= DataSet.length_unit
     TailShortest *= DataSet.length_unit
   
   DataSet.add_field(("gamer", Field), function=FieldFunction, sampling_type="cell", units=Units, force_override=True)
   
   LineLonggest = yt.LineBuffer( DataSet, TailLonggest, HeadLonggest, NumPts )
   LineShortest = yt.LineBuffer( DataSet, TailShortest, HeadShortest, NumPts )
   
   RayLonggest = np.sqrt( (LineLonggest["x"]-TailLonggest[0])**2 + (LineLonggest["y"]-TailLonggest[1])**2 + (LineLonggest["z"]-TailLonggest[2])**2 )
   RayShortest = np.sqrt( (LineShortest["x"]-TailShortest[0])**2 + (LineShortest["y"]-TailShortest[1])**2 + (LineShortest["z"]-TailShortest[2])**2 )

   if idx == 0: 
     IdxShockLonggest = np.flatnonzero(LineLonggest[Field]>=1e-14)[-1]
     IdxShockShortest = np.flatnonzero(LineShortest[Field]>=1e-14)[-1]
   else:
     IdxShockLonggest = np.flatnonzero(LineLonggest[Field]>=1e-14)[-1]
     IdxShockShortest = np.flatnonzero(LineShortest[Field]>=1e-14)[-1]


   Time = DataSet["Time"][0]

   RayLonggestAppend.append( RayLonggest[IdxShockLonggest] )
   RayShortestAppend.append( RayShortest[IdxShockShortest] )
   TimeAppend.append( Time )
   DataNameList.append(idx)



for idx in DataNameList:
  print("%30.16e%30.16e%30.16e" % (TimeAppend[idx], abs(RayShortestAppend[idx]), abs(RayLonggestAppend[idx])))


print("Done !!")        
