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
   FileName             = Plot__Paramater['FileName'] 

   DataName0            = Plot__Paramater['DataName0'] 
   DataName1            = Plot__Paramater['DataName1'] 
   DataName2            = Plot__Paramater['DataName2'] 

   FileFormat           = Plot__Paramater['FileFormat'] 
                                           
   Field0               = Plot__Paramater['Field0'] 
   Field1               = Plot__Paramater['Field1'] 
                                           
   ColorBarLabel0       = Plot__Paramater['ColorBarLabel0'] 
   ColorBarLabel1       = Plot__Paramater['ColorBarLabel1'] 
                                           
   ColorBarMax0         = Plot__Paramater['ColorBarMax0'] 
   ColorBarMax1         = Plot__Paramater['ColorBarMax1'] 
                                           
   ColorBarMin0         = Plot__Paramater['ColorBarMin0'] 
   ColorBarMin1         = Plot__Paramater['ColorBarMin1'] 
                                           
   # 0/1: linear/log
   norm0                = Plot__Paramater['norm0'] 
   norm1                = Plot__Paramater['norm1'] 
                                           
                                           
   CutAxis              = Plot__Paramater['CutAxis'] 
   Coord                = Plot__Paramater['Coord'] 
   Xmin0                = Plot__Paramater['Xmin0'] 
   Xmax0                = Plot__Paramater['Xmax0'] 
   Ymin0                = Plot__Paramater['Ymin0'] 
   Ymax0                = Plot__Paramater['Ymax0'] 
                                           
   Xmin1                = Plot__Paramater['Xmin1'] 
   Xmax1                = Plot__Paramater['Xmax1'] 
   Ymin1                = Plot__Paramater['Ymin1'] 
   Ymax1                = Plot__Paramater['Ymax1'] 

   NormalizedConst_Pres = Plot__Paramater['NormalizedConst_Pres'] 
   NormalizedConst_Dens = Plot__Paramater['NormalizedConst_Dens'] 

   Resolution           = Plot__Paramater['Resolution'] 
   aspect               = Plot__Paramater['aspect'] 
   CMap                 = Plot__Paramater['CMap'] 
   FigWidth             = Plot__Paramater['FigWidth']
                                           
   wspace               = Plot__Paramater['wspace'] 
   hspace               = Plot__Paramater['hspace'] 
  
   #################################################################

   DataName = [ DataName0, DataName1, DataName2 ]
   norm = [ norm0, norm1, norm1 ]
   ColorBarMax = [ ColorBarMax0, ColorBarMax1 ]
   ColorBarMin = [ ColorBarMin0, ColorBarMin1 ]
   ColorBarLabel = [ ColorBarLabel0, ColorBarLabel1  ]
   Field = [ Field0, Field1 ]
 
   #################################################################
   
   for i in range(len(norm)):
     if norm[i] == 1:
       norm[i] = LogNorm()
     else:
       norm[i] = None
       
   #################################################################
   
   WindowHeight1  = abs(Ymax1-Ymin1)
   WindowWidth1   = abs(Xmax1-Xmin1)
   BufferSize1    = [ int(Resolution), int(Resolution*WindowHeight1/WindowWidth1) ]
   
   WindowHeight0  = abs(Ymax0-Ymin0)
   WindowWidth0   = abs(Xmax0-Xmin0)
   BufferSize0    = [ int(BufferSize1[0]*WindowWidth0/WindowWidth1), int(BufferSize1[1]*WindowHeight0/WindowHeight1)  ]
   BufferSize = [BufferSize0, BufferSize1, BufferSize1]   
   
   Extent0    = [Xmin0, Xmax0, Ymin0, Ymax0]
   Extent1    = [Xmin1, Xmax1, Ymin1, Ymax1]
   Extent     = [Extent0, Extent1, Extent1] 
   
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

  
           sl[i].append(  DataSet[j].slice(CutAxis, Coord, data_source=DataSet[j].all_data()  )  )
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
   
   WidthRatio = [WindowWidth1, WindowWidth1,WindowWidth1, WindowWidth1*0.05 ]
   
   Sum_wspace = wspace*sum(WidthRatio)/len(WidthRatio)
   
   FigSize_X = sum(WidthRatio) + Sum_wspace
   FigSize_Y = WindowHeight1*len(Field) + hspace
  
   Ratio = FigWidth/FigSize_X
 
   fig = plt.figure(figsize=( FigSize_X*Ratio , FigSize_Y*Ratio ), constrained_layout=False)
   
   gs = fig.add_gridspec(len(Field),len(DataName)+1,wspace=wspace, hspace=hspace, width_ratios=WidthRatio)
   
   ax = [[None]*len(DataName)]*(len(Field))

   for i in range(len(Field)):
     for j in range(len(DataName)):
       ax[i][j] = fig.add_subplot(gs[i,j])
       im = ax[i][j].imshow(frb[i][j], cmap=CMap, norm=norm[i], aspect=aspect,  extent=Extent[j], vmax=ColorBarMax[i], vmin=ColorBarMin[i] )
       ax[i][j].get_xaxis().set_ticks([])
       ax[i][j].get_yaxis().set_ticks([])
  
     cax = fig.add_subplot(gs[i, 3])

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
