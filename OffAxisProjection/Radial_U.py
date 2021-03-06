import argparse
import sys
import yt
import numpy as np

PI            = 3.14159265
theta         = 90.0 # polar angle     (degree)
phi           = 3.0 # azimuthal angle (degree)
normal        = [np.sin(theta*PI/180.0)*np.cos(phi*PI/180.0), np.sin(theta*PI/180.0)*np.sin(phi*PI/180.0), np.cos(theta*PI/180.0)]

# define 4-velocity field
def _Ur_sr( field, data ):
   if ds["EoS"] == 2:
     h = 1.0 + ds["Gamma"] * data["Temp"] / ( ds["Gamma"] - 1.0 )
   elif ds["EoS"] == 1:
     h = 2.5*data["Temp"]+np.sqrt(2.25*data["Temp"]**2+1.0)
   else:
     print ("Your EoS isn't supported yet!")
   Ux = data["MomX"]/(data["Dens"]*h)
   Uy = data["MomY"]/(data["Dens"]*h)
   Uz = data["MomZ"]/(data["Dens"]*h)
   global normal
   cos_alpah = normal[0] / np.sqrt(normal[0]**2 + normal[1]**2 + normal[2]**2)
   cos_beta  = normal[1] / np.sqrt(normal[0]**2 + normal[1]**2 + normal[2]**2)
   cos_gamma = normal[2] / np.sqrt(normal[0]**2 + normal[1]**2 + normal[2]**2)
   Ur = cos_alpah * Ux + cos_beta * Uy + cos_gamma * Uz
   return Ur


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


idx_start     = args.idx_start
idx_end       = args.idx_end
didx          = args.didx
prefix        = args.prefix

colormap      = 'arbre'

field         = '4-velocity_r'    # to change the target field, one must modify set_unit() accordingly
center        = 'c'
dpi           = 150

width         = [40,20]
north_vector  = [ 0, 0, 1]


yt.enable_parallelism()

ts = yt.load( [ prefix+'/Data_%06d'%idx for idx in range(idx_start, idx_end+1, didx) ] )

for ds in ts.piter():

# add new derived field
   ds.add_field( ("gamer", "4-velocity_r")  , function=_Ur_sr  , sampling_type="cell", units="code_length/code_time" )

   sz = yt.OffAxisProjectionPlot( ds, normal, field, center, width, north_vector=north_vector)
   sz.annotate_title(r'$\theta = %.2f^\circ, \phi=%.2f^\circ$' %(theta, phi))
#   sz.set_zlim( field, -1.0e+3, 1.0e+3)
   sz.set_log( field, False )
   sz.set_cmap( field, colormap )
   sz.set_unit( field, 'code_length**2/code_time' ) # for energy, pressure
   sz.set_axes_unit( 'code_length' )
   sz.annotate_timestamp( time_unit='code_time', corner='upper_right', time_format='t = {time:.4f} {units}' )
#   #sz.annotate_grids( periodic=False )
   sz.save( mpl_kwargs={"dpi":dpi} )
