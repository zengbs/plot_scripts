import yt
import numpy as np
import yt.visualization.eps_writer as eps
import matplotlib
import matplotlib.pyplot as plt
from types import SimpleNamespace    
import sys



import derived_field as df
import unit

def _Plot(Plot__Paramater, Input__TestProb):   

   n = SimpleNamespace(**Plot__Paramater)

   # Below lists have the same size as number of row:
   Field       = []               
   YAxisLabel  = []               
   norm        = []
   Ymax        = []
   Ymin        = []
                                  
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
   Mark        = []
   MarkSize    = []


   List     = [  DataName,  Label,   Field,   NumPts,   norm,   HeadX,   HeadY,   HeadZ,   TailX,   TailY,   TailZ,   Title ,  YAxisLabel ,  Ymax,   Ymin  ,  Mark,   MarkSize  ]
   ListName = [ "DataName","Label", "Field", "NumPts", "norm", "HeadX", "HeadY", "HeadZ", "TailX", "TailY", "TailZ", "Title", "YAxisLabel", "Ymax", "Ymin" , "Mark", "MarkSize" ]


   for lstname, lst in zip(ListName, List):
     idx=0
     key = lstname+str("_00")
     while ( key in Plot__Paramater ):
       lst.append( Plot__Paramater[key] )
       idx=idx+1
       key = lstname+str("_%02d" % idx)

###################################################################
   NumRow = int(n.NumRow)
   NumCol = int(n.NumCol)

# check 
   Exit = False

   if ( len(Field) != NumRow ):
     print("len(Field) != %d" % (NumRow))
     Exit = True
   if ( len(YAxisLabel) != NumRow ):
     print("len(YAxisLabel) != %d" % (NumRow))
     Exit = True
   if ( len(YAxisLabel) != NumRow ):
     print("len(YAxisLabel) != %d" % (NumRow))
     Exit = True
   if ( len(norm) != NumRow ):
     print("len(norm) != %d" % (NumRow))
     Exit = True
   if ( len(Ymax) != NumRow ):
     print("len(Ymax) != %d" % (NumRow))
     Exit = True
   if ( len(Ymin) != NumRow ):
     print("len(Ymin) != %d" % (NumRow))
     Exit = True

   if ( len(Title) != NumCol ):
     print("len(Title) != %d" % (NumCol))
     Exit = True
   if ( len(NumPts) != NumCol ):
     print("len(NumPts) != %d" % (NumCol))
     Exit = True
   if ( len(HeadX) != NumCol ):
     print("len(HeadX) != %d" % (NumCol))
     Exit = True
   if ( len(HeadY) != NumCol ):
     print("len(HeadY) != %d" % (NumCol))
     Exit = True
   if ( len(HeadZ) != NumCol ):
     print("len(HeadZ) != %d" % (NumCol))
     Exit = True
   if ( len(TailX) != NumCol ):
     print("len(TailX) != %d" % (NumCol))
     Exit = True
   if ( len(TailY) != NumCol ):
     print("len(TailY) != %d" % (NumCol))
     Exit = True
   if ( len(TailZ) != NumCol ):
     print("len(TailZ) != %d" % (NumCol))
     Exit = True
   
   if ( Exit ):
     exit(0)
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
   for idx in range(NumCol):
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

   # Ray can not lie on the surface of or the edge of computational domain
   for i in range(NumCol):
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
   for i in range(NumRow):
       FieldFunction, Units = unit.ChooseUnit(Field[i])
       Line.append([])
       for j in range(NumCol):
           Line[i].append([])
           for k in range(len(DataName)):
              DataSet[k].add_field(("gamer", Field[i]), function=FieldFunction, sampling_type="cell", units=Units, force_override=True)
              Line[i][j].append ([])
              Line[i][j][k] = yt.LineBuffer( DataSet[k], Head[j], Tail[j], int(NumPts[j]) )

          
   for j in range(NumCol):
     Head[j] *= DataSet[j].length_unit

   # Matplolib
   #######################################################
   font = {'family': 'monospace','color': 'black', 'weight': 'heavy', 'size': 20}
   
   f, axs = plt.subplots( NumRow, NumCol, sharex=False, sharey=False )
   f.subplots_adjust( hspace=n.hspace, wspace=n.wspace )
   f.set_size_inches( 10.0, 16.0 )

   axs = axs.flatten()

   for i in range(NumRow):
     for j in range(NumCol):
       for k in range(len(DataName)):
         Ray = np.sqrt( (Line[i][j][k]["x"]-Head[j][0])**2 + (Line[i][j][k]["y"]-Head[j][1])**2 + (Line[i][j][k]["z"]-Head[j][2])**2 )
         axs[i*NumCol+j].plot( Ray, Line[i][j][k][Field[i]], Mark[k], label=Label[k], markersize=MarkSize[k] )

         axs[i*NumCol+j].tick_params( which='both', direction='in', labelsize=16, top=False )

         axs[i*NumCol+j].set_xlim(min(Ray), max(Ray))
         
         # Dtermine the extreme y-values
         if ( NumCol > 1 ):
           if ( Ymax[i] == 'auto' ):
             Ymax[i] = sys.float_info.min
             Ymax[i]=max(np.amax(Line[i][j][k][Field[i]]), Ymax[i])
           elif ( Ymin[i] == 'auto' ):
             Ymin[i] = sys.float_info.max
             Ymin[i]=min(np.amin(Line[i][j][k][Field[i]]), Ymin[i])

           axs[i*NumCol+j].set_ylim(Ymin[i], Ymax[i])

         if norm[i] == 1:
           axs[i*NumCol+j].set_yscale('log')
         if j==0:
           axs[i*NumCol+j].set_ylabel(YAxisLabel[i], fontsize=20, fontweight='bold')

         # Removing tick labels must be after setting log scale;
         # otherwise tick labels emerge again
         if i < NumRow-1:
           axs[i*NumCol+j].get_xaxis().set_ticks([])
         if j > 0:
           axs[i*NumCol+j].get_yaxis().set_ticks([])

         axs[i*NumCol+j].get_xaxis().set_ticks([])

         if i == 0:
           if ( Title[j] != 'off' ):
             if (Title[j] == 'auto'):
               title = "(%2.1f,%2.1f,%2.1f)\n(%2.1f,%2.1f,%2.1f)" % (Head[j][0], Head[j][1], Head[j][2], Tail[j][0], Tail[j][1], Tail[j][2])
               axs[i*NumCol+j].set_title( title, fontdict=font )
             else:
               axs[i*NumCol+j].set_title( Title[j], fontdict=font )

   # legend
   axs[0].legend(loc='upper center', fontsize=16)

   plt.savefig( n.FileName+'.'+n.FileFormat, bbox_inches='tight', pad_inches=0.05, format=n.FileFormat, dpi=800 )

   print("Done !!")
