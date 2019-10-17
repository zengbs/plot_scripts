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


dpi         = 150

#Point1 = [ 0, 0.5, 0.5]
#Point2 = [ 1, 0.5, 0.5]
#Point1 = [0, 1.0, 1.0]
#Point2 = [2, 1.0, 1.0]
Point1 = [0, 5.0, 5.0]
Point2 = [10, 5.0, 5.0]
#Point1 = (0, 0, 0)
#Point2 = (10, 10, 10)

dr        = 4e-4

yt.enable_parallelism()

ts = yt.load( [ prefix+'/Data_%06d'%idx for idx in range(idx_start, idx_end+1, didx) ] )

for df.ds in ts.piter():

# add new derived field
   field='3_velocity_magnitude'

   df.ds.add_field( ("gamer", 'specific_enthalpy_sr'        ), function=df._specific_enthalpy_sr        , sampling_type="cell", units=''                      )
   df.ds.add_field( ("gamer", '4_velocity_x'                ), function=df._4_velocity_x                , sampling_type="cell", units='code_length/code_time' )
   df.ds.add_field( ("gamer", '4_velocity_y'                ), function=df._4_velocity_y                , sampling_type="cell", units='code_length/code_time' )
   df.ds.add_field( ("gamer", '4_velocity_z'                ), function=df._4_velocity_z                , sampling_type="cell", units='code_length/code_time' )
   df.ds.add_field( ("gamer", 'Lorentz_factor'              ), function=df._lorentz_factor              , sampling_type="cell", units=''                      )
   df.ds.add_field( ("gamer", '3_velocity_magnitude'        ), function=df._3_velocity_magnitude        , sampling_type="cell", units='code_length/code_time' )
   df.ds.add_field( ("gamer", 'proper_number_density'       ), function=df._proper_number_density       , sampling_type="cell", units='1/code_length**3'      )
   df.ds.add_field( ("gamer", 'pressure_sr'                 ), function=df._pressure_sr                 , sampling_type="cell", units='code_mass/(code_length*code_time**2)')
   
   length    = np.linalg.norm(np.asarray(Point2)-np.asarray(Point1))
   NPoints   = length / dr
   ray       = np.linspace(0.0, length, num=int(NPoints))
   ray_field = yt.LineBuffer(df.ds, Point1, Point2, int(NPoints))
   print(ray)
   plt.yscale('log') 
   plt.plot	(ray, ray_field[(field)], 'go')
   plt.savefig('hi.png' )


#  load data
#   FileName   = 'Input__HydrostaticEquilibrium'
#   Table_ODE  = np.loadtxt( FileName,  usecols=(2,3), unpack=True, max_rows=NPoints )
#   print(Table_ODE[0])

#   plot = yt.LinePlot(df.ds, field, Point1, Point2, NPoints)
#   plot.annotate_legend(field)
#   plot.set_x_unit('kpc')
##   plot.set_unit(field, 'kg/cm**3')
#   plot.save()
