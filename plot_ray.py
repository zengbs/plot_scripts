import argparse
import sys
import yt
import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

def _temperature_sr(field, data):
    return data["Temp"]


# load the command-line parameters
parser = argparse.ArgumentParser( description='Plot sr-hydro velocity slices for the blast wave test' )

parser.add_argument( '-s', action='store', required=True,  type=int, dest='idx_start',
                     help='first data index' )
parser.add_argument( '-e', action='store', required=True,  type=int, dest='idx_end',
                     help='last data index' )
parser.add_argument( '-d', action='store', required=False, type=int, dest='didx',
                     help='delta data index [%(default)d]', default=1 )
parser.add_argument( '-i', action='store', required=False,  type=str, dest='prefix',
                     help='data path prefix [%(default)s]', default='./' )

args=parser.parse_args()

# take note
print( '\nCommand-line arguments:' )
print( '-------------------------------------------------------------------' )
for t in range( len(sys.argv) ):
   print( str(sys.argv[t]) ),
print( '' )
print( '-------------------------------------------------------------------\n' )


idx_start   = args.idx_start
idx_end     = args.idx_end
didx        = args.didx
prefix      = args.prefix

colormap    = 'arbre'

center_mode = 'c'
dpi         = 150


yt.enable_parallelism()

ts = yt.load( [ prefix+'/Data_%06d'%idx for idx in range(idx_start, idx_end+1, didx) ] )

for ds in ts.piter():

# add new derived field
   ds.add_field( ("gamer", "temp") , function=_temperature_sr  , sampling_type="cell", units="" )
   field='temp'
   my_ray=ds.ray((375, 94.75, 93.75), (375, 92.75, 93.75))
   srt = np.argsort(my_ray['y'])
   density = my_ray[field][srt]
   
#   plt.semilogy(np.array(my_ray['x'][srt]), np.array(my_ray[field][srt]), 'bo')
   plt.plot(np.array(my_ray['y'][srt]), np.array(my_ray[field][srt]), 'bo', markersize=2)
   plt.xlabel('y')
   plt.ylabel(field)
   plt.savefig("density_xsweep.png")
