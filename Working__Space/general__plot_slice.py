import argparse
import sys
import yt
import numpy as np
import yt.visualization.eps_writer as eps
import time
import os
import math
import json


import derived_field as df
import unit


def _Plot(Plot__Paramater, Input__TestProb):

     colormap = 'arbre'
     dpi = 150
     
     
     ########################################
     
     SliceMax             = Plot__Paramater['SliceMax'] 
     SliceMin             = Plot__Paramater['SliceMin'] 
     CutAxis              = Plot__Paramater['CutAxis']  
      
     DumpIDMin            = Plot__Paramater['DumpIDMin']  
     DumpIDMax            = Plot__Paramater['DumpIDMax']  
     DumpIDDelta          = Plot__Paramater['DumpIDDelta']  
     Zoom                 = Plot__Paramater['Zoom']  
     AxisUnit             = Plot__Paramater['AxisUnit']
     NumSlice             = Plot__Paramater['NumSlice']  
     FileFormat           = Plot__Paramater['FileFormat']
     Title                = Plot__Paramater['Title']
     Axis                 = Plot__Paramater['Axis']  
     TimeStamp            = Plot__Paramater['TimeStamp']  
     TimeUnit             = Plot__Paramater['TimeUnit']
     ColorBar             = Plot__Paramater['ColorBar']  
     CenterOffset_x       = Plot__Paramater['CenterOffset_x']  
     CenterOffset_y       = Plot__Paramater['CenterOffset_y']                    
     CenterOffset_z       = Plot__Paramater['CenterOffset_z']
     WindowHeight         = Plot__Paramater['WindowHeight'] 
     WindowWidth          = Plot__Paramater['WindowWidth'] 
      
     NormalizedConst_Pres = Plot__Paramater['NormalizedConst_Pres'] 
     NormalizedConst_Dens = Plot__Paramater['NormalizedConst_Dens'] 
     Resolution           = Plot__Paramater['Resolution']
     FigSize              = Plot__Paramater['FigSize'] 
     ColorBarMax          = Plot__Paramater['ColorBarMax']                                                                                                        
     ColorBarMin          = Plot__Paramater['ColorBarMin']
     NameColorBar         = Plot__Paramater['NameColorBar']
     LogScale             = Plot__Paramater['LogScale']  
     LinThresh            = Plot__Paramater['LinThresh'] 
     Grid                 = Plot__Paramater['Grid'] 
     
     Field                = Plot__Paramater['Field'] 
     
     
     
     
     
     
     t0 = time.time()
     
     yt.enable_parallelism()
     
     
     ts = yt.load(['Data_%06d' %  idx for idx in range(int(DumpIDMin), int(DumpIDMax)+1, int(DumpIDDelta))])
     
     
     for df.ds in ts.piter():
     
         #  the dimension of window
         if (WindowWidth == 'auto' or WindowHeight == 'auto'):
             if   Plot__Paramater['CutAxis'] == 'x':
                 WindowWidth  = df.ds["BoxSize"][1]
                 WindowHeight = df.ds["BoxSize"][2]
             elif Plot__Paramater['CutAxis'] == 'y':
                 WindowWidth  = df.ds["BoxSize"][2]
                 WindowHeight = df.ds["BoxSize"][0]
             elif Plot__Paramater['CutAxis'] == 'z':
                 WindowWidth  = df.ds["BoxSize"][0]
                 WindowHeight = df.ds["BoxSize"][1]
     
         #   resolution
         if Resolution == 'max':
             BoxSize    = np.asarray(df.ds["BoxSize"])
             MaxLevel   = np.asarray(df.ds["MaxLevel"])
             NX0_Tot    = np.asarray(df.ds["NX0_Tot"])
             MaxBoxSize = np.amax(BoxSize)
     
             Area = (FigureSize**2) * (np.amin(WindowWidth, WindowHeight) / max(WindowWidth, WindowHeight))
             dx = MaxBoxSize / (np.amax(NX0_Tot)*2**MaxLevel)
             Resolution = Area / dx**2
         elif Resolution == 'auto':
             Resolution = 150
     
     
         #   add derived field
         if Field not in ('total_energy_per_volume', 'momentum_x', 'momentum_y', 'momentum_z'):
             function, units = unit.ChooseUnit(Field)
             df.ds.add_field(("gamer", Field), function=function, sampling_type="cell", units=units)
     
         ad = df.ds.all_data()
     
         origin = SliceMin
     
         center = df.ds.domain_center
         center[0] += CenterOffset_x * df.ds.length_unit
         center[1] += CenterOffset_y * df.ds.length_unit
         center[2] += CenterOffset_z * df.ds.length_unit
     
         while origin <= SliceMax:
      
             # center coordinate of window
             if Plot__Paramater['CutAxis'] == 'x':
                 center[0] = origin
             elif Plot__Paramater['CutAxis'] == 'y':
                 center[1] = origin
             elif Plot__Paramater['CutAxis'] == 'z':
                 center[2] = origin
             else:
                 print("CutAxis should be x, y or z!\n")
                 sys.exit(0)
     
     
             sz = yt.SlicePlot(df.ds, Plot__Paramater['CutAxis'], Field, center=center, origin='native', data_source=ad, width=(WindowWidth, WindowHeight))
     
     
             # set the range of color bar
             if ( ColorBarMin == 'auto' and not ColorBarMax == 'auto'):
                 sz.set_zlim(Field, "min", ColorBarMax)
             elif (not ColorBarMin == 'auto' and ColorBarMax == 'auto'):
                 sz.set_zlim(Field, ColorBarMin, "max")
             elif ( ColorBarMin == 'auto' and ColorBarMax == 'auto'):
                 sz.set_zlim(Field, "min", "max")
             else:
                 sz.set_zlim(Field, ColorBarMin, ColorBarMax)
     
             # axis
             if ( Axis == 'off'):
                 sz.hide_axes()
     
             # color bar
             if ( ColorBar == 'off' ):
                 sz.hide_colorbar()
     
             # figure size
             if (FigSize != 'auto'):
                 sz.set_figure_size(FigSize)
     
             # set linear scale around zero
             if (LinThresh > 0  and LogScale == 'on'):
                 sz.set_log(Field, True, LinThresh)
             elif (LinThresh <= 0 and LogScale == 'on' ):
                 sz.set_log(Field, True)
             elif ( LogScale == 'off' ):
                 sz.set_log(Field, False)
                 
     
             # zoom in
             sz.zoom(Zoom)
     
             # colorbar label
             if ( '@' in NameColorBar ):      # with unit
               NameColorBar = NameColorBar.split('@')
               sz.set_colorbar_label( Field, NameColorBar[0] + ' ' + NameColorBar[1] )
             elif ( NameColorBar != 'auto' ): # without unit
               sz.set_colorbar_label( Field, NameColorBar )
         
     
             if Plot__Paramater['CutAxis'] == 'x':
                 x = '%0.3f' % center[0]
                 CutAxis = 'x='+x.zfill(8)
             elif Plot__Paramater['CutAxis'] == 'y':
                 y = '%0.3f' % center[1]
                 CutAxis = 'y='+y.zfill(8)
             elif Plot__Paramater['CutAxis'] == 'z':
                 z = '%0.3f' % center[2]
                 CutAxis = 'z='+z.zfill(8)
     
             #  title
             if (Title == 'auto'):
                 pwd = os.getcwd()
                 pwd = pwd.split('/')
                 Title = 'slice (' + CutAxis + ') ' + pwd[-1]
                 sz.annotate_title('slice (' + CutAxis + ') ' + pwd[-1])
                 Plot__Paramater['Title'] = Title
             elif ( Title != 'off' ):
                 sz.annotate_title(Title)
     
             # font
             sz.set_font({'weight': 'bold', 'size': '40'})
     
             # time stamp
             if (TimeStamp == 'on'):
                 if (TimeUnit == 'code_time'):
                     sz.annotate_timestamp(time_unit='code_time', corner='upper_right',
                                           time_format='t = {time:.4f} ' + AxisUnit + '/$c$', text_args={'color': 'black'})
                 else:
                     NormalizedTime = df.ds["Time"][0] * Zoom / max(WindowWidth, WindowHeight)
     
                     sz.annotate_timestamp(time_unit='code_time', corner='upper_right', 
                                           time_format='t = ' + str("%.1f" % (NormalizedTime)) + " " + TimeUnit, 
                                           text_args={'color': 'white'})
     
             sz.set_cmap(Field, colormap)
             sz.set_unit(Field, units)
             sz.set_axes_unit(AxisUnit)
     
             # grid
             if Grid == 'on':
                 sz.annotate_grids()
     
             # save figure
             FileName = 'Data_%06d_' % df.ds["DumpID"] + str(CutAxis)
     
     
             MetaData = {} 
            
             for key in df.ds:
               MetaData.update( {key: str( df.ds[key] ).replace("\n","")} )
             for key in Input__TestProb:
               MetaData.update( {key: str( Input__TestProb[key] ).replace("\n","")} )
             for key in Plot__Paramater:
               MetaData.update( {key: str( Plot__Paramater[key] ).replace("\n","")} )
        
      
             MetaData.update( {"Pwd":os.getcwd()} )
     
             #  mpl_kwargs: A dict to be passed to 'matplotlib.pyplot.savefig'
             sz.save(name=FileName, suffix=FileFormat,
                     mpl_kwargs={ "dpi": Resolution, "facecolor": 'w', "edgecolor": 'w',"bbox_inches":'tight', "pad_inches": 0.0
                                  ,"metadata":MetaData})
     
     
             FileName += "_Slice_" + CutAxis[0] + "_" + Field + "." + FileFormat
     
     
             # recoed all parameters in eps format 
             if FileFormat == 'eps':
                with open(FileName, "r+") as f2:
                       for x in range(6):
                          f2.readline()            # skip past early lines
                       pos = f2.tell()             # remember insertion position
                       f2_remainder = f2.read()    # cache the rest of f2
                       f2.seek(pos)
                       for key in MetaData:
                         string = '%%{:<12}  {:12}\n'.format(key, MetaData[key])
                         f2.write(string)
                       f2.write(f2_remainder)
     
     
     
             if NumSlice > 1:
                 origin += np.fabs(SliceMin-SliceMax)/(NumSlice-1)
             else:
                 origin = SliceMax + 1
     
     t1 = time.time()
     
     print("Done! it took %.5e sec" % (t1 - t0))
