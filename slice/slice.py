import argparse
import sys
import yt
import numpy as np
import yt.visualization.eps_writer as eps

def _pressure_sr( field, data ):
   if ds["EoS"] == 2:
     h = 1.0 + ds["Gamma"] * data["Temp"] / ( ds["Gamma"] - 1.0 )
   elif ds["EoS"] == 1:
     h = 2.5*data["Temp"]+np.sqrt(2.25*data["Temp"]**2+1.0)
   else:
     print ("Your EoS doesn't support yet!")
   Ux = data["MomX"]/(data["Dens"]*h)
   Uy = data["MomY"]/(data["Dens"]*h)
   Uz = data["MomZ"]/(data["Dens"]*h)
   factor = np.sqrt(1*(ds.length_unit/ds.time_unit)**2 + Ux**2 + Uy**2 + Uz**2)
   density = data["Dens"]/factor # proper number density
   pres = density * data["Temp"]
   return pres*ds.length_unit**3/(ds.time_unit**3)

def _proper_number_density( field, data ):
   if ds["EoS"] == 2:
     h = 1.0 + ds["Gamma"] * data["Temp"] / ( ds["Gamma"] - 1.0 )
   elif ds["EoS"] == 1:
     h = 2.5*data["Temp"]+np.sqrt(2.25*data["Temp"]**2+1.0)
   else:
     print ("Your EoS is not supported yet!")
   Ux = data["MomX"]/(data["Dens"]*h)
   Uy = data["MomY"]/(data["Dens"]*h)
   Uz = data["MomZ"]/(data["Dens"]*h)
   factor = np.sqrt(1*(ds.length_unit/ds.time_unit)**2 + Ux**2 + Uy**2 + Uz**2)
   density = data["Dens"]/factor
   return density*ds.length_unit/(ds.mass_unit*ds.time_unit)

def _lorentz_factor( field, data ):
   if ds["EoS"] == 2:
     h = 1.0 + ds["Gamma"] * data["Temp"] / ( ds["Gamma"] - 1.0 )
   elif ds["EoS"] == 1:
     h = 2.5*data["Temp"]+np.sqrt(2.25*data["Temp"]**2+1.0)
   else:
     print ("Your EoS doesn't support yet!")
   Ux = data["MomX"]/(data["Dens"]*h)
   Uy = data["MomY"]/(data["Dens"]*h)
   Uz = data["MomZ"]/(data["Dens"]*h)
   factor = np.sqrt(1*(ds.length_unit/ds.time_unit)**2 + Ux**2 + Uy**2 + Uz**2)
   return factor*(ds.time_unit/ds.length_unit)

def _Ux_sr( field, data ):
   if ds["EoS"] == 2:
     h = 1.0 + ds["Gamma"] * data["Temp"] / ( ds["Gamma"] - 1.0 )
   elif ds["EoS"] == 1:
     h = 2.5*data["Temp"]+np.sqrt(2.25*data["Temp"]**2+1.0)
   else:
     print ("Your EoS doesn't support yet!")
   Ux = data["MomX"]/(data["Dens"]*h)
   return Ux


def _Uy_sr( field, data ):
   if ds["EoS"] == 2:
     h = 1.0 + ds["Gamma"] * data["Temp"] / ( ds["Gamma"] - 1.0 )
   elif ds["EoS"] == 1:
     h = 2.5*data["Temp"]+np.sqrt(2.25*data["Temp"]**2+1.0)
   else:
     print ("Your EoS doesn't support yet!")
   Uy = data["MomY"]/(data["Dens"]*h)
   return Uy

def _Uz_sr( field, data ):
   if ds["EoS"] == 2:
     h = 1.0 + ds["Gamma"] * data["Temp"] / ( ds["Gamma"] - 1.0 )
   elif ds["EoS"] == 1:
     h = 2.5*data["Temp"]+np.sqrt(2.25*data["Temp"]**2+1.0)
   else:
     print ("Your EoS doesn't support yet!")
   Uz = data["MomZ"]/(data["Dens"]*h)
   return Uz

def _enthalpy( field, data ):
   if ds["EoS"] == 2:
     h = 1.0 + ds["Gamma"] * data["Temp"] / ( ds["Gamma"] - 1.0 )
   elif ds["EoS"] == 1:
     h = 2.5*data["Temp"]+np.sqrt(2.25*data["Temp"]**2+1.0)
   else:
     print ("Your EoS doesn't support yet!")
   return h

def _number_density(field, data):
   return data["Dens"]/ds.mass_unit



# load the command-line parameters
parser = argparse.ArgumentParser( description='Plot slices for sr-hydro' )

parser.add_argument( '-f', action='store',  required=True,  type=str,   dest='field',     help='pressure, 4-velocity_x/y/z, Lorentz_factor' )
parser.add_argument( '-p', action='store',  required=True,  type=str,   dest='cut_axis',  help='axis you want to cut' )
parser.add_argument( '-sx', action='store', required=True,  type=float, dest='start_cut',  help='start cut' )
parser.add_argument( '-ex', action='store', required=True,  type=float, dest='end_cut',   help='end cut' )
parser.add_argument( '-nx', action='store', required=True,  type=float, dest='N_cut',     help='number of cuts between -sx and -ex' )
parser.add_argument( '-st', action='store', required=True,  type=int,   dest='idx_start', help='first data index' )
parser.add_argument( '-et', action='store', required=True,  type=int,   dest='idx_end',   help='last data index' )
parser.add_argument( '-dt', action='store', required=False, type=int,   dest='didx',      help='delta data index [%(default)d]', default=1 )
parser.add_argument( '-i', action='store',  required=False, type=str,   dest='prefix',    help='data path prefix [%(default)s]', default='./' )
parser.add_argument( '-z', action='store',  required=True,  type=int,   dest='zoom',      help='zoom in' )
parser.add_argument( '-l', action='store',  required=True,  type=int,  dest='log',       help='log scale' )
parser.add_argument( '-g', action='store',  required=True,  type=int,  dest='grid',      help='grids' )

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


if ( field == '4-velocity_x' or field == '4-velocity_y' or field == '4-velocity_z' ) and log:
   print('log scale should be disabled!\n')
   sys.exit(0)


if field == 'proper_number_density':
      unit= '1/code_length**3'
      function=_proper_number_density
if field == 'Lorentz_factor':
      unit = ''
      function=_lorentz_factor
if field == 'pressure':
      unit= "code_mass/(code_length*code_time**2)"
      function=_pressure_sr
if field == '4-velocity_x':
      unit= "code_length/code_time"
      function = _Ux_sr
if field == '4-velocity_y':
      unit= "code_length/code_time"
      function=_Uy_sr
if field == '4-velocity_z':
      unit= 'code_length/code_time'
      function=_Uz_sr
if field == 'enthalpy':
      unit= ''
      function=_enthalpy
if field == 'energy_per_volume':
      unit = 'code_mass/(code_length*code_time**2)'
if field == 'number_density':
      unit = '1/code_length**3'
      function=_number_density
if field in ('momentum_x', 'momentum_y', 'momentum_z'):
        unit = 'code_mass/(code_time*code_length**2)'

yt.enable_parallelism()

ts = yt.load( [ prefix+'/Data_%06d'%idx for idx in range(idx_start, idx_end+1, didx) ] )


for ds in ts.piter():

 origin = start_cut

 while origin <= end_cut:
   center = ds.domain_center

   if cut_axis == 'x':
     center[0] = origin
   elif cut_axis == 'y':
     center[1] = origin
   elif cut_axis == 'z':
     center[2] = origin
   
# add new derived field
   if  field != 'momentum_x' or  field != 'momentum_y' or  field != 'momentum_z' or  field != 'energy_per_volume':
   ds.add_field( ("gamer", field)  , function=function  , sampling_type="cell", units=unit )

   sz = yt.SlicePlot( ds, cut_axis, field, center=center, origin='native'  )
   sz.set_zlim( field, 'min', 'max')

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

   sz.annotate_title('slice plot (' + cut_plane + ')')
   sz.set_font({'weight':'bold', 'size':'22'})


   if field == 'g':
     sz.annotate_velocity(factor = 16, normalize=True)

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
   sz.save( name='Data_%06d_' %idx_start + str(cut_plane), suffix='png' )

   origin += np.fabs(start_cut-end_cut)/N_cut
