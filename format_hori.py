import yt
import numpy as np
import yt.visualization.eps_writer as eps
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import matplotlib.gridspec as gridspec
import sys
import unit
import derived_field as df
from par import *


WindowHeight0         = abs(Ymax0-Ymin0)
WindowWidth0          = abs(Xmax0-Xmin0)
BufferSize0           = [ int(Resolution), int(Resolution*WindowHeight0/WindowWidth0) ]

WindowHeight         = abs(Ymax-Ymin)
WindowWidth          = abs(Xmax-Xmin)
BufferSize1          = [ int(BufferSize0[0]*0.25), int(BufferSize0[0]*0.25*WindowHeight/WindowWidth)  ]

FileOut              = FileName

Coord      = [ Coord0, Coord1, Coord2, Coord3, Coord4 ]
CutAxis    = [ CutAxis0, CutAxis1, CutAxis1, CutAxis1, CutAxis1 ]
Extent0    = [Xmin0, Xmax0, Ymin0, Ymax0]
Extent1    = [Xmin , Xmax , Ymin , Ymax ]

Extent     = [     Extent0,     Extent1,     Extent1,     Extent1,     Extent1 ]
BufferSize = [ BufferSize0, BufferSize1, BufferSize1, BufferSize1, BufferSize1 ]




df.ds = yt.load(FileName)


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
    ax[i][0].annotate( s, xy=(Coord[k],51), xytext=(Coord[k],52.5),color=annotate_color[i],fontweight='bold',fontsize='10', horizontalalignment="center", arrowprops=dict( facecolor='black', arrowstyle="-", color=annotate_color[i])  )

  cax = fig.add_subplot(gs[i, 5])
  cbar = fig.colorbar(im,cax=cax, use_gridspec=True)
  cbar.set_label(ColorBarLabel[i], size=20)
  cbar.ax.tick_params(labelsize=20, color='k', direction='in', which='both')


plt.savefig( FileOut+".png", bbox_inches='tight', pad_inches=0.05, format='png',dpi=800 )
