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
   annotate_color = [ 'white' , 'black' , 'black' , 'black', 'white', 'white'  ]

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
   WindowHeight = [None]*len(Field)
   WindowWidth  = [None]*len(Coord)
   BufferSize   = [None]*len(Coord)
   Extent       = [None]*len(Coord)
   dX           = [None]*len(Coord)
   dY           = [None]*len(Coord)

   dX_max = 0
   dY_max = 0

   for i in range(len(Coord)):
       dX[i]           = abs(Xmax[i]-Xmin[i])
       dY[i]           = abs(Ymax[i]-Ymin[i])
       dX_max          = max ( dX_max, dX[i] )
       dY_max          = max ( dY_max, dY[i] )


   for i in range(len(Coord)):
       BufferSize[i]   = [  int(n.Resolution*dX[i]/dX_max), int(n.Resolution*dY[i]/dX_max)  ]
       WindowWidth[i]  = dY_max * BufferSize[i][0] / BufferSize[i][1]
       Extent[i]       = [ Xmin[i], Xmax[i], Ymin[i], Ymax[i] ]

   for i in range(len(Field)):
       WindowHeight[i] = dY_max

   #################################################################
   
   sl  = []
   frb = []

   # !!! The second added derived field will overwrite the first one !!
 
   DataSet = yt.load(DataName[0])

   #   add derived field
   for i in range(len(Field)):
       function, units = unit.ChooseUnit(Field[i])
       ColorBarMax_Row = sys.float_info.min
       ColorBarMin_Row = sys.float_info.max

       for j in range(len(Coord)):
           sl.append([])
           frb.append([])

           DataSet.add_field(("gamer", Field[i]), function=function, sampling_type="cell", units=units)

  
           sl[i].append(  DataSet.slice(CutAxis[j], Coord[j], data_source=DataSet.all_data()  )  )
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
   
   Sum_hspace = n.hspace*sum(HeightRatio)/len(HeightRatio)
   Sum_wspace = n.wspace*sum(WidthRatio)/len(WidthRatio)

 
   FigSize_X = sum(WidthRatio)  + Sum_wspace
   FigSize_Y = sum(HeightRatio) + Sum_hspace
  
   Ratio = n.FigWidth/FigSize_X
 
   fig = plt.figure(figsize=( FigSize_X*Ratio , FigSize_Y*Ratio ), constrained_layout=False)
   
   gs = fig.add_gridspec(len(Field),len(Coord)+1,wspace=n.wspace, hspace=n.hspace, width_ratios=WidthRatio)
   
   ax = [[None]*len(Coord)]*(len(Field))


   for i in range(len(Field)):
     for j,a in zip(range(len(Coord)),[None,"D","C","B","A"]):
       ax[i][j] = fig.add_subplot(gs[i,j])
       im = ax[i][j].imshow(frb[i][j], cmap=n.CMap, norm=norm[i], aspect=n.aspect,  extent=Extent[j], vmax=ColorBarMax[i], vmin=ColorBarMin[i] )
       ax[i][j].get_xaxis().set_ticks([])
       ax[i][j].get_yaxis().set_ticks([])
       ax[i][j].text(0.05,0.95,a,horizontalalignment='left',verticalalignment='top',transform=ax[i][j].transAxes,fontdict=font, bbox=dict(facecolor='white', alpha=0.5) )

     for k,s in zip(range(1,len(Coord)),["D","C","B","A"]):
       ax[i][0].annotate( s, xy=(Coord[k],51), xytext=(Coord[k],52.5),color=annotate_color[i],fontweight='bold',fontsize='10', horizontalalignment="center", arrowprops=dict( facecolor='black', arrowstyle="-", edgecolor=annotate_color[i])  )

     cax = fig.add_subplot(gs[i, len(Coord)])

     cbar = fig.colorbar(im,cax=cax, use_gridspec=True)
     
     if i == 1:
       cbar.ax.yaxis.set_ticks([1e-1,1e-3])
 

     cbar.ax.tick_params(which='minor', length=0)
     cbar.set_label(ColorBarLabel[i], size=20)
     cbar.ax.tick_params(labelsize=20, color='k', direction='in', which='major')
   
   MetaData = {} 
   
   for key in DataSet:
     MetaData.update( {key: str( DataSet[key] ).replace("\n","")} )
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

   print('Done!')
