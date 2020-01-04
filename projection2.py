import argparse
import sys
import yt
import numpy as np
import yt.visualization.eps_writer as eps
import derived_field as df
import time
import os
import math

pwd = os.getcwd()
pwd = pwd.split('/')

# load the command-line parameters
parser = argparse.ArgumentParser( description='Plot slices for sr-hydro' )

parser.add_argument( '-f'     , action='store', required=True,  type=str,   dest='field',      help='pressure, 4_velocity_x/y/z, Lorentz_factor' )
parser.add_argument( '-stheta', action='store', required=True,  type=float, dest='head_theta', help='start theta' )
parser.add_argument( '-etheta', action='store', required=True,  type=float, dest='tail_theta', help='end theta' )
parser.add_argument( '-sphi  ', action='store', required=True,  type=float, dest='head_phi',   help='start phi' )
parser.add_argument( '-ephi  ', action='store', required=True,  type=float, dest='tail_phi',   help='end phi' )
parser.add_argument( '-nx'    , action='store', required=True,  type=float, dest='N_cut',      help='number of cuts between -sx and -ex')
parser.add_argument( '-st'    , action='store', required=True,  type=int,   dest='idx_start',  help='first data index' )
parser.add_argument( '-et'    , action='store', required=True,  type=int,   dest='idx_end',    help='last data index' )
parser.add_argument( '-dt'    , action='store', required=False, type=int,   dest='didx',       help='delta data index [%(default)d]', default=1 )
parser.add_argument( '-i'     , action='store', required=False, type=str,   dest='prefix',     help='data path prefix [%(default)s]', default='./' )
parser.add_argument( '-max'   , action='store', required=False, type=float, dest='maxlim',     help='max lim', default=float('nan') )
parser.add_argument( '-min'   , action='store', required=False, type=float, dest='minlim',     help='min lim', default=float('nan') )
parser.add_argument( '-max_max'  , action='store', required=False, type=float, dest='max_max',     help='min lim', default=float('nan') )
parser.add_argument( '-max_min'  , action='store', required=False, type=float, dest='max_min',     help='min lim', default=float('nan') )
parser.add_argument( '-max_d'  , action='store', required=True, type=float, dest='max_d',     help='min lim', default=float('nan') )
parser.add_argument( '-z'     , action='store', required=True,  type=int,   dest='zoom',       help='zoom in' )
parser.add_argument( '-l'     , action='store', required=True,  type=int,   dest='log',        help='log scale' )

args=parser.parse_args()

# take note
print( '\nCommand-line arguments:' )
print( '-------------------------------------------------------------------' )
for t in range( len(sys.argv) ):
   print( str(sys.argv[t]) ),
print( '' )
print( '-------------------------------------------------------------------\n' )

field       = args.field
head_theta  = args.head_theta
tail_theta  = args.tail_theta
head_phi    = args.head_phi
tail_phi    = args.tail_phi
N_cut       = args.N_cut
idx_start   = args.idx_start
idx_end     = args.idx_end
didx        = args.didx
prefix      = args.prefix
zoom        = args.zoom
log         = args.log
maxlim      = args.maxlim
minlim      = args.minlim
max_max     = args.max_max
max_min     = args.max_min
max_d       = args.max_d

colormap    = 'afmhot'

dpi         = 150


# ! check parameter
if (zoom < 1):
   print('zoom factor should >= 1!\n')
   sys.exit(0)

if ( log > 1 or log < 0 ):
   print('-l should be 0 or 1!') 
   sys.exit(0)

if ( ( head_theta != tail_theta ) and ( head_phi != tail_phi ) ):
   print('head_theta(tail_theta) should be equal to tail_theta(tail_phi)!')
   sys.exit(0)

if field == 'proper_mass_density':
      unit= 'g/cm**3'
      function=df._proper_mass_density
if field == 'temperature_sr':
      unit= 'GeV'
      function=df._temperature_sr
if field == 'Lorentz_factor':
      unit = ''
      function=df._lorentz_factor
if field == 'pressure_sr':
      unit= 'g/(cm*s**2)'
      function=df._pressure_sr
if field == '4_velocity_x':
      unit= 'cm/s'
      function=df._4_velocity_x
if field == '4_velocity_y':
      unit= 'cm/s'
      function=df._4_velocity_y
if field == '4_velocity_z':
      unit= 'cm/s'
      function=df._4_velocity_z
if field == 'specific_enthalpy_sr':
      unit= '(cm/s)**2'
      function=df._specific_enthalpy_sr
if field == 'total_energy_per_volume':
      unit = 'g/(cm*s**2)'
if field == 'gravitational_potential':
      unit= '(cm/s)**2'
      function=df._gravitational_potential
if field == 'mass_density_sr':
      unit = '1/cm**3'
      function=df._mass_density_sr
if field in ('momentum_x', 'momentum_y', 'momentum_z'):
        unit = 'g/(s*cm**2)'
if field == 'thermal_energy_density_sr':
      unit= 'g/(cm*s**2)'
      function=df._thermal_energy_density_sr
if field == 'kinetic_energy_density_sr':
      unit= 'g/(cm*s**2)'
      function=df._kinetic_energy_density_sr
if field == 'Bernoulli_constant':
      unit= '(cm/s)**2'
      function=df._Bernoulli_const
if field == 'spherical_radial_4velocity':
      unit= 'cm/s'
      function=df._spherical_radial_4velocity
if field == 'cylindrical_radial_4velocity':
      unit= 'cm/s'
      function=df._cylindrical_radial_4velocity
if field == '3_velocity_x':
      unit= 'cm/s'
      function=df._3_velocity_x
if field == '3_velocity_y':
      unit= 'cm/s'
      function=df._3_velocity_y
if field == '3_velocity_z':
      unit= 'cm/s'
      function=df._3_velocity_z
if field == '3_velocity_magnitude':
      unit= 'cm/s'
      function=df._3_velocity_magnitude
if field == 'entropy_per_particle':
      unit = ''
      function=df._entropy_per_particle
if field == 'sound_speed':
      unit = 'cm/s'
      function=df._sound_speed
if field == 'threshold':
      unit = ''
      function=df._threshold
if field == 'synchrotron_emissivity':
      #unit = 'g/(cm*s**2)'
      unit = 'g**2/(cm**4*s**2)'
      function=df._synchrotron_emissivity
if field == 'internal_energy_density_sr':
      unit= 'g/(cm*s**2)'
      function=df._internal_energy_density_sr


t0 = time.time()

yt.enable_parallelism()

ts = yt.load( [ prefix+'/Data_%06d'%idx for idx in range(idx_start, idx_end+1, didx) ] )


if ( head_theta != tail_theta  ):
   head_angle = head_theta
   tail_angle = tail_theta
   fix__angle = head_phi
else:
   head_angle = head_phi
   tail_angle = tail_phi
   fix__angle = head_theta

width         = [300,120]

# ! A vector defining the ‘up’ direction in the plot. 
north_vector  = [ 0, 1, 0]



for df.ds in ts.piter():

#  ! take notes
   if df.ds["EoS"] == 2:
     print ('%s %.6f %s' % ('Equation of state: constant gamma (', df.ds["Gamma"], ')\n'))
   elif df.ds["EoS"] == 1:
     print ('%s' % ('Equation of state: Synge\n'))
   else:
     print ("Your EoS doesn't support yet!\n")
     sys.exit(0)
   
  
   ad = df.ds.all_data()
  
   angle = head_angle

   while angle <= tail_angle:
        
       if ( head_theta != tail_theta  ):
            df.theta = angle
            df.phi   = fix__angle
       else:
            df.theta = fix__angle
            df.phi   = angle

#      ! unit conversion
       df.theta *= np.pi/180.0
       df.phi   *= np.pi/180.0

#      ! The line of sight normal to the slicing plane
       df.normal = [np.sin(df.theta)*np.cos(df.phi), np.sin(df.theta)*np.sin(df.phi), np.cos(df.theta)]
  
#      ! add new derived field
       if field not in ( 'total_energy_per_volume', 'momentum_x', 'momentum_y', 'momentum_z' ):
           df.ds.add_field( ("gamer", field                  ), function=function                 , sampling_type="cell", units=unit                    )
  
#      ! make a projected plot
       if ( df.theta == 0.0 and df.phi == 0.0 ):
          sz = yt.ProjectionPlot( df.ds, 'z', field, center='c', data_source=ad )
       else:
          sz = yt.OffAxisProjectionPlot( df.ds, df.normal, field, 'c', width, north_vector=north_vector, data_source=ad )

#      ! set the range of color bar
       #if   (     math.isnan(minlim) and not math.isnan(maxlim) ):
       #  sz.set_zlim( field, "min", maxlim)
       #elif ( not math.isnan(minlim) and     math.isnan(maxlim) ):
       #  sz.set_zlim( field, minlim, "max")
       #elif (     math.isnan(minlim) and     math.isnan(maxlim) ):
       #  sz.set_zlim( field, "min", "max")
       #else:
       #  sz.set_zlim( field, minlim, maxlim)

       maxlim = max_min

       while ( maxlim <= max_max ):


           sz.set_zlim( field, 'min', maxlim)

#          ! set figure size
#           sz.set_figure_size(150)

#          ! set linear scale around zero
#           sz.set_log( field, log, linthresh=1e-10 )
           sz.set_log( field, log )

#          ! zoom in
           sz.zoom(zoom)

#          ! unit conversion
           df.theta *= 180.0/np.pi
           df.phi   *= 180.0/np.pi

#          ! annotate a title
           title = r'$\theta = %.2f^\circ, \phi=%.2f^\circ$' %(df.theta, df.phi)
           sz.annotate_title(title + pwd[-1])
           sz.set_font({'weight':'bold', 'size':'22'})

#          ! annotate straight line
#           sz.annotate_line((line_x, 0, 20), (line_x, 40, 20), coord_system='data')
           sz.annotate_timestamp( time_unit='code_time', corner='upper_right', time_format='t = {time:.2f} grid$/c$', text_args={'color':'black'})
           sz.set_cmap( field, colormap )
           sz.set_unit( field, 'cm*'+unit )
           sz.set_axes_unit( 'kpc' )

#          ! save picture
           filename = 'theta=%.2f_phi=%.2f' %(df.theta, df.phi)
           sz.save( name='Data_%06d_%2.1e' %( df.ds["DumpID"], maxlim ) + filename, suffix='png' )

#          ! advance angle
           if N_cut > 1:
            angle += np.fabs(head_angle - tail_angle) / N_cut
           else:
            angle += tail_angle + 1

           maxlim += max_d

# ! end timer
t1 = time.time()

print("BigStuff took %.5e sec" % (t1 - t0))
