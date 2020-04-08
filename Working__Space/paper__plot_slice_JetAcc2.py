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
   DataName             = Plot__Paramater['DataName'] 
   FileFormat           = Plot__Paramater['FileFormat'] 
   Field                = Plot__Paramater['Field'] 
   ColorBarLabel        = Plot__Paramater['ColorBarLabel'] 
   ColorBarMax          = Plot__Paramater['ColorBarMax'] 
   ColorBarMin          = Plot__Paramater['ColorBarMin'] 
   norm                 = Plot__Paramater['norm'] 
   CutAxis              = Plot__Paramater['CutAxis'] 
   Coord1               = Plot__Paramater['Coord1'] 
   Coord2               = Plot__Paramater['Coord2'] 
   Coord3               = Plot__Paramater['Coord3'] 
   Coord4               = Plot__Paramater['Coord4'] 
   Xmin                 = Plot__Paramater['Xmin'] 
   Xmax                 = Plot__Paramater['Xmax'] 
   Ymin                 = Plot__Paramater['Ymin'] 
   Ymax                 = Plot__Paramater['Ymax'] 
   Resolution           = Plot__Paramater['Resolution'] 
   aspect               = Plot__Paramater['aspect'] 
   FigWidth             = Plot__Paramater['FigWidth'] 
   CMap                 = Plot__Paramater['CMap'] 
   cylindrical_axis     = Plot__Paramater['cylindrical_axis'] 
   wspace               = Plot__Paramater['wspace'] 
  
   #################################################################

   Coord                = [ Coord1, Coord2, Coord3, Coord4 ]
   Extent               = [Xmin , Xmax , Ymin , Ymax ]

   if norm == 1:
     norm = LogNorm()
   else:
     norm = None
 
   #################################################################
   
   WindowHeight         = abs(Ymax-Ymin)
   WindowWidth          = abs(Xmax-Xmin)
   BufferSize           = [ int(Resolution), int(Resolution*WindowHeight/WindowWidth) ]

   
   df.ds = yt.load(DataName)
   
   
   #   add derived field
   function, units = unit.ChooseUnit(Field)
   df.ds.add_field(("gamer", Field), function=function, sampling_type="cell", units=units)
   
   ad = df.ds.all_data()
   
   sl  = []
   frb = []
   
   ColorBarMax_Row = sys.float_info.min
   ColorBarMin_Row = sys.float_info.max
   
   for j in range(0,len(Coord)):
     sl.append(  df.ds.slice(CutAxis, Coord[j], data_source=ad  )  )
     frb.append( yt.FixedResolutionBuffer(sl[j], Extent,  BufferSize ) )
     frb[j] = np.array(frb[j][Field])
     ColorBarMax_Row = max( ColorBarMax_Row, np.amax(frb[j]) )
     ColorBarMin_Row = min( ColorBarMin_Row, np.amin(frb[j]) )
   
   if ( ColorBarMax == 'auto' ):
     ColorBarMax = ColorBarMax_Row
   if ( ColorBarMin == 'auto' ):
     ColorBarMin = ColorBarMin_Row
   
   
   # Matplolib
   ######################################################
   
   font = {'family': 'monospace','color': 'black', 'weight': 'heavy', 'size': 20}
   
   WidthRatio1 = WindowWidth
   WidthRatio2 = WindowWidth
   WidthRatio3 = WindowWidth
   WidthRatio4 = WindowWidth
   WidthRatio5 = 0.1*WindowWidth
   
   # The amount of width/height reserved for space between subplots,
   # expressed as a fraction of the average axis width/height
   
   WidthRatio=[WidthRatio1, WidthRatio2, WidthRatio3, WidthRatio4, WidthRatio5]
   
   Sum_wspace = (len(WidthRatio)-1)*wspace*sum(WidthRatio)/len(WidthRatio)
   
   FigSize_X = sum(WidthRatio) + Sum_wspace
   FigSize_Y = WindowHeight
   
   Ratio = FigWidth / FigSize_X

   fig = plt.figure(figsize=( FigSize_X*Ratio , FigSize_Y*Ratio ), constrained_layout=False)
   
   gs = fig.add_gridspec(1, len(Coord)+1, wspace=wspace, width_ratios=WidthRatio)
   
   ax = [None]*len(Coord)
   
   
   for j,a in zip(range(len(Coord)),["A","B","C","D"]):
     ax[j] = fig.add_subplot(gs[0,j])
     im = ax[j].imshow(frb[j], cmap=CMap, norm=norm, aspect=aspect,  extent=Extent, vmax=ColorBarMax, vmin=ColorBarMin )
     ax[j].get_xaxis().set_ticks([])
     ax[j].get_yaxis().set_ticks([])
     ax[j].text(0.05,0.95,a,horizontalalignment='left',verticalalignment='top',transform=ax[j].transAxes,fontdict=font, bbox=dict(facecolor='white', alpha=0.5) )
   
   
   cax = fig.add_subplot(gs[0, 4])
   cbar = fig.colorbar(im,cax=cax, use_gridspec=True)
   cbar.set_label(ColorBarLabel, size=20)
   cbar.ax.tick_params(labelsize=20, color='k', direction='in', which='both')
   
   MetaData = {} 
   
   for key in df.ds:
     MetaData.update( {key: str( df.ds[key] ).replace("\n","")} )
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
