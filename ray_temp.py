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
#Point1 = [0, 5.0, 5.0]
#Point2 = [10, 5.0, 5.0]
#Point1 = [0 ,  0,  0] 
#Point2 = [10, 10, 10]



# theta = angle between vector and z-axis 
# phi   = angle between vector and x-axis

##big box
#Center = [5.0, 5.0, 5.0]
## center --> side
#theta_1   = 90.0*np.pi/180.0
#phi_1     = 0.0*np.pi/180.0
#NPoints_1 = 12500 
#
#
## center --> edge
#theta_2   = 90.0*np.pi/180.0
#phi_2     = 45.0*np.pi/180.0
#NPoints_2 = 17676
#
## center --> corner
#theta_3   = np.arccos(1.0/np.sqrt(3.0)) 
#phi_3     = 45.0*np.pi/180.0
#NPoints_3 = 21649

##small box
#radius = 0.1148*0.5
#Center = [radius, radius, radius]
## center --> side
#theta_1   = 90.0*np.pi/180.0
#phi_1     = 0.0*np.pi/180.0
#NPoints_1 = 143
#
#
## center --> edge
#theta_2   = 90.0*np.pi/180.0
#phi_2     = 45.0*np.pi/180.0
#NPoints_2 = 202
#
## center --> corner
#theta_3   = np.arccos(1.0/np.sqrt(3.0)) 
#phi_3     = 45.0*np.pi/180.0
#NPoints_3 = 249
#
#
#phi     = [    phi_1,     phi_2,     phi_3]
#theta   = [  theta_1,   theta_2,   theta_3]
#NPoints = [NPoints_1, NPoints_2, NPoints_3]


Point1 = [80 ,80,80]
Point2 = [160,80,80]


yt.enable_parallelism()

ts = yt.load( [ prefix+'/Data_%06d'%idx for idx in range(idx_start, idx_end+1, didx) ] )

for df.ds in ts.piter():

#  add new derived field
   field='temperature_sr'

#   df.ds.add_field( ("gamer", 'specific_enthalpy_sr'        ), function=df._specific_enthalpy_sr        , sampling_type="cell", units=''                      )
#   df.ds.add_field( ("gamer", '4_velocity_x'                ), function=df._4_velocity_x                , sampling_type="cell", units='code_length/code_time' )
#   df.ds.add_field( ("gamer", '4_velocity_y'                ), function=df._4_velocity_y                , sampling_type="cell", units='code_length/code_time' )
#   df.ds.add_field( ("gamer", '4_velocity_z'                ), function=df._4_velocity_z                , sampling_type="cell", units='code_length/code_time' )
#   df.ds.add_field( ("gamer", 'Lorentz_factor'              ), function=df._lorentz_factor              , sampling_type="cell", units=''                      )
#   df.ds.add_field( ("gamer", '3_velocity_magnitude'        ), function=df._3_velocity_magnitude        , sampling_type="cell", units='code_length/code_time' )
#   df.ds.add_field( ("gamer", 'proper_mass_density'          ), function=df._proper_mass_density       , sampling_type="cell", units='g/cm**3'      )
#   df.ds.add_field( ("gamer", 'pressure_sr'                 ), function=df._pressure_sr                 , sampling_type="cell", units='g/(cm*s**2)')
#   df.ds.add_field( ("gamer", 'gravitational_potential'     ), function=df._gravitational_potential     , sampling_type="cell", units='(code_length/code_time)**2')
   df.ds.add_field( ("gamer", 'temperature_sr'               ), function=df._temperature_sr              , sampling_type="cell", units='K')

   NPoints = 5000
   
#  It's dangerous to set x_min and x_max at boundary otherwise the points on boundary would not be found!
   ray = np.linspace(Point1[0]*1.0000001, Point2[0]*0.9999999, NPoints)

   
   for j in range(0, NPoints):
      point          = [ray[j], Point1[1], Point1[2]]
      point_obj      = df.ds.point(point*df.ds.length_unit)
      field_at_point = point_obj['gamer', field]
      np_ary = np.asarray(field_at_point)

      if (j is 0):
        field_gamer = np_ary
      else:
        field_gamer = np.hstack((field_gamer,np_ary))

#  offset
   ray -= 80.0

#  plot
   plt.plot	( ray, field_gamer, 'ro', markersize=1.0 )

#  get extreme values
   x_min = np.amin(ray)
   x_max = np.amax(ray)
   plt.xlim(x_min, x_max)
   #plt.ylim(4e-28, 1e-23) # mass density
   #plt.ylim(2e-11, 1e-8)  # pressure
   #plt.ylim(5e-5, 1.0)  # Dens
   #plt.ylim(-2e-4, 1e-4)  # Ux

   #plt.xscale('log') 
   plt.yscale('log') 
   #plt.yscale('symlog', linthreshy=1e-10) 
   plt.xlabel('kpc')
   plt.ylabel('temperuature (K)')
   #plt.ylabel('4-velocity_x (cm/s)')
   #plt.ylabel('pressure (g/(cm*s**2))')
   FigName = 'Data_%06d_LinePlot_%s.png' % ( df.ds["DumpID"], field )
   plt.savefig( FigName )
   plt.close()
