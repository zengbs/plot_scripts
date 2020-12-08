import yt
import numpy as np
import yt.visualization.eps_writer as eps
import matplotlib
import matplotlib.pyplot as plt
from types import SimpleNamespace    
import sys
import re

import derived_field as df
import unit

def Plot(Plot__Paramater, Input__TestProb, NumRow, NumCol):

# Plot__Paramater = 
# {'plot/panel_00_00': {'Title': 'off', 'YAxisLabel': '$\\gamma$', 'XAxisLabel': 'x', 
#                       'normX': 0.0, 'normY': 0.0, 'Ymax': 'auto', 'Ymin': 'auto', 'NumLine': 2.0, 
#                       'DataName_00': 'Data_000008', 'DataName_01': 'Data_000008', 'Mark_00': 'ro', 
#                       'Mark_01': 'ro', 'MarkSize_00': 1.0, 'MarkSize_01': 1.0, 'Label_00': 'off', 
#                       'Label_01': 'off', 'Model_00': 'SRHD', 'Model_01': 'SRHD', 'Field_00': 'Lorentz_factor', 
#                       'Field_01': 'Lorentz_factor', 'NumPts_00': 2048.0, 'NumPts_01': 2048.0, 
#                       'HeadX_00': 50.0, 'HeadY_00': 50.0, 'HeadZ_00': 50.0, 'TailX_00': 77.5, 'TailY_00': 50.0, 
#                       'TailZ_00': 50.0, 'HeadX_01': 50.0, 'HeadY_01': 50.0, 'HeadZ_01': 50.0, 'TailX_01': 77.5, 
#                       'TailY_01': 50.0, 'TailZ_01': 50.0, 'OriginX_00': 0.0, 'OriginX_01': 0.0}, 
#  'plot/panel_00_00': {'Title': 'off', 'YAxisLabel': '$\\gamma$', 'XAxisLabel': 'x', 
#                       'normX': 0.0, 'normY': 0.0, 'Ymax': 'auto', 'Ymin': 'auto', 'NumLine': 2.0, 
#                       'DataName_00': 'Data_000008', 'DataName_01': 'Data_000008', 'Mark_00': 'ro', 
#                       'Mark_01': 'ro', 'MarkSize_00': 1.0, 'MarkSize_01': 1.0, 'Label_00': 'off', 
#                       'Label_01': 'off', 'Model_00': 'SRHD', 'Model_01': 'SRHD', 'Field_00': 'Lorentz_factor', 
#                       'Field_01': 'Lorentz_factor', 'NumPts_00': 2048.0, 'NumPts_01': 2048.0, 
#                       'HeadX_00': 50.0, 'HeadY_00': 50.0, 'HeadZ_00': 50.0, 'TailX_00': 77.5, 'TailY_00': 50.0, 
#                       'TailZ_00': 50.0, 'HeadX_01': 50.0, 'HeadY_01': 50.0, 'HeadZ_01': 50.0, 'TailX_01': 77.5, 
#                       'TailY_01': 50.0, 'TailZ_01': 50.0, 'OriginX_00': 0.0, 'OriginX_01': 0.0} }

#  Create a list of namespace
   ns = []
   for key in Plot__Paramater.keys():
       ns.append( SimpleNamespace(**Plot__Paramater[key]) )


# check common keys in Plot__Paramater['panel_common']
   Keys = ["FileName","FileFormat","FigSizeX","FigSizeY","wspace","hspace",
           "NormalizedConst_Pres","NormalizedConst_Dens"]
   panel = list(Plot__Paramater.keys())[-1]
   for key in Plot__Paramater[panel]:
      if key not in Keys:
         print("The %20s is absent in %20s !!" % ( key, panel ))
         exit()

# check shared keys in Plot__Paramater['panel_??_??']
   Keys = ["XAxisLabel","YAxisLabel","Title","normX","normY","Ymax","Ymin","NumLine"]
   for panel in list(Plot__Paramater.keys())[:-1]: # iterate over panels in dictionary but panel_common
       for key in Keys:
          if key not in Plot__Paramater[panel]:
             print("The %20s is absent in %20s !!" % ( key, panel ))
             exit()

# check data keys in Plot__Paramater['panel_??_??']
# RealDataKey = 
# {'plot/panel_00_00': {'DataName': ['DataName_00', 'DataName_01'], 
#                       'Mark'    : ['Mark_00'    , 'Mark_01'    ], 
#                       'MarkSize': ['MarkSize_00', 'MarkSize_01'], 
#                       'Label'   : ['Label_00'   , 'Label_01'   ], 
#                       'Model'   : ['Model_00'   , 'Model_01'   ], 
#                       'Field'   : ['Field_00'   , 'Field_01'   ], 
#                       'NumPts'  : ['NumPts_00'  , 'NumPts_01'  ], 
#                       'HeadX'   : ['HeadX_00'   , 'HeadX_01'   ], 
#                       'HeadY'   : ['HeadY_00'   , 'HeadY_01'   ], 
#                       'HeadZ'   : ['HeadZ_00'   , 'HeadZ_01'   ], 
#                       'TailX'   : ['TailX_00'   , 'TailX_01'   ], 
#                       'TailY'   : ['TailY_00'   , 'TailY_01'   ], 
#                       'TailZ'   : ['TailZ_00'   , 'TailZ_01'   ], 
#                       'OriginX' : ['OriginX_00' , 'OriginX_01' ]}}

   DataKeys = ["DataName","Mark","MarkSize","Label","Model","Field","NumPts",
               "HeadX","HeadY","HeadZ","TailX","TailY","TailZ","OriginX"]
   FIdx=0
   RealDataKey = {}
   for panel in list(Plot__Paramater.keys())[:-1]: # iterate over panels in dictionary but panel_common
       RealDataKey[panel] = {}
       for data_key in DataKeys:
               real_key_list = list("_".join((data_key, "%02d"% (line))) for line in range(int(ns[FIdx].NumLine)))
               RealDataKey[panel][data_key] = real_key_list
               for real_key in real_key_list:
                   if real_key not in Plot__Paramater[panel]:
                      print("The %20s is absent in %20s !!" % ( real_key, panel ))
                      exit()
       FIdx=FIdx+1


#  Change `Label` from 'no' to 'None'
   for panel in list(Plot__Paramater.keys())[:-1]: # iterate over panels in dictionary but panel_common
       for label in RealDataKey[panel]['Label']:
           if Plot__Paramater[panel][label] == 'off':
              Plot__Paramater[panel][label] = None 




#  Check rays lie inside the box
   for panel in list(Plot__Paramater.keys())[:-1]: # iterate over panels in dictionary but panel_common
       ZippedPoints = zip( RealDataKey[panel]['HeadX'], RealDataKey[panel]['HeadY'], RealDataKey[panel]['HeadZ'],
                           RealDataKey[panel]['TailX'], RealDataKey[panel]['TailY'], RealDataKey[panel]['TailZ'],
                           RealDataKey[panel]['DataName'] )
       for headx, heady, headz, tailx, taily, tailz, DataName in ZippedPoints:

           Head = [ Plot__Paramater[panel][headx], Plot__Paramater[panel][heady], Plot__Paramater[panel][headz] ]
           Tail = [ Plot__Paramater[panel][tailx], Plot__Paramater[panel][taily], Plot__Paramater[panel][tailz] ]

           DataSet  = yt.load(Plot__Paramater[panel][DataName])

           BoxSizeX = DataSet["BoxSize"][0]
           BoxSizeY = DataSet["BoxSize"][1]
           BoxSizeZ = DataSet["BoxSize"][2]

           # Ray can not lie on the surface of or the edge of computational domain
           for j in range(3):
             if (Head[j] == 0 and Tail[j] == 0):
                print("error: Ray can not lie on the surface or edge of computational domain")
                exit(0)
             elif ( j==0 and Head[j] == BoxSizeX and Tail[j] == BoxSizeX ):
                print("error: Ray can not lie on the surface or edge of computational domain")
                exit(0)
             elif ( j==1 and Head[j] == BoxSizeY and Tail[j] == BoxSizeY ):
                print("error: Ray can not lie on the surface or edge of computational domain")
                exit(0)
             elif ( j==2 and Head[j] == BoxSizeZ and Tail[j] == BoxSizeZ ):
                print("error: Ray can not lie on the surface or edge of computational domain")
                exit(0)

   exit()
   
   # Line[Field][Ray][DataName] = [....]
   Line     = []

   # !!! The second added derived field will overwrite the first one !!
   # add derived field
   for i in range(NumRow):
       Line.append([])
       for j in range(NumCol):
           Line[i].append([])
           for k in range(len(DataName)):
              FieldFunction, Units = unit.ChooseUnit(Field[k])
              if ( Model[k] == 'SRHD' ):
                if (Field[k] not in ('momentum_x', 'momentum_y', 'momentum_z', 'total_energy_per_volume')):
                   DataSet[k].add_field(("gamer", Field[k]), function=FieldFunction, sampling_type="cell", units=Units, force_override=True)
              Line[i][j].append ([])
              Line[i][j][k] = yt.LineBuffer( DataSet[k], Head[j], Tail[j], int(NumPts[j]) )

          
   for j in range(NumCol):
     Head[j]    *= DataSet[j].length_unit
     OriginX[j] *= DataSet[j].length_unit

   # Matplolib
   #######################################################
   font = {'family': 'monospace','color': 'black', 'weight': 'heavy', 'size': 20}
   
   f, axs = plt.subplots( NumRow, NumCol, sharex=False, sharey=False )
   f.subplots_adjust( hspace=n.hspace, wspace=n.wspace )
   f.set_size_inches( n.FigSizeX, n.FigSizeY )

   if ( NumRow != 1 or NumCol != 1 ):
        axs = axs.flatten()

   for i in range(NumRow):
     for j in range(NumCol):
       for k in range(len(DataName)):

         if ( NumRow == 1 and NumCol == 1 ):
              ax = axs
         else:
              ax = axs[i*NumCol+j]

         Ray = np.sqrt( (Line[i][j][k]["x"]-Head[j][0])**2 + (Line[i][j][k]["y"]-Head[j][1])**2 + (Line[i][j][k]["z"]-Head[j][2])**2 )
         ax.plot( Ray-OriginX[j], Line[i][j][k][Field[k]], Mark[k], label=Label[k], markersize=MarkSize[k] )
         ax.tick_params( which='both', direction='in', labelsize=16, top=False )
         ax.set_xlim(min(Ray), max(Ray))
         
         # Dtermine the extreme y-values
         if ( NumCol > 1 ):
           if ( Ymax[i] == 'auto' ):
             Ymax[i] = sys.float_info.min
             Ymax[i]=max(np.amax(Line[i][j][k][Field[k]]), Ymax[i])
           if ( Ymin[i] == 'auto' ):
             Ymin[i] = sys.float_info.max
             Ymin[i]=min(np.amin(Line[i][j][k][Field[k]]), Ymin[i])
           ax.set_ylim(Ymin[i], Ymax[i])

         if normX[i] == 1:
           ax.set_xscale('log')
         if normY[i] == 1:
           ax.set_yscale('log')
         if j==0:
           ax.set_ylabel(YAxisLabel[i], fontsize=20, fontweight='bold')
         if i==0:
           ax.set_xlabel(XAxisLabel[i], fontsize=20, fontweight='bold')

         # Removing tick labels must be after setting log scale;
         # otherwise tick labels emerge again
         #if i < NumRow:
         #  ax.get_xaxis().set_ticks([])
         #if j > 0:
         #  ax.get_yaxis().set_ticks([])

         if i == 0:
           if ( Title[j] != 'off' ):
             if (Title[j] == 'auto'):
               title = "(%2.1f,%2.1f,%2.1f)\n(%2.1f,%2.1f,%2.1f)" % (Head[j][0], Head[j][1], Head[j][2], Tail[j][0], Tail[j][1], Tail[j][2])
               ax.set_title( title, fontdict=font )
             else:
               ax.set_title( Title[j], fontdict=font )

   # if all elements in Label are None then do not add legends
   if not all(label is None for label in Label):
     if ( i == 0 and j == 0 ):
          ax.legend(loc='lower left', fontsize=12)

   plt.savefig( n.FileName+'.'+n.FileFormat, bbox_inches='tight', pad_inches=0.05, format=n.FileFormat, dpi=800 )

   print("Done !!")
