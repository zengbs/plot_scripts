import argparse
import sys
import yt
import numpy as np
import yt.visualization.eps_writer as eps
import derived_field as df
import time
import os

pwd = os.getcwd()
pwd = pwd.split('/')

# load the command-line parameters
parser = argparse.ArgumentParser( description='Plot slices for sr-hydro' )

parser.add_argument( '-f',  action='store', required=True,  type=str,   dest='field',     help='pressure, 4_velocity_x/y/z, Lorentz_factor' )
parser.add_argument( '-p',  action='store', required=True,  type=str,   dest='cut_axis',  help='axis you want to cut' )
parser.add_argument( '-sx', action='store', required=True,  type=float, dest='start_cut', help='start cut' )
parser.add_argument( '-ex', action='store', required=True,  type=float, dest='end_cut',   help='end cut' )
parser.add_argument( '-nx', action='store', required=True,  type=float, dest='N_cut',     help='number of cuts between -sx and -ex' )
parser.add_argument( '-st', action='store', required=True,  type=int,   dest='idx_start', help='first data index' )
parser.add_argument( '-et', action='store', required=True,  type=int,   dest='idx_end',   help='last data index' )
parser.add_argument( '-dt', action='store', required=False, type=int,   dest='didx',      help='delta data index [%(default)d]', default=1 )
parser.add_argument( '-i',  action='store', required=False, type=str,   dest='prefix',    help='data path prefix [%(default)s]', default='./' )
parser.add_argument( '-z',  action='store', required=True,  type=int,   dest='zoom',      help='zoom in' )
parser.add_argument( '-l',  action='store', required=True,  type=int,   dest='log',       help='log scale' )
parser.add_argument( '-g',  action='store', required=True,  type=int,   dest='grid',      help='grids' )

args=parser.parse_args()

# take note
print( '\nCommand-line arguments:' )
print( '-------------------------------------------------------------------' )
for t in range( len(sys.argv) ):
   print( str(sys.argv[t]) ),
print( '' )
print( '-------------------------------------------------------------------\n' )

field       = args.field
cut_axis    = args.cut_axis
start_cut   = args.start_cut
end_cut     = args.end_cut
N_cut       = args.N_cut
idx_start   = args.idx_start
idx_end     = args.idx_end
didx        = args.didx
prefix      = args.prefix
zoom        = args.zoom
log         = args.log
grid        = args.grid

colormap    = 'arbre'

dpi         = 150


# check parameter
########################################
if (zoom < 1):
   print('zoom factor should >= 1!\n')
   sys.exit(0)


if ( log > 1 or log < 0 ):
   print('-l should be 0 or 1!') 
   sys.exit(0)

if ( grid > 1 or grid < 0 ):
   print('-g should be 0 or 1!') 
   sys.exit(0)

if ( start_cut > end_cut ):
   print('-ex should be greater than -sx!')
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
      unit = 'g/(cm*s**2)'
      function=df._synchrotron_emissivity
if field == 'internal_energy_density_sr':
      unit= 'g/(cm*s**2)'
      function=df._internal_energy_density_sr


t0 = time.time()

yt.enable_parallelism()

ts = yt.load( [ prefix+'/Data_%06d'%idx for idx in range(idx_start, idx_end+1, didx) ] )


for df.ds in ts.piter():


# take notes
 if df.ds["EoS"] == 2:
   print ('%s %.6f %s' % ('Equation of state: constant gamma (', df.ds["Gamma"], ')\n'))
 elif df.ds["EoS"] == 1:
   print ('%s' % ('Equation of state: Synge\n'))
 else:
   print ("Your EoS doesn't support yet!\n")
   sys.exit(0)


# add new derived field
 if field not in ( 'total_energy_per_volume', 'momentum_x', 'momentum_y', 'momentum_z' ):
   df.ds.add_field( ("gamer", field                         ), function=function                        , sampling_type="cell", units=unit                    )

 ad = df.ds.all_data()

 origin = start_cut

 while origin <= end_cut:
   center = df.ds.domain_center

   if cut_axis == 'x':
     center[0] = origin
   elif cut_axis == 'y':
     center[1] = origin
   elif cut_axis == 'z':
     center[2] = origin
   else:
     print ("cut_axis should be x, y or z!\n")
     sys.exit(0)
     

#  ! cut and plot
#   if ( field in ( '4_velocity_x' ,'4_velocity_y' ,'4_velocity_z', 'momentum_x', 'momentum_y', 'momentum_z', 'kinetic_energy_density' )):
#     cr=ad.cut_region(["obj['kinetic_energy_density'] > 0.0"])
#   else:
#     cr=ad.clone()

#   center[0] = 200.0
   sz = yt.SlicePlot( df.ds, cut_axis, field, center=center, origin='native', data_source=ad )

#   ! set the width of plot window
#   center[0] = 300.0
#   sz = yt.SlicePlot( df.ds, cut_axis, field, center=center, origin='native', data_source=ad, width=(300,120)  )

#   ! cut cylinder shape region 
#   ! center: coordinate at the center of cylinder shape region
#
#   normal_vector = [-1.0, 0.0, 0.0]  
#   radius = 0.7
#   height = 1.0 
#   center[0] = center[0] - 1.5 * df.ds.length_unit
#  
#   cylinder=df.ds.disk(center, normal_vector, radius, height)
#   center = df.ds.domain_center
#   center[2] = origin
#   sz = yt.SlicePlot( df.ds, cut_axis, field, center=center, origin='native', data_source=cylinder )



#   ! set the range of color bar
   sz.set_zlim( field, 'min', 'max')
#   sz.set_zlim( field, 4e-28, 1e-23)

#   ! set figure size
#   sz.set_figure_size(150)

#   ! set linear scale around zero
#   sz.set_log( field, log, linthresh=1e-10 )
   sz.set_log( field, log )

#   ! zoom in
   sz.zoom(zoom)


   if cut_axis == 'x':
     x='%0.3f'% center[0]
     cut_plane ='x_'+x.zfill(8)
   elif cut_axis == 'y':
     y='%0.3f'% center[1]
     cut_plane ='y_'+y.zfill(8)
   elif cut_axis == 'z':
     z='%0.3f'% center[2]
     cut_plane ='z_'+z.zfill(8)

   sz.annotate_title('slice (' + cut_plane + ') ' + pwd[-1])
   sz.set_font({'weight':'bold', 'size':'22'})

#  ! annote velocity vectors
#   sz.annotate_velocity(factor = 16, normalize=False)
#  ! annotate streamlines
#   sz.annotate_streamlines('velocity_x', 'velocity_y')

#  ! annotate straight line
# for line_x in range(50,95,5):
#   sz.annotate_line((line_x, 0, 20), (line_x, 40, 20), coord_system='data')

   df.ds["Unit_L"]*df.ds.length_unit
   UNIT_T = df.ds["Unit_T"]*df.ds.time_unit


   sz.annotate_timestamp( time_unit='code_time', corner='upper_right', time_format='t = {time:.4f} kpc/$c$', text_args={'color':'black'})
   sz.set_cmap( field, colormap )
   sz.set_unit( field, unit )
   sz.set_axes_unit( 'kpc' )

   if grid:
    sz.annotate_grids()
#   sz.annotate_quiver()
#   sz.annotate_line((70,80),(70,0), coord_system='plot')
#   sz.annotate_streamlines('momentum_y','momentum_z')
#   sz.save( mpl_kwargs={"dpi":dpi} )
#   sz.save( name='Data_%06d_' %idx_start + cut_plane, suffix='eps' )
   sz.save( name='Data_%06d_' %df.ds["DumpID"] + str(cut_plane), suffix='png' )

   if N_cut > 1:
    origin += np.fabs(start_cut-end_cut)/N_cut
   else:
    origin += end_cut + 1

t1 = time.time()

print("BigStuff took %.5e sec" % (t1 - t0))
