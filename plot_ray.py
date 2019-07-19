import argparse
import sys
import yt
import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt



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
   ds.add_field( ("gamer", "Lorentz_factor") , function=_density_pri  , sampling_type="cell", units="" )
   ds.add_field( ("gamer", "density")      , function=_density_pri  , sampling_type="cell", units="code_mass/code_length**3" )
   ds.add_field( ("gamer", "4-velocity_x") , function=_4velocity_x  , sampling_type="cell", units="code_length/code_time" )
   ds.add_field( ("gamer", "4-velocity_y") , function=_4velocity_y  , sampling_type="cell", units="code_length/code_time" )
   ds.add_field( ("gamer", "4-velocity_z") , function=_4velocity_z  , sampling_type="cell", units="code_length/code_time" )
   ds.add_field( ("gamer", "pressure")     , function=_pressure_sr  , sampling_type="cell", units="code_mass/(code_length*code_time**2)" )
   ds.add_field( ("gamer", "4-velocity_z") , function=_4velocity_z  , sampling_type="cell", units="code_length/code_time" )
   ds.add_field( ("gamer", "magnitude of 4-velocity"), function=_4velocity_mag, sampling_type="cell", units="code_length/code_time" )
   ds.add_field( ("gamer", "3-velocity_x")  , function=_3velocity_x  , sampling_type="cell", units="code_length/code_time" )
   ds.add_field( ("gamer", "3-velocity_y")  , function=_3velocity_y  , sampling_type="cell", units="code_length/code_time" )
   ds.add_field( ("gamer", "3-velocity_z")  , function=_3velocity_z  , sampling_type="cell", units="code_length/code_time" )
   ds.add_field( ("gamer", "magnitude of 3-velocity"), function=_3velocity_mag, sampling_type="cell", units="code_length/code_time" )
   ds.add_field( ("gamer", "conservative density") , function=_density_cons , sampling_type="cell", units="code_mass/code_length**3" )
#   ds.add_field( ("gamer", "momentum_x_sr"), function=_momentum_x_sr, sampling_type="cell", units="code_mass/(code_time*code_length**2)" )
#   ds.add_field( ("gamer", "momentum_y_sr"), function=_momentum_y_sr, sampling_type="cell", units="code_mass/(code_time*code_length**2)" )
#   ds.add_field( ("gamer", "momentum_z_sr"), function=_momentum_z_sr, sampling_type="cell", units="code_mass/(code_time*code_length**2)" )
#   ds.add_field( ("gamer", "energy_cons")  , function=_energy_cons  , sampling_type="cell", units="code_mass/(code_length*code_time**2)" )

   my_ray = ds.ray((0, 0.5, 0.5), (1.0, 0.5, 0.5))
   srt = np.argsort(my_ray['x'])
   density = my_ray[field][srt]
   
#   plt.semilogy(np.array(my_ray['x'][srt]), np.array(my_ray[field][srt]), 'bo')
   plt.plot(np.array(my_ray['x'][srt]), np.array(my_ray[field][srt]), 'bo', markersize=2)
   plt.xlabel('x')
   plt.ylabel(field)
   plt.savefig("density_xsweep.png")
