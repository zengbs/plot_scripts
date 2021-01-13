import yt
import numpy as np
import yt.visualization.eps_writer as eps
from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import matplotlib.gridspec as gridspec
from types import SimpleNamespace    
import sys
import os
from yt.units import gravitational_constant_cgs,\
    speed_of_light_cgs,        \
    charge_proton_cgs,         \
    eV,                        \
    boltzmann_constant_cgs,    \
    mass_hydrogen_cgs,         \
    planck_constant_cgs

from yt.utilities.physical_ratios import sec_per_Myr

import derived_field as df
import unit

def SlicePlot(Plot__Paramater, Input__TestProb):   

   n = SimpleNamespace(**Plot__Paramater)

   DataName      = []
   Field         = []
   CbrLabel      = []
   Unit          = []
   CbrMax        = []
   CbrMin        = []
   norm          = []
   Title         = []
   Xmin          = []
   Xmax          = []
   Ymin          = []
   Ymax          = []
   CbrTick       = []

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
     List     = [  DataName,   Field,   CbrLabel,   CbrMax,   CbrMin,   norm,   CutAxis,   Coord,   Xmin,   Xmax,   Ymin,   Ymax,   Title,   CbrTick,   Unit ]
     ListName = [ "DataName", "Field", "CbrLabel", "CbrMax", "CbrMin", "norm", "CutAxis", "Coord", "Xmin", "Xmax", "Ymin", "Ymax", "Title", "CbrTick", "Unit"]

#  A plane normal to a specified vector and intersecting a particular coordinate.
   else:
     List     = [  DataName,   Field,   CbrLabel,   CbrMax,   CbrMin,   norm,   NormalVectorX,  NormalVectorY,  NormalVectorZ,   CenterX,   CenterY,   CenterZ,  NorthVectorX,  NorthVectorY,  NorthVectorZ,   Xmin,   Xmax,   Ymin,   Ymax,   Title,   CbrTick ,  Unit ]
     ListName = [ "DataName", "Field", "CbrLabel", "CbrMax", "CbrMin", "norm", "NormalVectorX","NormalVectorY","NormalVectorZ", "CenterX", "CenterY", "CenterZ","NorthVectorX","NorthVectorY","NorthVectorZ", "Xmin", "Xmax", "Ymin", "Ymax", "Title", "CbrTick", "Unit"]

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
   if ( len(CbrLabel) != NumRow ):
     print("len(CbrLabel) != %d" % (NumRow))
     Exit = True
   if ( len(Unit) != NumRow ):
     print("len(Unit) != %d" % (NumRow))
     Exit = True
   if ( len(CbrMax) != NumRow ):
     print("len(CbrMax) != %d" % (NumRow))
     Exit = True
   if ( len(CbrMin) != NumRow ):
     print("len(CbrMin) != %d" % (NumRow))
     Exit = True
   if ( len(CbrTick) != NumRow ):
     print("len(CbrTick) != %d" % (NumRow))
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
   MaxFig       = [None]*NumCol
   DataSet      = [None]*NumCol
   TimeStamp    = [None]*NumCol
 

   dX_max = 0
   dY_max = 0

   for j in range(NumCol):
       DataSet[j]   = yt.load(DataName[j])

   for j in range(NumCol):
       if ( Xmax[j] == 'auto' or Xmin[j] == 'auto' or Ymax[j] == 'auto' or Xmin[j] == 'auto' ):
          MaxFig[j] = True;

   for j in range(NumCol):
       if ( n.OffAxisSlice == 0 and MaxFig[j] ):
          Xmin[j] = 0.0
          Ymin[j] = 0.0
  
          if ( Xmax[j] == 'auto' ):
               if ( CutAxis[j] == 'x' ):
                    Xmax[j] = DataSet[j]['BoxSize'][1]
               if ( CutAxis[j] == 'y' ):
                    Xmax[j] = DataSet[j]['BoxSize'][2]
               if ( CutAxis[j] == 'z' ):
                    Xmax[j] = DataSet[j]['BoxSize'][0]
          else:
               if ( CutAxis[j] == 'x' and Xmax[j] >= DataSet[j]['BoxSize'][1] ):
                    print(" Xmax[%d] >= %f" % ( j, DataSet[j]['BoxSize'][1] ) )
                    exit(0)
               if ( CutAxis[j] == 'y' and Xmax[j] >= DataSet[j]['BoxSize'][2] ):
                    print(" Xmax[%d] >= %f" % ( j, DataSet[j]['BoxSize'][2] ) )
                    exit(0)
               if ( CutAxis[j] == 'z' and Xmax[j] >= DataSet[j]['BoxSize'][0] ):
                    print(" Xmax[%d] >= %f" % ( j, DataSet[j]['BoxSize'][0] ) )
                    exit(0)

          if ( Ymax[j] == 'auto' ):
               if ( CutAxis[j] == 'x' ):
                    Ymax[j] = DataSet[j]['BoxSize'][2]
               if ( CutAxis[j] == 'y' ):
                    Ymax[j] = DataSet[j]['BoxSize'][0]
               if ( CutAxis[j] == 'z' ):
                    Ymax[j] = DataSet[j]['BoxSize'][1]
          else:
               if ( CutAxis[j] == 'x' and Ymax[j] >= DataSet[j]['BoxSize'][2] ):
                    print(" Ymax[%d] >= %f" % ( j, DataSet[j]['BoxSize'][2] ) )
                    exit(0)
               if ( CutAxis[j] == 'y' and Ymax[j] >= DataSet[j]['BoxSize'][0]):
                    print(" Ymax[%d] >= %f" % ( j, DataSet[j]['BoxSize'][0] ) )
                    exit(0)
               if ( CutAxis[j] == 'z' and Ymax[j] >= DataSet[j]['BoxSize'][1]):
                    print(" Ymax[%d] >= %f" % ( j, DataSet[j]['BoxSize'][1] ) )
                    exit(0)



       elif ( n.OffAxisSlice == 1 and MaxFig[j] == True ):
          print("Off axis slice does not support maximum slice")
          exit(0)

       dX[j]  = abs(Xmax[j]-Xmin[j])
       dY[j]  = abs(Ymax[j]-Ymin[j])
       dX_max = max( dX_max, dX[j] )
       dY_max = max( dY_max, dY[j] )

   for j in range(NumCol):
       BufferSize[j]   = [  int(n.Resolution*dX[j]/dX_max), int(n.Resolution*dY[j]/dX_max)  ]
       WindowWidth[j]  = dY_max * BufferSize[j][0] / BufferSize[j][1]
       Extent[j]       = [ Xmin[j], Xmax[j], Ymin[j], Ymax[j] ]

   for i in range(NumRow):
       WindowHeight[i] = dY_max

   #################################################################
   

   sl  = []
   frb = []

   # !!! The second added derived field will overwrite the first one !!
 
   #   add derived field
   for i in range(NumRow):
       function, units = unit.ChooseUnit(Field[i], Unit[i])
       CbrMax_Row = sys.float_info.min
       CbrMin_Row = sys.float_info.max

       for j in range(NumCol):
           sl.append([])
           frb.append([])


           if ( n.Model == 'SRHD' ):
             if (Field[i] not in ('momentum_x', 'momentum_y', 'momentum_z', 'total_energy_per_volume')):
               DataSet[j].add_field(("gamer", Field[i]), function=function, sampling_type="cell", units=units)

           if n.OffAxisSlice == 0:
             sl[i].append(  DataSet[j].slice(CutAxis[j], Coord[j], data_source=DataSet[j].all_data()  )  )
           elif n.OffAxisSlice == 1:
             NormalVector = [ NormalVectorX[j], NormalVectorY[j], NormalVectorZ[j]  ]
             Center       = [       CenterX[j],       CenterY[j],       CenterZ[j]  ]
             NorthVector  = [  NorthVectorX[j],  NorthVectorY[j],  NorthVectorZ[j]  ]
             sl[i].append(  DataSet[j].cutting(NormalVector, Center, north_vector=NorthVector, data_source=DataSet[j].all_data()  )  )
          
           frb[i].append( yt.FixedResolutionBuffer(sl[i][j], Extent[j],  BufferSize[j] ) )

           frb[i][j] = np.array(frb[i][j][Field[i]])


           CbrMax_Row = max( CbrMax_Row, np.amax(frb[i][j]) )
           CbrMin_Row = min( CbrMin_Row, np.amin(frb[i][j]) )

       if ( CbrMax[i] == 'auto' ):
         CbrMax[i] = CbrMax_Row
       if ( CbrMin[i] == 'auto' ):
         CbrMin[i] = CbrMin_Row

       print("CbrMax[%d]=%e, CbrMin[%d]=%e" % (i, CbrMax[i], i, CbrMin[i]) )

   # Matplolib
   ######################################################
   # The amount of width/height reserved for space between subplots,
   # expressed as a fraction of the average axis width/height
   
   WidthRatio = []
   for i in range(NumCol):
     WidthRatio.append( WindowWidth[i] )
   
   # colorbar
   WidthRatio.append( WindowWidth[0]*n.CbrWidthRatio )
  
   
   HeightRatio = []
   for i in range(NumRow):
     HeightRatio.append( WindowHeight[i] )
   
   Sum_hspace = n.hspace*sum(HeightRatio)/len(HeightRatio)
   Sum_wspace = n.wspace*sum(WidthRatio)/len(WidthRatio)

 
   FigSize_X = sum(WidthRatio)  + Sum_wspace
   FigSize_Y = sum(HeightRatio) + Sum_hspace
  
   Ratio = n.FigWidth/FigSize_X
 
   fig = plt.figure(figsize=( FigSize_X*Ratio , FigSize_Y*Ratio ), constrained_layout=False)
   
   gs = fig.add_gridspec(NumRow,NumCol+1, wspace=n.wspace, hspace=n.hspace, width_ratios=WidthRatio)
   
   ax = [[None]*NumCol]*(NumRow)

   # Create a big subplot
   BigAx = fig.add_subplot(111, frameon=False)
   # hide tick and tick label of the big axes
   plt.tick_params(labelcolor='none', top='off', bottom='off', left='off', right='off', length=0)
  
 
   BigAx.set_xlabel(n.XAxisLabel, fontdict=dict(size=n.AxisLabelSize), labelpad=n.XAxisLabelPad) # Use argument `labelpad` to move label downwards.
   BigAx.set_ylabel(n.YAxisLabel, fontdict=dict(size=n.AxisLabelSize), labelpad=n.YAxisLabelPad)


   for i in range(NumRow):
     for j in range(NumCol):
       ax[i][j] = fig.add_subplot(gs[i,j])
       im = ax[i][j].imshow(frb[i][j], cmap=n.CMap, norm=norm[i], aspect=n.aspect,  extent=Extent[j], vmax=CbrMax[i], vmin=CbrMin[i] )

       TimeStamp[j] = DataSet[j]['Unit_T']*DataSet[j]['Time'][0]/sec_per_Myr
       ax[i][j].text(0.03, 0.97, format(TimeStamp[j], '.2f')+" Myr", horizontalalignment='left', verticalalignment='top',
                     transform=ax[i][j].transAxes, fontdict=dict(size=n.TimeStampSize),
                     bbox=dict(facecolor='white', alpha=0.5, boxstyle="round", edgecolor='none') )

       if n.AxisTick == 'on':
          ax[i][j].tick_params(labelsize=n.AxisTickLabelSize, color='k', direction='in', which='major',
                               width=n.AxisTickWidth, length=n.AxisMajorTickLength, pad=n.AxisTickLabelPad)
          ax[i][j].get_xaxis().set_ticks([float(i) for i in n.XAxisTick.split(",")])
          ax[i][j].get_yaxis().set_ticks([float(i) for i in n.YAxisTick.split(",")])
          if j > 0:
             ax[i][j].get_yaxis().set_ticks([])
          if i < NumRow-1:
             ax[i][j].get_xaxis().set_ticks([])
       elif n.AxisTick == 'off':
            ax[i][j].get_yaxis().set_ticks([])
            ax[i][j].get_xaxis().set_ticks([])
  
       if i == 0:
         if ( Title[j] != 'off' ):
           if (Title[j] == 'auto'):
               Title[j] = DataName[j]
           ax[i][j].set_title( Title[j], fontdict=dict(size=n.TitleSize), pad=0 )

       for axis in ['top','bottom','left','right']:
           ax[i][j].spines[axis].set_linewidth(n.CbrBorderWidth)


     cbar = fig.colorbar(im,cax=fig.add_subplot(gs[i, NumCol]), use_gridspec=True)

     if Unit[i] == 'off':
        cbar.set_label(CbrLabel[i], size=n.CbrLabelSize)
     else:
        cbar.set_label(CbrLabel[i]+" "+"("+Unit[i]+")", size=n.CbrLabelSize)

     cbar.ax.tick_params(labelsize=n.CbrTickLabelSize, color='k', direction='in', which='major',
                         width=n.CbrTickWidth, length=n.CbrMajorTickLength, pad=n.CbrTickLabelPad)
     cbar.ax.tick_params(                              color='k', direction='in', which='minor',
                         width=n.CbrTickWidth, length=n.CbrMinorTickLength, pad=n.CbrTickLabelPad)
 
     if CbrTick[i] != 'off':
        cbar.ax.get_yaxis().set_ticks([float(k) for k in CbrTick[i].split(",")])

     cbar.outline.set_linewidth(n.CbrBorderWidth)

   FileOut = n.FileName+"."+n.FileFormat
 
   plt.savefig( FileOut, bbox_inches='tight', pad_inches=0, format=n.FileFormat, dpi=800 )

   print ("Done !!")
