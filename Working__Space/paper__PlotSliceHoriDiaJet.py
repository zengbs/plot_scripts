import yt
import numpy as np
import yt.visualization.eps_writer as eps
import matplotlib.patches as patches
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import matplotlib.gridspec as gridspec
from types import SimpleNamespace    
import sys
import os



import derived_field as df
import unit


def Rotate(X, Y, Theta):
  RotatedX = X*np.cos(Theta) - Y*np.sin(Theta)
  RotatedY = X*np.sin(Theta) + Y*np.cos(Theta)
  return RotatedX, RotatedY

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

   if NumCol == 3:
     font = {'family': 'monospace','color': 'black', 'weight': 'heavy', 'size': 15}
   if NumCol == 2:
     font = {'family': 'monospace','color': 'black', 'weight': 'heavy', 'size': 15}
   if NumCol == 5:
     font = {'family': 'monospace','color': 'black', 'weight': 'heavy', 'size': 15}
   
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


   Theta = np.arctan2(  NormalVectorZ[1] , (NormalVectorX[1]**2 + NormalVectorY[1]**2 )**0.5 )
   RotatedArrow1 = [None,None,None,None]
   RotatedArrow2 = [None,None,None,None]
   RotatedArrow3 = [None,None,None,None]

   # [0/1/2/3] = head-x / head-y / tail-x / tail-y
   # -->  xycoords='data', the coordinate system of the data.
   # --> (Xmin, Ymin) is bottom left of the axes, and (Xmax, Ymax) is top right of the axes.
   Arrow1      = [-6,+0,-6,+4] # A
   #Arrow2      = [+6,+0,+6,-4] # B
   #Arrow3      = [+8,+0,+8,+4] # C
 

   ### Counterclockwise rotation w.r.t. center of axes
   ## Arrow1
   RotatedArrow1[0], RotatedArrow1[1] = Rotate( Arrow1[0],  Arrow1[1], Theta )
   RotatedArrow1[2], RotatedArrow1[3] = Rotate( Arrow1[2],  Arrow1[3], Theta )


   #### Arrow2
   #RotatedArrow2[0], RotatedArrow2[1] = Rotate( Arrow2[0],  Arrow2[1], Theta )
   #RotatedArrow2[2], RotatedArrow2[3] = Rotate( Arrow2[2],  Arrow2[3], Theta )

   #### Arrow3
   #RotatedArrow3[0], RotatedArrow3[1] = Rotate( Arrow3[0],  Arrow3[1], Theta )
   #RotatedArrow3[2], RotatedArrow3[3] = Rotate( Arrow3[2],  Arrow3[3], Theta )

   ### Rectangular coordinates [x,y]
   Corner1 = [1,-3]
   Corner2 = [7,-3]
   Corner3 = [7,+3]
   Corner4 = [1,+3]

   RotatedCorner1 = [None,None]
   RotatedCorner2 = [None,None]
   RotatedCorner3 = [None,None]
   RotatedCorner4 = [None,None]

   RotatedCorner1[0], RotatedCorner1[1] = Rotate( Corner1[0], Corner1[1], Theta )
   RotatedCorner2[0], RotatedCorner2[1] = Rotate( Corner2[0], Corner2[1], Theta )
   RotatedCorner3[0], RotatedCorner3[1] = Rotate( Corner3[0], Corner3[1], Theta )
   RotatedCorner4[0], RotatedCorner4[1] = Rotate( Corner4[0], Corner4[1], Theta )


   Corner = np.array([[RotatedCorner1[0],RotatedCorner1[1]],
                      [RotatedCorner2[0],RotatedCorner2[1]],
                      [RotatedCorner3[0],RotatedCorner3[1]],
                      [RotatedCorner4[0],RotatedCorner4[1]]])

   if NormalVectorX[0] == 0 and NormalVectorY[0] == 1 and  NormalVectorZ[0] == 0:
     Horizontal = True
   else:
     Horizontal = False

   if DataName[0].split('/')[-2][-6:] == "LowRes":
     Case = "LowRes"
   else:
     Case = "HigRes"
     
 

   for i in range(NumRow):
     for j in range(NumCol):
       ax[i][j] = fig.add_subplot(gs[i,j])
       im = ax[i][j].imshow(frb[i][j], cmap=n.CMap, norm=norm[i], aspect=n.aspect,  extent=Extent[j], vmax=ColorBarMax[i], vmin=ColorBarMin[i] )
       ax[i][j].get_xaxis().set_ticks([])
       ax[i][j].get_yaxis().set_ticks([])
       if NumCol == 2:
         if j == 0:
           if Case == "HigRes" and Horizontal:
             ax[i][j].add_patch(patches.Polygon(Corner, True,
                                edgecolor="w",                                
                                linestyle='-',
                                facecolor="None",linewidth=1) ) 
           ax[i][j].annotate( "A", xy=(RotatedArrow1[0],RotatedArrow1[1]), xytext=(RotatedArrow1[2],RotatedArrow1[3]),color='w',
                             fontsize=font['size'], xycoords='data',horizontalalignment="center", verticalalignment='center', 
                             arrowprops=dict( color='w', arrowstyle="-")  )
         if j == 1:
           ax[i][j].text(0.05,0.95,"A",horizontalalignment='left',verticalalignment='top',
                         transform=ax[i][j].transAxes,fontdict=font, bbox=    dict(facecolor='white', alpha=0.5) )
       elif NumCol == 3:
          if j == 0:
           ax[i][j].annotate( "B", xy=(2,0.5), xytext=(2,1),color='w',
                               fontsize=font['size'], xycoords='data',horizontalalignment="center", verticalalignment='center', 
                               arrowprops=dict( color='w', arrowstyle="-")  )
           ax[i][j].annotate( "C", xy=(6,0.5), xytext=(6,1),color='w',
                               fontsize=font['size'], xycoords='data',horizontalalignment="center", verticalalignment='center', 
                               arrowprops=dict( color='w', arrowstyle="-")  )
          if j == 1:
            ax[i][j].text(0.05,0.95,"B",horizontalalignment='left',verticalalignment='top',
                          transform=ax[i][j].transAxes,fontdict=font, bbox=    dict(facecolor='white', alpha=0.5) )
          if j == 2:
            ax[i][j].text(0.05,0.95,"C",horizontalalignment='left',verticalalignment='top',
                          transform=ax[i][j].transAxes,fontdict=font, bbox=    dict(facecolor='white', alpha=0.5) )

       if i == 0:
         if ( Title[j] != 'off' ):
           if (Title[j] == 'auto'):
               Title[j] = DataName[j]
           ax[i][j].set_title( Title[j], fontdict=font )
         

     cax = fig.add_subplot(gs[i, NumCol])

     cbar = fig.colorbar(im,cax=cax, use_gridspec=True)

     cbar.ax.tick_params(which='minor', length=0)
     cbar.set_label(ColorBarLabel[i], size=font['size'])
     cbar.ax.tick_params(labelsize=font['size'], color='k', direction='in', which='major')
  
 
   FileOut = n.FileName+"."+n.FileFormat 
   plt.savefig( FileOut, bbox_inches='tight', pad_inches=0.05, format=n.FileFormat, dpi=800 )
   print ("Done !!")
