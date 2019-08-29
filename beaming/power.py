import argparse
import sys
import yt
import numpy as np

theta         = 90.0*np.pi/180.0 # polar angle     (degree)
phi           = 20.0*np.pi/180.0 # azimuthal angle (degree)
normal        = [np.sin(theta)*np.cos(phi), np.sin(theta)*np.sin(phi), np.cos(theta)]


# define pressure field
def projected_power( field, data ):
   if ds["EoS"] == 2:
     h = 1.0 + ds["Gamma"] * data["Temp"] / ( ds["Gamma"] - 1.0 )
   elif ds["EoS"] == 1:
     h = 2.5*data["Temp"]+np.sqrt(2.25*data["Temp"]**2+1.0)
   else:
     print ("Your EoS doesn't support yet!")

   Ux = data["MomX"]/(data["Dens"]*h)
   Uy = data["MomY"]/(data["Dens"]*h)
   Uz = data["MomZ"]/(data["Dens"]*h)
   
   Usqr = Ux**2+Uy**2+Uz**2

   # Lorentz factor
   gamma = np.sqrt(1*(ds.length_unit/ds.time_unit)**2 + Usqr)

   Var = gamma - (Ux*normal[0]+Uy*normal[1]+Uz*normal[2])

   # beaming effect
   factor = Var**-4

   return factor
   



# load the command-line piarameters
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

field       = 'beaming factor'    # to change the target field, one must modify set_unit() accordingly
center      = 'c'
dpi         = 150

width         = [40,40]
north_vector  = [ 0, 0, 1]

yt.enable_parallelism()

ts = yt.load( [ prefix+'/Data_%06d'%idx for idx in range(idx_start, idx_end+1, didx) ] )

for ds in ts.piter():

# add new derived field
   ds.add_field( ("gamer", field)  , function=projected_power  , sampling_type="cell", units="code_time**4*code_length**-4" )
   sz = yt.ProjectionPlot( ds, 'z', field, center=center  )
#   sz = yt.OffAxisProjectionPlot( ds, normal, field, center, width, north_vector=north_vector)
   sz.annotate_title(r'$\theta = %.2f^\circ, \phi=%.2f^\circ$' %(theta*180.0/np.pi, phi*180.0/np.pi))
   sz.set_zlim( field, 'min', 'max')
#   sz.set_log( field, False )
   sz.set_cmap( field, colormap )
   sz.set_unit( field, 'code_time**4*code_length**-3' )
   sz.set_axes_unit( 'code_length' )
   sz.set_xlabel('x (grid)')
   sz.set_ylabel('y (grid)')
   sz.annotate_title('slice plot')
   sz.set_font({'weight':'bold', 'size':'22'})
   sz.annotate_timestamp( time_unit='code_time', corner='upper_right', time_format='t = {time:.2f} grid$/c$', text_args={'color':'black'})
#   #sz.annotate_grids( periodic=False )
   sz.save( mpl_kwargs={"dpi":dpi} )
