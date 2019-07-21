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

parser.add_argument( '-f',  action='store', required=True,  type=str,   dest='field',     help='pressure, 4-velocity_x/y/z, Lorentz_factor' )
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

if field == 'proper_number_density':
      unit= '1/code_length**3'
      function=df._proper_number_density
if field == 'temperature_sr':
      unit= ''
      function=df._temperature_sr
if field == 'Lorentz_factor':
      unit = ''
      function=df._lorentz_factor
if field == 'pressure_sr':
      unit= 'code_mass/(code_length*code_time**2)'
      function=df._pressure_sr
if field == '4-velocity_x':
      unit= 'code_length/code_time'
      function=df._4-velocity_x
if field == '4-velocity_y':
      unit= 'code_length/code_time'
      function=df._4-velocity_y
if field == '4-velocity_z':
      unit= 'code_length/code_time'
      function=df._4-velocity_z
if field == 'specific_enthalpy_sr':
      unit= ''
      function=df._specific_enthalpy_sr
if field == 'total_energy_per_volume':
      unit = 'code_mass/(code_length*code_time**2)'
if field == 'number_density_sr':
      unit = '1/code_length**3'
      function=df._number_density_sr
if field in ('momentum_x', 'momentum_y', 'momentum_z'):
        unit = 'code_mass/(code_time*code_length**2)'
if field == 'thermal_energy_density_sr':
      unit= 'code_mass/(code_length*code_time**2)'
      function=df._thermal_energy_density_sr
if field == 'kinetic_energy_density_sr':
      unit= 'code_mass/(code_length*code_time**2)'
      function=df._kinetic_energy_density_sr
if field == 'Bernoulli_constant':
      unit= ''
      function=df._Bernoulli_const
if field == 'spherical_radial_4velocity':
      unit= 'code_length/code_time'
      function=df._spherical_radial_4velocity
if field == 'cylindrical_radial_4velocity':
      unit= 'code_length/code_time'
      function=df._cylindrical_radial_4velocity
if field == '3-velocity_x':
      unit= 'code_length/code_time'
      function=df._3-velocity_x
if field == '3-velocity_y':
      unit= 'code_length/code_time'
      function=df._3-velocity_y
if field == '3-velocity_z':
      unit= 'code_length/code_time'
      function=df._3-velocity_z
if field == 'isentropic_constant':
      unit = ''
      function=df._isentropic_constant
if field == 'sound_speed':
      unit = 'code_length/code_time'
      function=df._sound_speed
if field == 'threshold':
      unit = ''
      function=df._threshold


t0 = time.time()

yt.enable_parallelism()

ts = yt.load( [ prefix+'/Data_%06d'%idx for idx in range(idx_start, idx_end+1, didx) ] )


for df.ds in ts.piter():

# take note
 if df.ds["EoS"] == 2:
   print ('%s %.6f %s' % ('Equation of state: constant gamma (', df.ds["Gamma"], ')\n'))
 elif df.ds["EoS"] == 1:
   print ('%s' % ('Equation of state: Synge\n'))
 else:
   print ("Your EoS doesn't support yet!\n")
   sys.exit(0)
 
# add new derived field
 if field not in ( 'total_energy_per_volume', 'momentum_x', 'momentum_y', 'momentum_z' ):
   df.ds.add_field( ("gamer", 'specific_enthalpy_sr')  , function=df._specific_enthalpy_sr  , sampling_type="cell", units='' )
   df.ds.add_field( ("gamer", '4_velocity_x')  , function=df._4_velocity_x  , sampling_type="cell", units='code_length/code_time' )
   df.ds.add_field( ("gamer", '4_velocity_y' ) , function=df._4_velocity_y  , sampling_type="cell", units='code_length/code_time' )
   df.ds.add_field( ("gamer", '4_velocity_z' ) , function=df._4_velocity_z  , sampling_type="cell", units='code_length/code_time' )
   df.ds.add_field( ("gamer", field)  , function=function  , sampling_type="cell", units=unit )

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
     
   

#   if ( field in ( '4-velocity_x' ,'4-velocity_y' ,'4-velocity_z', 'momentum_x', 'momentum_y', 'momentum_z', 'kinetic_energy_density' )):
#     cr=ad.cut_region(["obj['kinetic_energy_density'] > 0.0"])
#   else:
#     cr=ad.clone()


   sz = yt.SlicePlot( df.ds, cut_axis, field, center=center, origin='native', data_source=ad  )
#   sz.set_zlim( field, 81.97, 82)
#   sz.set_zlim( field, 'min', 'max')

#   sz.set_log( field, log, linthresh=1e-4 )
   sz.set_log( field, log )

   sz.zoom(zoom)


   if cut_axis == 'x':
     sz.set_xlabel('y (grid)')
     sz.set_ylabel('z (grid)')
     x='%0.3f'% center[0]
     cut_plane ='x_'+x.zfill(8)
   elif cut_axis == 'y':
     sz.set_xlabel('z (grid)')
     sz.set_ylabel('x (grid)')
     y='%0.3f'% center[1]
     cut_plane ='y_'+y.zfill(8)
   elif cut_axis == 'z':
     sz.set_xlabel('x (grid)')
     sz.set_ylabel('y (grid)')
     z='%0.3f'% center[2]
     cut_plane ='z_'+z.zfill(8)

   sz.annotate_title('slice (' + cut_plane + ') ' + pwd[-1])
   sz.set_font({'weight':'bold', 'size':'22'})


#   if field == 'Lorentz_factor':
#     sz.annotate_velocity(factor = 16, normalize=False)
#     sz.annotate_streamlines('velocity_x', 'velocity_y')

   sz.annotate_timestamp( time_unit='code_time', corner='upper_right', time_format='t = {time:.2f} grid$/c$', text_args={'color':'black'})
   sz.set_cmap( field, colormap )
   sz.set_unit( field, unit )
   sz.set_axes_unit( 'code_length' )

   if grid:
    sz.annotate_grids()
#   sz.annotate_quiver()
#   sz.annotate_line((70,80),(70,0), coord_system='plot')
#    sz.annotate_streamlines('momentum_y','momentum_z')
#   sz.save( mpl_kwargs={"dpi":dpi} )
#   sz.save( name='Data_%06d_' %idx_start + cut_plane, suffix='eps' )
   sz.save( name='Data_%06d_' %df.ds["DumpID"] + str(cut_plane), suffix='png' )

   if N_cut > 1:
    origin += np.fabs(start_cut-end_cut)/N_cut
   else:
    origin += end_cut + 1

t1 = time.time()

print("BigStuff took %.5e sec" % (t1 - t0))
