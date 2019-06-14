import argparse
import sys
import yt
import numpy as np

x_shift = 0.0
y_shift = 0.0
z_shift = 0.0

cut_plane='z'

####################  ON-DISK DATA  ###############################

# define 4-velocity field
def _Uz_sr( field, data ):
   if ds["EoS"] == 2:
     h = 1.0 + ds["Gamma"] * data["Temp"] / ( ds["Gamma"] - 1.0 )
   elif ds["EoS"] == 1:
     h = 2.5*data["Temp"]+np.sqrt(2.25*data["Temp"]**2+1.0)
   else:
     print ("Your EoS doesn't support yet!")
   Uz = data["MomZ"]/(data["Dens"]*h)
   return Uz

####################  DERIVED DATA  ############################


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

field       = '4-velocity_z'    # to change the target field, one must modify set_unit() accordingly
center_mode = 'c'
dpi         = 150


yt.enable_parallelism()

ts = yt.load( [ prefix+'/Data_%06d'%idx for idx in range(idx_start, idx_end+1, didx) ] )

for ds in ts.piter():
   center = ds.domain_center

   x_center = center[0] + x_shift*ds.length_unit
   y_center = center[1] + y_shift*ds.length_unit
   z_center = center[2] + z_shift*ds.length_unit

# add new derived field
   ds.add_field( ("gamer", "4-velocity_z")  , function=_Uz_sr  , sampling_type="cell", units="code_length/code_time" )

   sz = yt.SlicePlot( ds, cut_plane, field, center=(x_center,y_center,z_center), origin='native'  )
   sz.set_zlim( field, 'min', 'max')
#   sz.set_log( field, False )
#   sz.zoom(2)
   sz.set_cmap( field, colormap )
   sz.set_unit( field, 'code_length/code_time' ) # for energy, pressure
   sz.set_axes_unit( 'code_length' )
   sz.set_xlabel('x (grid)')
   sz.set_ylabel('y (grid)')
   sz.annotate_title('slice plot')
   sz.set_font({'weight':'bold', 'size':'22'})
   sz.annotate_timestamp( time_unit='code_time', corner='upper_right', time_format='t = {time:.2f} grid$/c$', text_args={'color':'black'})
#   #sz.annotate_grids( periodic=False )
   sz.save( mpl_kwargs={"dpi":dpi} )
