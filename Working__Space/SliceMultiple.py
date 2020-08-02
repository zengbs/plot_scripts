import yt
import numpy as np
import yt.visualization.eps_writer as eps
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import matplotlib.gridspec as gridspec
from types import SimpleNamespace    
import sys
import os



import derived_field as df
import unit

def _Plot(Plot__Paramater, Input__TestProb):   

   n = SimpleNamespace(**Plot__Paramater)

   DataName      = []
   Field         = []
   ColorBarLabel = []
   ColorBarMax   = []
   ColorBarMin   = []
   norm          = []
   Title         = []
   Xmin          = []
   Xmax          = []
   Ymin          = []
   Ymax          = []

#  axis slice
   CutAxis       = []   # The axis along which to slice
   Coord         = []   # The coordinate along the axis at which to slice. 

#  off axis slice
   NormalVectorX = []
   NormalVectorY = []
   NormalVectorZ = []
   NorthVectorX  = []
   NorthVectorY  = []
   NorthVectorZ  = []
   CenterX       = []
   CenterY       = []
   CenterZ       = []
  
   List          = []
   ListName      = []

#  A plane normal to one of the axes and intersecting a particular coordinate
   if n.OffAxisSlice == 0:
     List     = [  DataName,   Field,   ColorBarLabel,   ColorBarMax,   ColorBarMin,   norm,   CutAxis,   Coord,   Xmin,   Xmax,   Ymin,   Ymax,   Title ]
     ListName = [ "DataName", "Field", "ColorBarLabel", "ColorBarMax", "ColorBarMin", "norm", "CutAxis", "Coord", "Xmin", "Xmax", "Ymin", "Ymax", "Title" ]

#  A plane normal to a specified vector and intersecting a particular coordinate.
   else:
     List     = [  DataName,   Field,   ColorBarLabel,   ColorBarMax,   ColorBarMin,   norm,   NormalVectorX,  NormalVectorY,  NormalVectorZ,   CenterX,   CenterY,   CenterZ,  NorthVectorX,  NorthVectorY,  NorthVectorZ,   Xmin,   Xmax,   Ymin,   Ymax,   Title ]
     ListName = [ "DataName", "Field", "ColorBarLabel", "ColorBarMax", "ColorBarMin", "norm", "NormalVectorX","NormalVectorY","NormalVectorZ", "CenterX", "CenterY", "CenterZ","NorthVectorX","NorthVectorY","NorthVectorZ", "Xmin", "Xmax", "Ymin", "Ymax", "Title" ]

   NumData = 0
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
   if ( len(norm) != NumRow ):
     print("len(norm) != %d" % (NumRow))
     Exit = True
   if ( len(ColorBarLabel) != NumRow ):
     print("len(ColorBarLabel) != %d" % (NumRow))
     Exit = True
   if ( len(ColorBarMax) != NumRow ):
     print("len(ColorBarMax) != %d" % (NumRow))
     Exit = True
   if ( len(ColorBarMin) != NumRow ):
     print("len(ColorBarMin) != %d" % (NumRow))
     Exit = True

   if ( len(DataName) != NumCol ):
     print("len(DataName) != %d" % (NumCol))
     Exit = True
   if ( len(Title) != NumCol ):
     print("len(Title) != %d" % (NumCol))
     Exit = True
   if ( len(Ymax) != NumCol ):
     print("len(Ymax) != %d" % (NumCol))
     Exit = True
   if ( len(Ymin) != NumCol ):
     print("len(Ymin) != %d" % (NumCol))
     Exit = True
   
   if (n.OffAxisSlice == 1):
     if ( len(NormalVectorX) != NumCol ):
       print("len(NormalVectorX) != %d" % (NumCol))
       Exit = True
     if ( len(NormalVectorY) != NumCol ):
       print("len(NormalVectorY) != %d" % (NumCol))
       Exit = True
     if ( len(NormalVectorZ) != NumCol ):
       print("len(NormalVectorZ) != %d" % (NumCol))
       Exit = True
     if ( len(NorthVectorX) != NumCol ):
       print("len(NorthVectorX) != %d" % (NumCol))
       Exit = True
     if ( len(NorthVectorY) != NumCol ):
       print("len(NorthVectorY) != %d" % (NumCol))
       Exit = True
     if ( len(NorthVectorZ) != NumCol ):
       print("len(NorthVectorZ) != %d" % (NumCol))
       Exit = True
     if ( len(CenterX) != NumCol ):
       print("len(CenterX) != %d" % (NumCol))
       Exit = True
     if ( len(CenterY) != NumCol ):
       print("len(CenterY) != %d" % (NumCol))
       Exit = True
     if ( len(CenterZ) != NumCol ):
       print("len(CenterZ) != %d" % (NumCol))
       Exit = True
     if ( len(Xmax) != NumCol ):
       print("len(Xmax) != %d" % (NumCol))
       Exit = True
     if ( len(Xmin) != NumCol ):
       print("len(Xmin) != %d" % (NumCol))
       Exit = True
   elif (n.OffAxisSlice == 0):
     if ( len(CutAxis) != NumCol ):
       print("len(CutAxis) != %d" % (NumCol))
       Exit = True
     if ( len(Coord) != NumCol ):
       print("len(Coord) != %d" % (NumCol))
       Exit = True
     

   if ( Exit ):
     exit(0)
       

   #################################################################
 
   for i in range(NumRow):
     if ( Field[i] == 'Lorentz_factor_1' and norm[i] == 1 ):
       print('We recommand plot Lorentz_factor_1 with linear scale')
       exit(0)
      

   #################################################################
   
   for i in range(len(norm)):
     if norm[i] == 1:
       norm[i] = LogNorm()
     else:
       norm[i] = None
       
   #################################################################
   WindowHeight = [None]*NumRow
   WindowWidth  = [None]*NumCol
   BufferSize   = [None]*NumCol
   Extent       = [None]*NumCol
   dX           = [None]*NumCol
   dY           = [None]*NumCol

   dX_max = 0
   dY_max = 0

   for i in range(NumCol):
       dX[i]           = abs(Xmax[i]-Xmin[i])
       dY[i]           = abs(Ymax[i]-Ymin[i])
       dX_max          = max ( dX_max, dX[i] )
       dY_max          = max ( dY_max, dY[i] )


   for i in range(NumCol):
       BufferSize[i]   = [  int(n.Resolution*dX[i]/dX_max), int(n.Resolution*dY[i]/dX_max)  ]
       WindowWidth[i]  = dY_max * BufferSize[i][0] / BufferSize[i][1]
       Extent[i]       = [ Xmin[i], Xmax[i], Ymin[i], Ymax[i] ]

   for i in range(NumRow):
       WindowHeight[i] = dY_max

   #################################################################
   
   DataSet  = [ None ]*NumCol

   sl  = []
   frb = []

   # !!! The second added derived field will overwrite the first one !!
 
   #   add derived field
   for i in range(NumRow):
       function, units = unit.ChooseUnit(Field[i])
       ColorBarMax_Row = sys.float_info.min
       ColorBarMin_Row = sys.float_info.max

       for j in range(NumCol):
           sl.append([])
           frb.append([])

           DataSet[j] = yt.load(DataName[j])
           DataSet[j].add_field(("gamer", Field[i]), function=function, sampling_type="cell", units=units)

           if n.OffAxisSlice == 0:
             sl[i].append(  DataSet[j].slice(CutAxis[j], Coord[j], data_source=DataSet[j].all_data()  )  )
           else:
             NormalVector = [ NormalVectorX[j], NormalVectorY[j], NormalVectorZ[j]  ]
             Center       = [       CenterX[j],       CenterY[j],       CenterZ[j]  ]
             NorthVector  = [  NorthVectorX[j],  NorthVectorY[j],  NorthVectorZ[j]  ]
             sl[i].append(  DataSet[j].cutting(NormalVector, Center, north_vector=NorthVector, data_source=DataSet[j].all_data()  )  )
          
           frb[i].append( yt.FixedResolutionBuffer(sl[i][j], Extent[j],  BufferSize[j] ) )

           frb[i][j] = np.array(frb[i][j][Field[i]])

           ColorBarMax_Row = max( ColorBarMax_Row, np.amax(frb[i][j]) )
           ColorBarMin_Row = min( ColorBarMin_Row, np.amin(frb[i][j]) )

       if ( ColorBarMax[i] == 'auto' ):
         ColorBarMax[i] = ColorBarMax_Row
       if ( ColorBarMin[i] == 'auto' ):
         ColorBarMin[i] = ColorBarMin_Row


   # Matplolib
   ######################################################
   
   font = {'family': 'monospace','color': 'black', 'weight': 'heavy', 'size': 20}
   
   
   # The amount of width/height reserved for space between subplots,
   # expressed as a fraction of the average axis width/height
   
   WidthRatio = []
   for i in range(NumCol):
     WidthRatio.append( WindowWidth[i] )
   
   # colorbar
   WidthRatio.append( WindowWidth[0]*0.05 )
  
   
   HeightRatio = []
   for i in range(NumRow):
     HeightRatio.append( WindowHeight[i] )
   
   Sum_hspace = n.hspace*sum(HeightRatio)/len(HeightRatio)
   Sum_wspace = n.wspace*sum(WidthRatio)/len(WidthRatio)

 
   FigSize_X = sum(WidthRatio)  + Sum_wspace
   FigSize_Y = sum(HeightRatio) + Sum_hspace
  
   Ratio = n.FigWidth/FigSize_X
 
   fig = plt.figure(figsize=( FigSize_X*Ratio , FigSize_Y*Ratio ), constrained_layout=False)
   
   gs = fig.add_gridspec(NumRow,NumCol+1,wspace=n.wspace, hspace=n.hspace, width_ratios=WidthRatio)
   
   ax = [[None]*NumCol]*(NumRow)


   for i in range(NumRow):
     for j in range(NumCol):
       ax[i][j] = fig.add_subplot(gs[i,j])
       im = ax[i][j].imshow(frb[i][j], cmap=n.CMap, norm=norm[i], aspect=n.aspect,  extent=Extent[j], vmax=ColorBarMax[i], vmin=ColorBarMin[i] )
       ax[i][j].get_xaxis().set_ticks([])
       ax[i][j].get_yaxis().set_ticks([])

       if i == 0:
         if ( Title[j] != 'off' ):
           if (Title[j] == 'auto'):
               Title[j] = DataName[j]
           ax[i][j].set_title( Title[j], fontdict=font )

     cax = fig.add_subplot(gs[i, NumCol])

     cbar = fig.colorbar(im,cax=cax, use_gridspec=True)

     cbar.ax.tick_params(which='minor', length=0)
     cbar.set_label(ColorBarLabel[i], size=20)
     cbar.ax.tick_params(labelsize=20, color='k', direction='in', which='major')
  
 
   MetaData = {} 
   
   for key in DataSet[0]:
     MetaData.update( {key: str( DataSet[0][key] ).replace("\n","")} )
   for key in Input__TestProb:
     MetaData.update( {key: str( Input__TestProb[key] ).replace("\n","")} )
   for key in Plot__Paramater:
     MetaData.update( {key: str( Plot__Paramater[key] ).replace("\n","")} )
   
   
   MetaData.update( {"Pwd":os.getcwd()} )
  
   FileOut = n.FileName+"."+n.FileFormat
 
   plt.savefig( FileOut, bbox_inches='tight', pad_inches=0.05, format=n.FileFormat, dpi=800, metadata=MetaData )


   # recoed all parameters in eps format 
   if n.FileFormat == 'eps':
      with open(FileOut, "r+") as f2:
             for x in range(6):
                f2.readline()            # skip past early lines
             pos = f2.tell()             # remember insertion position
             f2_remainder = f2.read()    # cache the rest of f2
             f2.seek(pos)
             for key in MetaData:
               string = '%%{:<12}  {:12}\n'.format(key, MetaData[key])
               f2.write(string)
             f2.write(f2_remainder)

   print ("Done !!")
