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
#                       'Mark_01': 'ro', 'MarkSize_00': 1.0, 'MarkSize_01': 1.0, 'Legend_00': 'off', 
#                       'Legend_01': 'off', 'Model_00': 'SRHD', 'Model_01': 'SRHD', 'Field_00': 'Lorentz_factor', 
#                       'Field_01': 'Lorentz_factor', 'NumPts_00': 2048.0, 'NumPts_01': 2048.0, 
#                       'HeadX_00': 50.0, 'HeadY_00': 50.0, 'HeadZ_00': 50.0, 'TailX_00': 77.5, 'TailY_00': 50.0, 
#                       'TailZ_00': 50.0, 'HeadX_01': 50.0, 'HeadY_01': 50.0, 'HeadZ_01': 50.0, 'TailX_01': 77.5, 
#                       'TailY_01': 50.0, 'TailZ_01': 50.0, 'OriginX_00': 0.0, 'OriginX_01': 0.0}, 
#  'plot/panel_00_00': {'Title': 'off', 'YAxisLabel': '$\\gamma$', 'XAxisLabel': 'x', 
#                       'normX': 0.0, 'normY': 0.0, 'Ymax': 'auto', 'Ymin': 'auto', 'NumLine': 2.0, 
#                       'DataName_00': 'Data_000008', 'DataName_01': 'Data_000008', 'Mark_00': 'ro', 
#                       'Mark_01': 'ro', 'MarkSize_00': 1.0, 'MarkSize_01': 1.0, 'Legend_00': 'off', 
#                       'Legend_01': 'off', 'Model_00': 'SRHD', 'Model_01': 'SRHD', 'Field_00': 'Lorentz_factor', 
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
#                       'Legend'  : ['Legend_00'  , 'Legend_01'   ], 
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

   DataKeys = ["DataName","Mark","MarkSize","Legend","Model","Field","NumPts",
               "HeadX","HeadY","HeadZ","TailX","TailY","TailZ","OriginX"]
   RealDataKey = {}
   for panel in list(Plot__Paramater.keys())[:-1]: # iterate over panels in dictionary but panel_common
       PanelIdx = list(Plot__Paramater.keys()).index(panel)
       RealDataKey[panel] = {}
       for data_key in DataKeys:
               real_key_list = list("_".join((data_key, "%02d"% (line))) for line in range(int(ns[PanelIdx].NumLine)))
               RealDataKey[panel][data_key] = real_key_list
               for real_key in real_key_list:
                   if real_key not in Plot__Paramater[panel]:
                      print("The %20s is absent in %20s !!" % ( real_key, panel ))
                      exit()



   font = {'family': 'monospace','color': 'black', 'weight': 'heavy', 'size': 20}
   
   f, axs = plt.subplots( NumRow, NumCol, sharex=False, sharey=False )
   f.subplots_adjust( hspace=ns[-1].hspace, wspace=ns[-1].wspace )
   f.set_size_inches( ns[-1].FigSizeX, ns[-1].FigSizeY )

   if ( NumRow != 1 or NumCol != 1 ):
        axs = axs.flatten()

 # Line[panel][RayIdx] = [....]
   Line     = []

#  Extract ray data from dataset
   for panel in list(Plot__Paramater.keys())[:-1]: # iterate over panels in dictionary but panel_common
       PanelIdx = list(Plot__Paramater.keys()).index(panel)
       Zipped = zip( RealDataKey[panel]['HeadX'],    RealDataKey[panel]['HeadY'],   RealDataKey[panel]['HeadZ'],
                     RealDataKey[panel]['TailX'],    RealDataKey[panel]['TailY'],   RealDataKey[panel]['TailZ'],
                     RealDataKey[panel]['DataName'], RealDataKey[panel]['Field'],   RealDataKey[panel]['NumPts'],
                     RealDataKey[panel]['Model'],    RealDataKey[panel]['OriginX'], RealDataKey[panel]['Mark'],
                     RealDataKey[panel]['MarkSize'], RealDataKey[panel]['Legend'] )
       Line.append([])
       RayIdx=0

       Ymax       = Plot__Paramater[panel]['Ymax']
       Ymin       = Plot__Paramater[panel]['Ymin']
       normX      = Plot__Paramater[panel]['normX']
       normY      = Plot__Paramater[panel]['normY']
       Title      = Plot__Paramater[panel]['Title']
       XAxisLabel = Plot__Paramater[panel]['XAxisLabel']
       YAxisLabel = Plot__Paramater[panel]['YAxisLabel']
       XmaxPanel  = []
       XminPanel  = []
       YmaxPanel  = []
       YminPanel  = []

       # iterate over attributes in a specific panel
       for headx, heady, headz, tailx, taily, tailz, dataname, field, pts, model, originx, mark, marksize, legend in Zipped:
           HeadX    = Plot__Paramater[panel][headx]
           HeadY    = Plot__Paramater[panel][heady]
           HeadZ    = Plot__Paramater[panel][headz]
           TailX    = Plot__Paramater[panel][tailx]
           TailY    = Plot__Paramater[panel][taily]
           TailZ    = Plot__Paramater[panel][tailz]
           DataName = Plot__Paramater[panel][dataname]
           Field    = Plot__Paramater[panel][field]
           NumPts   = Plot__Paramater[panel][pts]
           Model    = Plot__Paramater[panel][model]
           OriginX  = Plot__Paramater[panel][originx]
           Mark     = Plot__Paramater[panel][mark]
           MarkSize = Plot__Paramater[panel][marksize]
           Legend   = Plot__Paramater[panel][legend]

           DataSet  = yt.load(DataName)

           Head     = [HeadX, HeadY, HeadZ]
           Tail     = [TailX, TailY, TailZ]

           Head    *= DataSet.length_unit
           OriginX *= DataSet.length_unit

           BoxSizeX = DataSet["BoxSize"][0]
           BoxSizeY = DataSet["BoxSize"][1]
           BoxSizeZ = DataSet["BoxSize"][2]

           # Rays can not lie on the surface of or the edge of computational domain
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

           Line[PanelIdx].append([])
           FieldFunction, Units = unit.ChooseUnit(Field)
           if Model == 'SRHD':
              if (Field not in ('momentum_x', 'momentum_y', 'momentum_z', 'total_energy_per_volume')):
                 DataSet.add_field(("gamer", Field), function=FieldFunction, sampling_type="cell", units=Units, force_override=True)
           Line[PanelIdx][RayIdx] = yt.LineBuffer( DataSet, Head, Tail, int(NumPts) )



           if ( NumRow == 1 and NumCol == 1 ):
                ax = axs
           else:
                ax = axs[PanelIdx]


           Ray = np.sqrt( (Line[PanelIdx][RayIdx]["x"]-Head[0])**2 + (Line[PanelIdx][RayIdx]["y"]-Head[1])**2 + (Line[PanelIdx][RayIdx]["z"]-Head[2])**2 )
           ax.plot( Ray-OriginX, Line[PanelIdx][RayIdx][Field], Mark, label=Legend, markersize=MarkSize )
           ax.tick_params( which='both', direction='in', labelsize=16, top=False )
           
           # Dtermine the extreme x-values in a specific panel
           XmaxPanel.append(max(Ray))
           XminPanel.append(min(Ray))
           
           # Dtermine the extreme y-values in a specific panel
           YmaxPanel.append(np.amax(Line[PanelIdx][RayIdx][Field]))
           YminPanel.append(np.amin(Line[PanelIdx][RayIdx][Field]))

           if normX == 1:
             ax.set_xscale('log')
           if normY == 1:
             ax.set_yscale('log')
           if PanelIdx%NumCol == 0:
             ax.set_ylabel(YAxisLabel, fontsize=20, fontweight='bold')
           if PanelIdx>=(NumRow-1)*NumCol:
             ax.set_xlabel(XAxisLabel, fontsize=20, fontweight='bold')

           # Removing tick legends must be after setting log scale;
           # otherwise tick legends emerge again
           if PanelIdx<(NumRow-1)*NumCol:
             ax.get_xaxis().set_ticks([])
           if PanelIdx%NumCol != 0:
             ax.get_yaxis().set_ticks([])

           if ( Title != 'off' ):
             if (Title == 'auto'):
               title = "(%2.1f,%2.1f,%2.1f)\n(%2.1f,%2.1f,%2.1f)" % (Head[0], Head[1], Head[2], Tail[0], Tail[1], Tail[2])
               ax.set_title( title, fontdict=font )
             else:
               ax.set_title( Title, fontdict=font )

           if Legend != 'off':
              ax.legend(loc='lower left', fontsize=12)

           RayIdx=RayIdx+1


   for panel in list(Plot__Paramater.keys())[:-1]: # iterate over panels in dictionary but panel_common
       if ( NumRow == 1 and NumCol == 1 ):
            ax = axs
       else:
            ax = axs[PanelIdx]
       Ymax = Plot__Paramater[panel]['Ymax']
       Ymin = Plot__Paramater[panel]['Ymin']
       PanelIdx = list(Plot__Paramater.keys()).index(panel)
       if Ymin == 'auto'    and Ymax == 'DataMax':
          ax.set_ylim(None, max(YmaxPanel))
       if Ymin == 'DataMin' and Ymax == 'auto':
          ax.set_ylim(min(YminPanel), None)
       if Ymin == 'DataMin' and Ymax == 'DataMax':
          ax.set_ylim(min(YminPanel), max(YmaxPanel))

       ax.set_xlim(min(XminPanel), max(XmaxPanel))


   plt.savefig( ns[-1].FileName+'.'+ns[-1].FileFormat, bbox_inches='tight', pad_inches=0.05, format=ns[-1].FileFormat, dpi=800 )

   print("Done !!")
