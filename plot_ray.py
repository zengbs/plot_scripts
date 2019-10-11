import argparse
import sys
import yt
import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import derived_field as df


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

Point1 = (0, 5, 5)
Point2 = (10, 5, 5)
axis='x'

yt.enable_parallelism()

ts = yt.load( [ prefix+'/Data_%06d'%idx for idx in range(idx_start, idx_end+1, didx) ] )

for df.ds in ts.piter():

# add new derived field
   field='gravitational_potential'

   df.ds.add_field( ("gamer", 'specific_enthalpy_sr'        ), function=df._specific_enthalpy_sr        , sampling_type="cell", units=''                      )
   df.ds.add_field( ("gamer", '4_velocity_x'                ), function=df._4_velocity_x                , sampling_type="cell", units='code_length/code_time' )
   df.ds.add_field( ("gamer", '4_velocity_y'                ), function=df._4_velocity_y                , sampling_type="cell", units='code_length/code_time' )
   df.ds.add_field( ("gamer", '4_velocity_z'                ), function=df._4_velocity_z                , sampling_type="cell", units='code_length/code_time' )
   df.ds.add_field( ("gamer", 'Lorentz_factor'              ), function=df._lorentz_factor              , sampling_type="cell", units=''                      )
#   df.ds.add_field( ("gamer", 'cylindrical_radial_4velocity'), function=df._cylindrical_radial_4velocity, sampling_type="cell", units='code_length/code_time' )
   df.ds.add_field( ("gamer", 'proper_number_density'       ), function=df._proper_number_density       , sampling_type="cell", units='1/code_length**3'      )
   df.ds.add_field( ("gamer", 'pressure_sr'                 ), function=df._pressure_sr          , sampling_type="cell", units='code_mass/(code_length*code_time**2)')
   df.ds.add_field( ("gamer", field                         ), function=function                        , sampling_type="cell", units=unit                    )

   my_ray=df.ds.ray(Point1, Point2)

   srt = np.argsort(my_ray[axis])

   
   plt.plot(np.array(my_ray[axis][srt]), np.array(my_ray[field][srt]), 'bo', markersize=2)


#   plt.semilogy(np.array(my_ray['x'][srt]), np.array(my_ray[field][srt]), 'bo')
#   plt.yscale("log")
   plt.xlabel(axis)
   plt.ylabel(field)

   plt.savefig(field + "_ray_Data_%06d_" %df.ds["DumpID"] + str(axis) + "_axis")
