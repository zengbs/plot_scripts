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
                                           
   Field0               = Plot__Paramater['Field0'] 
   Field1               = Plot__Paramater['Field1'] 
   Field2               = Plot__Paramater['Field2'] 
   Field3               = Plot__Paramater['Field3'] 
   Field4               = Plot__Paramater['Field4'] 
                                           
   ColorBarLabel0       = Plot__Paramater['ColorBarLabel0'] 
   ColorBarLabel1       = Plot__Paramater['ColorBarLabel1'] 
   ColorBarLabel2       = Plot__Paramater['ColorBarLabel2'] 
   ColorBarLabel3       = Plot__Paramater['ColorBarLabel3'] 
   ColorBarLabel4       = Plot__Paramater['ColorBarLabel4'] 
                                           
   ColorBarMax0         = Plot__Paramater['ColorBarMax0'] 
   ColorBarMax1         = Plot__Paramater['ColorBarMax1'] 
   ColorBarMax2         = Plot__Paramater['ColorBarMax2'] 
   ColorBarMax3         = Plot__Paramater['ColorBarMax3'] 
   ColorBarMax4         = Plot__Paramater['ColorBarMax4'] 
                                           
   ColorBarMin0         = Plot__Paramater['ColorBarMin0'] 
   ColorBarMin1         = Plot__Paramater['ColorBarMin1'] 
   ColorBarMin2         = Plot__Paramater['ColorBarMin2'] 
   ColorBarMin3         = Plot__Paramater['ColorBarMin3'] 
   ColorBarMin4         = Plot__Paramater['ColorBarMin4']
                                           
   # 0/1: linear/log
   norm0                = Plot__Paramater['norm0'] 
   norm1                = Plot__Paramater['norm1'] 
   norm2                = Plot__Paramater['norm2'] 
   norm3                = Plot__Paramater['norm3'] 
   norm4                = Plot__Paramater['norm4'] 
                                           
                                           
   CutAxis0             = Plot__Paramater['CutAxis0'] 
   Coord0               = Plot__Paramater['Coord0'] 
   Xmin0                = Plot__Paramater['Xmin0'] 
   Xmax0                = Plot__Paramater['Xmax0'] 
   Ymin0                = Plot__Paramater['Ymin0'] 
   Ymax0                = Plot__Paramater['Ymax0'] 
                                           
   CutAxis1             = Plot__Paramater['CutAxis1'] 
   Coord1               = Plot__Paramater['Coord1'] 
   Coord2               = Plot__Paramater['Coord2'] 
   Coord3               = Plot__Paramater['Coord3'] 
   Coord4               = Plot__Paramater['Coord4'] 
   Xmin                 = Plot__Paramater['Xmin'] 
   Xmax                 = Plot__Paramater['Xmax'] 
   Ymin                 = Plot__Paramater['Ymin'] 
   Ymax                 = Plot__Paramater['Ymax'] 
   NormalizedConst_Pres = Plot__Paramater['NormalizedConst_Pres'] 
   NormalizedConst_Dens = Plot__Paramater['NormalizedConst_Dens'] 
   Resolution           = Plot__Paramater['Resolution'] 
   aspect               = Plot__Paramater['aspect'] 
   FigSize              = Plot__Paramater['FigSize'] 
   CMap                 = Plot__Paramater['CMap'] 
                                           
   cylindrical_axis     = Plot__Paramater['cylindrical_axis'] 
   wspace               = Plot__Paramater['wspace'] 
   hspace               = Plot__Paramater['hspace'] 
  
   #################################################################

   norm = [ norm0, norm1, norm2, norm3, norm4  ]
   ColorBarMax = [ ColorBarMax0, ColorBarMax1, ColorBarMax2, ColorBarMax3, ColorBarMax4  ]
   ColorBarMin = [ ColorBarMin0, ColorBarMin1, ColorBarMin2, ColorBarMin3, ColorBarMin4  ]
   ColorBarLabel = [ ColorBarLabel0, ColorBarLabel1, ColorBarLabel2, ColorBarLabel3, ColorBarLabel4  ]
   Field = [ Field0, Field1, Field2, Field3, Field4  ]
   annotate_color = [ 'white' , 'black' , 'black' , 'black', 'white'  ]
 
   #################################################################
   
   for i in range(0,len(norm)):
     if norm[i] == 'auto':
       norm[i] = LogNorm()
     else:
       norm[i] = None
       
   
   
   #################################################################
   
   WindowHeight0         = abs(Ymax0-Ymin0)
   WindowWidth0          = abs(Xmax0-Xmin0)
   BufferSize0           = [ int(Resolution), int(Resolution*WindowHeight0/WindowWidth0) ]
   
   WindowHeight         = abs(Ymax-Ymin)
   WindowWidth          = abs(Xmax-Xmin)
   BufferSize1          = [ int(BufferSize0[0]*0.25), int(BufferSize0[0]*0.25*WindowHeight/WindowWidth)  ]
   
   
   Coord      = [ Coord0, Coord1, Coord2, Coord3, Coord4 ]
   CutAxis    = [ CutAxis0, CutAxis1, CutAxis1, CutAxis1, CutAxis1 ]
   Extent0    = [Xmin0, Xmax0, Ymin0, Ymax0]
   Extent1    = [Xmin , Xmax , Ymin , Ymax ]
   
   Extent     = [     Extent0,     Extent1,     Extent1,     Extent1,     Extent1 ]
   BufferSize = [ BufferSize0, BufferSize1, BufferSize1, BufferSize1, BufferSize1 ]
   
   
   
   
   df.ds = yt.load(DataName)
   
   
   #   add derived field
   for field in Field:
       function, units = unit.ChooseUnit(field)
       df.ds.add_field(("gamer", field), function=function, sampling_type="cell", units=units)
   
   ad = df.ds.all_data()
   
   sl  = []
   frb = []
   
   
   
   for i in range(0,len(Field)):
     sl.append([])
     frb.append([])
     ColorBarMax_Row = sys.float_info.min
     ColorBarMin_Row = sys.float_info.max
   
     for j in range(0,len(Coord)):
       sl[i].append(  df.ds.slice(CutAxis[j], Coord[j], data_source=ad  )  )
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
   
   WidthRatio0 = WindowWidth0*WindowWidth/WindowHeight0 
   WidthRatio1 = WindowWidth
   WidthRatio2 = WindowWidth
   WidthRatio3 = WindowWidth
   WidthRatio4 = WindowWidth
   WidthRatio5 = 0.2*WindowWidth
   
   # The amount of width/height reserved for space between subplots,
   # expressed as a fraction of the average axis width/height
   
   WithRatio=[WidthRatio0, WidthRatio1, WidthRatio2, WidthRatio3, WidthRatio4, WidthRatio5]
   
   Sum_wspace = 5*wspace*sum(WithRatio)/6
   Sum_hspace = 4*hspace
   
   FigSize_X = sum(WithRatio)*FigSize + Sum_wspace
   FigSize_Y = WindowHeight*FigSize*5 + Sum_hspace
   
   fig = plt.figure(figsize=( FigSize_X , FigSize_Y ), constrained_layout=False)
   
   
   gs = fig.add_gridspec(5,6,wspace=wspace, hspace=hspace, width_ratios=WithRatio)
   
   ax = [[None]*len(Field)]*len(Coord)
   
   
   for i in range(0,len(Field)):
     for j,a in zip(range(0,len(Coord)),[None,"A","B","C","D"]):
       ax[i][j] = fig.add_subplot(gs[i,j])
       im = ax[i][j].imshow(frb[i][j], cmap=CMap, norm=norm[i], aspect=aspect,  extent=Extent[j], vmax=ColorBarMax[i], vmin=ColorBarMin[i] )
       ax[i][j].get_xaxis().set_ticks([])
       ax[i][j].get_yaxis().set_ticks([])
       ax[i][j].text(0.05,0.95,a,horizontalalignment='left',verticalalignment='top',transform=ax[i][j].transAxes,fontdict=font, bbox=dict(facecolor='white', alpha=0.5) )
   
     for k,s in zip(range(1,len(Coord)),["A","B","C","D"]):
       ax[i][0].annotate( s, xy=(Coord[k],51), xytext=(Coord[k],52.5),color=annotate_color[i],fontweight='bold',fontsize='10', horizontalalignment="center", arrowprops=dict( facecolor='black', arrowstyle="-", edgecolor=annotate_color[i])  )
   
     cax = fig.add_subplot(gs[i, 5])
     cbar = fig.colorbar(im,cax=cax, use_gridspec=True)
     cbar.set_label(ColorBarLabel[i], size=20)
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
