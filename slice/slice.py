import argparse
import sys
import yt
import numpy as np

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

def _number_density( field, data ):
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

parser.add_argument
( '-f', action='store',  required=True,  type=str,   dest='field',     help='field you want to plot' )
parser.add_argument
( '-p', action='store',  required=True,  type=str,   dest='cut_axis',  help='axis you want to cut' )
parser.add_argument
( '-sx', action='store', required=True,  type=float, dest='sart_cut',  help='start cut' )
parser.add_argument
( '-ex', action='store', required=True,  type=float, dest='end_cut',   help='end cut' )
parser.add_argument
( '-nx', action='store', required=True,  type=int,   dest='N_cut',     help='number of cuts between -sx and -ex' )
parser.add_argument
( '-st', action='store', required=True,  type=int,   dest='idx_start', help='first data index' )
parser.add_argument
( '-et', action='store', required=True,  type=int,   dest='idx_end',   help='last data index' )
parser.add_argument
( '-dt', action='store', required=False, type=int,   dest='didx',      help='delta data index [%(default)d]', default=1 )
parser.add_argument
( '-i', action='store',  required=False, type=str,   dest='prefix',    help='data path prefix [%(default)s]', default='./' )
parser.add_argument
( '-o', action='store',  required=True,  type=int,   dest='zoom',      help='zoom in' )
parser.add_argument
( '-l', action='store',  required=True,  type=bool,  dest='log',       help='log scale' )
parser.add_argument
( '-g', action='store',  required=True,  type=bool,  dest='grid',      help='grids' )

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
log         = args.l

colormap    = 'arbre'

dpi         = 150

if   field is 'proper_number_density':
        unit= '1/code_length**3'
        function='_number_density'
elif field is 'Lorentz_factor':
        unit = ''
        function='_lorentz_factor'
elif field is 'pressure':
        unit= 'code_mass/(code_length*code_time**2)'
        function='_pressure_sr'
elif field is '4-velocity_x':
        unit= 'code_length/code_time'
        function='_Ux_sr'
elif field is '4-velocity_y':
        unit= 'code_length/code_time'
        function='_Uy_sr'
elif field is '4-velocity_z':
        unit= 'code_length/code_time'
        function='_Uz_sr'
elif field is 'enthalpy':
        unit= ''
        function='_enthalpy'
elif field is 'energy_per_volume':
        unit = 'code_mass/(code_length*code_time**2)'
        function=''
elif field is 'number_density':
        unit = '1/code_length**3'
        function='_number_density'
elif field in ('momentum_x', 'momentum_y', 'momentum_z'):
        unit = 'code_mass/(code_time*code_length**2)'

yt.enable_parallelism()

ts = yt.load( [ prefix+'/Data_%06d'%idx for idx in range(idx_start, idx_end+1, didx) ] )

for ds in ts.piter():
center = ds.domain_center

x_shift = y_shift = z_shift = 0.0

 for shift in np.arange(start_cut, end_cut, (start_cut-end_cut)/N_cut):

   if   cut_axis is 'x'
     x_shift = shift
   elif cut_axis is 'y'
     y_shift = shift 
   elif cut_axis is 'z'
     z_shift = shift 
   
   center[0] += x_shift*ds.length_unit
   center[1] += y_shift*ds.length_unit
   center[2] += z_shift*ds.length_unit

# add new derived field
   ds.add_field( ("gamer", field)  , function=_number_density  , sampling_type="cell", unit=unit )

   sz = yt.SlicePlot( ds, cut_axis, field, center=center, origin='native'  )
   sz.set_zlim( field, 'min', 'max')
   sz.set_log( field, log )
   sz.zoom(zoom)

   if cut_axis is 'x':
     sz.set_xlabel('y (grid)')
     sz.set_ylabel('z (grid)')
     cut_plane ='x='+ str('%3.3f'center[0])
   elif cut_axis is 'y':
     sz.set_xlabel('z (grid)')
     sz.set_ylabel('x (grid)')
     cut_plane ='y='+ str('%3.3f'center[1])
   elif cut_axis is 'z':
     sz.set_xlabel('x (grid)')
     sz.set_ylabel('y (grid)')
     cut_plane ='z='+ str('%3.3f'center[2])

   sz.annotate_title('slice plot (' + cut_plane + ')')
   sz.set_font({'weight':'bold', 'size':'22'})

   if field is 'g'
     sz.annotate_velocity(factor = 16, normalize=True)

   sz.annotate_timestamp( time_unit='code_time', corner='upper_right', time_format='t = {time:.2f} grid$/c$', text_args={'color':'black'})
   sz.set_cmap( field, colormap )
   sz.set_unit( field, unit )
   sz.set_axes_unit( 'code_length' )
   sz.annotate_grids( periodic=grid )
#   sz.annotate_line((70,80),(70,0), coord_system='plot')
#   sz.save( mpl_kwargs={"dpi":dpi} )
   sz.save( name='Data_%06d_' + str(cut_plane), mpl_kwargs={"dpi":dpi} )
