import yt
import numpy as np
import yt.visualization.eps_writer as eps
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import matplotlib.gridspec as gridspec
import sys
import os



import derived_field as df
import unit

def _Plot(Plot__Paramater, Input__TestProb):   
   FileName               = Plot__Paramater['FileName'] 

   DataName_00            = Plot__Paramater['DataName_00'] 
   DataName_01            = Plot__Paramater['DataName_01'] 
   #DataName_02            = Plot__Paramater['DataName_02'] 

   FileFormat             = Plot__Paramater['FileFormat'] 
                                           
   Field_00               = Plot__Paramater['Field_00'] 
   Field_01               = Plot__Paramater['Field_01'] 
                                           
   ColorBarLabel_00       = Plot__Paramater['ColorBarLabel_00'] 
   ColorBarLabel_01       = Plot__Paramater['ColorBarLabel_01'] 
                                           
   ColorBarMax_00         = Plot__Paramater['ColorBarMax_00'] 
   ColorBarMax_01         = Plot__Paramater['ColorBarMax_01'] 
                                           
   ColorBarMin_00         = Plot__Paramater['ColorBarMin_00'] 
   ColorBarMin_01         = Plot__Paramater['ColorBarMin_01'] 
                                           
   # 0/1: linear/log
   norm_00                = Plot__Paramater['norm_00'] 
   norm_01                = Plot__Paramater['norm_01'] 
                                           
   CutAxis_00              = Plot__Paramater['CutAxis_00'] 
   Coord_00                = Plot__Paramater['Coord_00'] 
   Xmin_00                 = Plot__Paramater['Xmin_00'] 
   Xmax_00                 = Plot__Paramater['Xmax_00'] 
   Ymin_00                 = Plot__Paramater['Ymin_00'] 
   Ymax_00                 = Plot__Paramater['Ymax_00'] 
                                           
   CutAxis_01              = Plot__Paramater['CutAxis_01'] 
   Coord_01                = Plot__Paramater['Coord_01'] 
   Xmin_01                 = Plot__Paramater['Xmin_01'] 
   Xmax_01                 = Plot__Paramater['Xmax_01'] 
   Ymin_01                 = Plot__Paramater['Ymin_01'] 
   Ymax_01                 = Plot__Paramater['Ymax_01'] 
                                           
   #CutAxis_02              = Plot__Paramater['CutAxis_02'] 
   #Coord_02                = Plot__Paramater['Coord_02'] 
   #Xmin_02                 = Plot__Paramater['Xmin_02'] 
   #Xmax_02                 = Plot__Paramater['Xmax_02'] 
   #Ymin_02                 = Plot__Paramater['Ymin_02'] 
   #Ymax_02                 = Plot__Paramater['Ymax_02'] 
   #                                        
   #CutAxis_03              = Plot__Paramater['CutAxis_03'] 
   #Coord_03                = Plot__Paramater['Coord_03'] 
   #Xmin_03                 = Plot__Paramater['Xmin_03'] 
   #Xmax_03                 = Plot__Paramater['Xmax_03'] 
   #Ymin_03                 = Plot__Paramater['Ymin_03'] 
   #Ymax_03                 = Plot__Paramater['Ymax_03'] 
   #                                        
   #CutAxis_04              = Plot__Paramater['CutAxis_04'] 
   #Coord_04                = Plot__Paramater['Coord_04'] 
   #Xmin_04                 = Plot__Paramater['Xmin_04'] 
   #Xmax_04                 = Plot__Paramater['Xmax_04'] 
   #Ymin_04                 = Plot__Paramater['Ymin_04'] 
   #Ymax_04                 = Plot__Paramater['Ymax_04'] 
   #                                        
   #CutAxis_05              = Plot__Paramater['CutAxis_05'] 
   #Coord_05                = Plot__Paramater['Coord_05'] 
   #Xmin_05                 = Plot__Paramater['Xmin_05'] 
   #Xmax_05                 = Plot__Paramater['Xmax_05'] 
   #Ymin_05                 = Plot__Paramater['Ymin_05'] 
   #Ymax_05                 = Plot__Paramater['Ymax_05'] 
                                           
   NormalizedConst_Pres = Plot__Paramater['NormalizedConst_Pres'] 
   NormalizedConst_Dens = Plot__Paramater['NormalizedConst_Dens'] 

   Resolution           = Plot__Paramater['Resolution'] 
   aspect               = Plot__Paramater['aspect'] 
   CMap                 = Plot__Paramater['CMap'] 
   FigWidth             = Plot__Paramater['FigWidth']
                                           
   wspace               = Plot__Paramater['wspace'] 
   hspace               = Plot__Paramater['hspace'] 
  
   #################################################################
   DataName = []
   Field = []
   ColorBarLabel = []
   ColorBarMax = []
   ColorBarMin = []
   norm = []
   CutAxis = []
   Coord = []
   Xmin = []
   Xmax = []
   Ymin = []
   Ymax = []

   List     = [   DataName,   Field,   ColorBarLabel,   ColorBarMax,   ColorBarMin,   norm,   CutAxis,   Coord,   Xmin,   Xmax,   Ymin,   Ymax ]
   ListName = [ "DataName", "Field", "ColorBarLabel", "ColorBarMax", "ColorBarMin", "norm", "CutAxis", "Coord", "Xmin", "Xmax", "Ymin", "Ymax" ]

   for lstname, lst in zip(ListName, List):
     for idx in range(100):
       key = lstname+str("_%02d" % idx)
       if key in Plot__Paramater:
           lst.append( Plot__Paramater[key] )
       else:
           continue


   #################################################################
   
   for i in range(len(norm)):
     if norm[i] == 1:
       norm[i] = LogNorm()
     else:
       norm[i] = None
       
   #################################################################
   WindowHeight = [None]*len(Coord)
   WindowWidth  = [None]*len(Coord)
   BufferSize   = [None]*len(Coord)
   Extent       = [None]*len(Coord)

   for i in range(len(Coord)):
       WindowHeight[i] = abs(Ymax[i]-Ymin[i])
       WindowWidth[i]  = abs(Xmax[i]-Xmin[i])
       BufferSize[i]   = [ int(Resolution), int(Resolution*WindowHeight[i]/WindowWidth[i]) ]
       Extent[i]       = [ Xmin[i], Xmax[i], Ymin[i], Ymax[i] ]

   #################################################################
   
   DataSet  = [ None ]*len(DataName)

   sl  = []
   frb = []

   # !!! The second added derived field will overwrite the first one !!
 
   #   add derived field
   for i in range(len(Field)):
       function, units = unit.ChooseUnit(Field[i])
       ColorBarMax_Row = sys.float_info.min
       ColorBarMin_Row = sys.float_info.max

       for j in range(len(DataSet)):
           sl.append([])
           frb.append([])

           DataSet[j] = yt.load(DataName[j])
           DataSet[j].add_field(("gamer", Field[i]), function=function, sampling_type="cell", units=units)

  
           sl[i].append(  DataSet[j].slice(CutAxis[j], Coord[j], data_source=DataSet[j].all_data()  )  )
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
   for i in range(len(Coord)):
     WidthRatio.append( WindowWidth[i] )
   
   # colorbar
   WidthRatio.append( WindowWidth[0]*0.05 )
  
   
   HeightRatio = []
   for i in range(len(Field)):
     HeightRatio.append( WindowHeight[i] )
   
   Sum_hspace = hspace*sum(HeightRatio)/len(HeightRatio)
   Sum_wspace = wspace*sum(WidthRatio)/len(WidthRatio)

 
   FigSize_X = sum(WidthRatio)  + Sum_wspace
   FigSize_Y = sum(HeightRatio) + Sum_hspace
  
   Ratio = FigWidth/FigSize_X
 
   fig = plt.figure(figsize=( FigSize_X*Ratio , FigSize_Y*Ratio ), constrained_layout=False)
   
   gs = fig.add_gridspec(len(Field),len(Coord)+1,wspace=wspace, hspace=hspace, width_ratios=WidthRatio)
   
   ax = [[None]*len(Coord)]*(len(Field))


   for i in range(len(Field)):
     for j in range(len(Coord)):
       ax[i][j] = fig.add_subplot(gs[i,j])
       im = ax[i][j].imshow(frb[i][j], cmap=CMap, norm=norm[i], aspect=aspect,  extent=Extent[j], vmax=ColorBarMax[i], vmin=ColorBarMin[i] )
       ax[i][j].get_xaxis().set_ticks([])
       ax[i][j].get_yaxis().set_ticks([])

     cax = fig.add_subplot(gs[i, len(Coord)])

     if Field[i] == 'Lorentz_factor':
       cbar = fig.colorbar(im,cax=cax, use_gridspec=True, ticks=[1e1,1e2,1e3,1e4,1e5,1e6])
       cbar.ax.tick_params(which='minor', length=0)
     else:
       cbar = fig.colorbar(im,cax=cax, use_gridspec=True)
       cbar.ax.tick_params(which='minor', length=0)



     #cbar = fig.colorbar(im,cax=cax, use_gridspec=True)
     #cbar.ax.tick_params(which='minor', length=0)

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
  
   FileOut = FileName+"."+FileFormat
 
   plt.savefig( FileOut, bbox_inches='tight', pad_inches=0.05, format=FileFormat, dpi=800, metadata=MetaData )


   # recoed all parameters in eps format 
   if FileFormat == 'eps':
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
