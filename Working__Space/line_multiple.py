import yt
import numpy as np
import yt.visualization.eps_writer as eps
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from types import SimpleNamespace    
import sys
import os



import derived_field as df
import unit

def _Plot(Plot__Paramater, Input__TestProb):   

   n = SimpleNamespace(**Plot__Paramater)

   # Below lists have the same size as number of row:
   Field       = []               
   YAxisLabel  = []               
   norm        = []
                                  
   # Below lists have the same size as number of column:
   Title       = []
   NumPts      = []
   HeadX       = []
   HeadY       = []
   HeadZ       = []
   TailX       = []
   TailY       = []
   TailZ       = []

   # Below list has arbitrary size:
   DataName    = []
   Label       = []


   List     = [  DataName,  Label,   Field,   NumPts,   norm,   HeadX,   HeadY,   HeadZ,   TailX,   TailY,   TailZ,   Title ,  YAxisLabel ]
   ListName = [ "DataName","Label", "Field", "NumPts", "norm", "HeadX", "HeadY", "HeadZ", "TailX", "TailY", "TailZ", "Title", "YAxisLabel" ]


   for lstname, lst in zip(ListName, List):
     idx=0
     key = lstname+str("_00")
     while ( key in Plot__Paramater ):
       lst.append( Plot__Paramater[key] )
       idx=idx+1
       key = lstname+str("_%02d" % idx)

###################################################################

#  Head = [ [ HeadX_01, HeadY_01, HeadZ_01 ],
#           [ HeadX_02, HeadY_02, HeadZ_02 ],
#           [ HeadX_03, HeadY_03, HeadZ_03 ],
#           [ HeadX_04, HeadY_04, HeadZ_04 ] ]
#
#  Tail = [ [ TailX_01, TailY_01, TailZ_01 ],
#           [ TailX_02, TailY_02, TailZ_02 ],
#           [ TailX_03, TailY_03, TailZ_03 ],
#           [ TailX_04, TailY_04, TailZ_04 ] ]

   NumRay = len(HeadX)
   Head = []
   Tail = []
   for idx in range(NumRay):
     Head.append([])
     Tail.append([])
     Head[idx].append( HeadX[idx] )
     Head[idx].append( HeadY[idx] )
     Head[idx].append( HeadZ[idx] )
     Tail[idx].append( TailX[idx] )
     Tail[idx].append( TailY[idx] )
     Tail[idx].append( TailZ[idx] )

   # DataSet[DataName]          = [....]
   DataSet  = [yt.load(DataName[k]) for k in range(len(DataName))]

   BoxSizeX = DataSet[0]["BoxSize"][0]
   BoxSizeY = DataSet[0]["BoxSize"][1]
   BoxSizeZ = DataSet[0]["BoxSize"][2]

   # Ray can not lie on the surface or the edge of computational domain
   for i in range(NumRay):
     for j in range(3):
       if (Head[i][j] == 0 and Tail[i][j] == 0):
          print("error: Ray can not lie on the surface or edge of computational domain")
          exit(0)
       elif ( j==0 and Head[i][j] == BoxSizeX and Tail[i][j] == BoxSizeX ):
          print("error: Ray can not lie on the surface or edge of computational domain")
          exit(0)
       elif ( j==1 and Head[i][j] == BoxSizeY and Tail[i][j] == BoxSizeY ):
          print("error: Ray can not lie on the surface or edge of computational domain")
          exit(0)
       elif ( j==2 and Head[i][j] == BoxSizeZ and Tail[i][j] == BoxSizeZ ):
          print("error: Ray can not lie on the surface or edge of computational domain")
          exit(0)


   
   # Line[Field][Ray][DataName] = [....]
   Line     = []

   # !!! The second added derived field will overwrite the first one !!

   # add derived field
   for i in range(len(Field)):
       FieldFunction, Units = unit.ChooseUnit(Field[i])
       Line.append([])
       for j in range(NumRay):
           Line[i].append([])
           for k in range(len(DataName)):
              DataSet[k].add_field(("gamer", Field[i]), function=FieldFunction, sampling_type="cell", units=Units, force_override=True)
              Line[i][j].append ([])
              Line[i][j][k] = yt.LineBuffer( DataSet[k], Head[j], Tail[j], int(NumPts[j]) )

          
   for j in range(NumRay):
     Head[j] *= DataSet[j].length_unit

   # Dtermine the extreme y-values
   YMax = [sys.float_info.min]*len(Field)
   YMin = [sys.float_info.max]*len(Field)

   for i in range(len(Field)):
     for j in range(NumRay):
       for k in range(len(DataName)):
         YMax[i]=max(np.amax(Line[i][j][k][Field[i]]), YMax[i])
         YMin[i]=min(np.amin(Line[i][j][k][Field[i]]), YMin[i])


   # Matplolib
   #######################################################
   font = {'family': 'monospace','color': 'black', 'weight': 'heavy', 'size': 20}
   
   f, axs = plt.subplots( len(Field), NumRay, sharex=False, sharey=False )
   f.subplots_adjust( hspace=n.hspace, wspace=n.wspace )
   f.set_size_inches( 10.0, 16.0 )


   for i in range(len(Field)):
     for j in range(NumRay):
       for k in range(len(DataName)):
         Ray = np.sqrt( (Line[i][j][k]["x"]-Head[j][0])**2 + (Line[i][j][k]["y"]-Head[j][1])**2 + (Line[i][j][k]["z"]-Head[j][2])**2 )
         axs[i][j].plot( Ray, Line[i][j][k][Field[i]], label=Label[k] )

         axs[i][j].tick_params( which='both', direction='in', labelsize=12, top=False )

         axs[i][j].set_xlim(min(Ray), max(Ray))
         axs[i][j].set_ylim(YMin[i]/1.2,   YMax[i]*1.2)

         if norm[i] == 1:
           axs[i][j].set_yscale('log')
         if j==0:
          axs[i][j].set_ylabel(YAxisLabel[i], fontsize=16, fontweight='bold')

         # Removing tick labels must be after setting log scale;
         # otherwise tick labels emerge again
         if i < len(Field)-1:
           axs[i][j].get_xaxis().set_ticks([])
         if j > 0:
           axs[i][j].get_yaxis().set_ticks([])

         if i == 0:
           if ( Title[j] != 'off' ):
             if (Title[j] == 'auto'):
               title = "(%2.1f,%2.1f,%2.1f)\n(%2.1f,%2.1f,%2.1f)" % (Head[j][0], Head[j][1], Head[j][2], Tail[j][0], Tail[j][1], Tail[j][2])
               axs[i][j].set_title( title, fontdict=font )
             else:
               axs[i][j].set_title( Title[j], fontdict=font )

   # legend
   axs[0][0].legend(loc='upper center', fontsize=16)

   plt.show()
