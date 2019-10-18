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

Point1 = [0.0, 50.0, 50.0]
Point2 = [100.0, 50.0, 50.0]
#Point1 = [ 0, 0.5, 0.5]
#Point2 = [ 1, 0.5, 0.5]
#Point1 = [0, 1.0, 1.0]
#Point2 = [2, 1.0, 1.0]
#Point1 = [0, 0.0574, 0.0574]
#Point2 = [0.1148, 0.0574, 0.0574]
#Point1 = (0, 0, 0)
#Point2 = (10, 10, 10)
NPoints = 5000

yt.enable_parallelism()

ts = yt.load( [ prefix+'/Data_%06d'%idx for idx in range(idx_start, idx_end+1, didx) ] )

for df.ds in ts.piter():

# add new derived field
   #field='3_velocity_x'
   #field='3_velocity_magnitude'
   field='proper_number_density'
   #field='temperature_sr'

   df.ds.add_field( ("gamer", 'specific_enthalpy_sr'        ), function=df._specific_enthalpy_sr        , sampling_type="cell", units=''                      )
   df.ds.add_field( ("gamer", '4_velocity_x'                ), function=df._4_velocity_x                , sampling_type="cell", units='code_length/code_time' )
   df.ds.add_field( ("gamer", '4_velocity_y'                ), function=df._4_velocity_y                , sampling_type="cell", units='code_length/code_time' )
   df.ds.add_field( ("gamer", '4_velocity_z'                ), function=df._4_velocity_z                , sampling_type="cell", units='code_length/code_time' )
   df.ds.add_field( ("gamer", 'Lorentz_factor'              ), function=df._lorentz_factor              , sampling_type="cell", units=''                      )
   df.ds.add_field( ("gamer", '3_velocity_magnitude'        ), function=df._3_velocity_magnitude        , sampling_type="cell", units='code_length/code_time' )
   df.ds.add_field( ("gamer", 'proper_number_density'       ), function=df._proper_number_density       , sampling_type="cell", units='1/code_length**3'      )
   df.ds.add_field( ("gamer", 'pressure_sr'                 ), function=df._pressure_sr                 , sampling_type="cell", units='code_mass/(code_length*code_time**2)')
   df.ds.add_field( ("gamer", '3_velocity_x'                ), function=df._3_velocity_x                , sampling_type="cell", units='code_length/code_time' )
   df.ds.add_field( ("gamer", '3_velocity_y'                ), function=df._3_velocity_y                , sampling_type="cell", units='code_length/code_time' )
   df.ds.add_field( ("gamer", '3_velocity_z'                ), function=df._3_velocity_z                , sampling_type="cell", units='code_length/code_time' )
   df.ds.add_field( ("gamer", 'temperature_sr'              ), function=df._temperature_sr              , sampling_type="cell", units='' )
   

#  line plot
   plot = yt.LinePlot(df.ds, field, Point1, Point2, NPoints, figure_size=10)
#   plot.set_log(field, True)
#   plot.set_xlabel('x-axis')
##   plot.set_ylim( field, 1e-5, 1.0)
##   plot.set_x_unit('kpc')
##   plot.set_unit(field, 'kg/cm**3')
#   plot.save( name='Data_%06d' %df.ds["DumpID"], suffix='png' )


#  extract data from line plot
   axis = np.linspace(Point1[0], Point2[0], num=NPoints)

   line = np.array(plot)
   plt.plot(axis, line, 'bo')    
   
