
from math import *
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MultipleLocator


# performance tables
table_pizdaint   = 'table__pizdaint'
table_bluewaters = 'table__bluewaters'


# settings
FileOut = 'fig__benchmark_pizdaint'



f, ax = plt.subplots( 1, 2, sharex=False, sharey=False )
#f.subplots_adjust( hspace=0.2, wspace=0.0 )
#f.set_size_inches( 6.4, 9.6 )
f.subplots_adjust( hspace=0.0, wspace=0.2 )
f.set_size_inches( 12.0, 5.0 )

# line styles
LStyle_Dot     = [1, 2]
LStyle_Dash    = [4, 2]
LStyle_DashDot = [4, 2, 1, 2]


# load data
pizdaint   = np.loadtxt( table_pizdaint,   usecols=(0,5), unpack=True )
bluewaters = np.loadtxt( table_bluewaters, usecols=(0,5), unpack=True )


# plot the performance
# ============================================================
nodes=np.asarray( [2**n for n in range(0,13)] )

ax[0].plot( pizdaint  [0], pizdaint  [1], 'r-o', mec='k', lw=2, ms=6,                        label='Piz Daint' )
ax[0].plot( bluewaters[0], bluewaters[1], 'b-D', mec='k', lw=2, ms=6, dashes=LStyle_Dash,    label='Blue Waters' )
ax[0].plot( nodes,         nodes*3.1e7,   'k-',  mec='k', lw=2, ms=6, dashes=LStyle_DashDot, label='Ideal scaling' )

# set axis
ax[0].set_xscale( 'log' )
ax[0].set_yscale( 'log' )
ax[0].set_xlim( 12, 3.0e3 )
ax[0].set_ylim( 1.0e8, 1.0e11 )
ax[0].set_xlabel( 'Number of Nodes', fontsize='large' )
ax[0].set_ylabel( 'Cells/sec',       fontsize='large' )
ax[0].tick_params( which='both', tick2On=True, direction='in' )

# add legend
ax[0].legend( loc='upper left', numpoints=1, labelspacing=0.1, handletextpad=0.4,
              borderpad=0.4, handlelength=2.7, fontsize='large' )


# plot the speedup factor
# ============================================================
ax[1].plot( pizdaint  [0], pizdaint  [1]/pizdaint  [1][0]*pizdaint  [0][0]/pizdaint  [0], 'r-o', mec='k', lw=2, ms=6,                       )
ax[1].plot( bluewaters[0], bluewaters[1]/bluewaters[1][0]*bluewaters[0][0]/bluewaters[0], 'b-D', mec='k', lw=2, ms=6, dashes=LStyle_Dash    )
ax[1].plot( (1.0e0,4.0e3), (1.0,1.0),                                                     'k-',  mec='k', lw=2, ms=6, dashes=LStyle_DashDot )

# set axes
ax[1].set_xscale( 'log' )
ax[1].set_xlim( 8.0e0, 3.0e3 )
ax[1].set_ylim( 0.00, 1.1 )
ax[1].set_xlabel( 'Number of Nodes',     fontsize='large' )
ax[1].set_ylabel( 'Parallel Efficiency', fontsize='large' )
ax[1].tick_params( which='both', tick2On=True, direction='in' )
ax[1].yaxis.set_minor_locator( MultipleLocator(0.05) )

#ax[1].plot( bluewaters[0], pizdaint[2][4:]/bluewaters[2], 'k-o', mec='k', lw=2, ms=6,                     label='Cells/sec' )
#ax[1].plot( bluewaters[0], bluewaters[1]/pizdaint[1][4:], 'r-D', mec='k', lw=2, ms=6, dashes=LStyle_Dash, label='Wall time' )

# set axis
#ax[1].set_xscale( 'log', nonposy='clip' )
#ax[1].set_xlim( 1.0e1, 4.0e2 )
#ax[1].set_ylim( 5.6e1, 1.12e2 )
#ax[1].set_xlabel( 'Blue Waters XK/XE nodes', fontsize='large' )
#ax[1].set_ylabel( 'Speedup (low-res)',       fontsize='large' )
#ax[1].tick_params( which='both', tick2On=True, direction='in' )
#ax[1].yaxis.set_minor_locator( MultipleLocator(2.0) )


# add legend
#ax[1].legend( loc='upper left', numpoints=1, labelspacing=0.1, handletextpad=0.4,
#              borderpad=0.4, handlelength=2.7, fontsize='large' );


# save/show figure
plt.savefig( FileOut+".png", bbox_inches='tight', pad_inches=0.05 )
#plt.savefig( FileOut+".pdf", bbox_inches='tight', pad_inches=0.05 )
#plt.show()
