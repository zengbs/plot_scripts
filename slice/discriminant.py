import argparse
import sys
import yt

def _discriminant(field, data):
    Engy_unit = ds.mass_unit / ( ds.length_unit * ds.time_unit**2 )
    Dens_unit = ds.mass_unit / ( ds.length_unit**3 )
    Mom_unit  = ds.mass_unit / ( ds.time_unit * ds.length_unit**2 )
    A = data["Engy"]**2 / (Engy_unit**2)
    if ds["Conserved_Engy"]  == 1:
      B = - data["Dens"]**2 / ( Dens_unit**2 )
    elif ds["Conserved_Engy"] == 2:
      B = 2 * data["Engy"] * data["Dens"] / ( Engy_unit * Dens_unit )
    C = (data["MomX"]**2 + data["MomY"]**2 + data["MomZ"]**2) / ( Mom_unit**2 )
    return A+B+C


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

field       = 'discriminant'    # to change the target field, one must modify set_unit() accordingly
center_mode = 'c'
dpi         = 150


yt.enable_parallelism()

ts = yt.load( [ prefix+'/Data_%06d'%idx for idx in range(idx_start, idx_end+1, didx) ] )

for ds in ts.piter():

# add new derived field
   ds.add_field( ("gamer", "discriminant")     , function=_discriminant  , sampling_type="cell", units="" )

   sz = yt.SlicePlot( ds, 'z', field, center_mode  )
   sz.set_zlim( field, 'min', 'max')
#   sz.set_log( field, False )
   sz.set_cmap( field, colormap )
   sz.set_unit( field, '' ) # for energy, pressure
   sz.set_axes_unit( 'code_length' )
   sz.set_xlabel('x (grid)')
   sz.set_ylabel('y (grid)')
   sz.annotate_title('slice plot')
   sz.set_font({'weight':'bold', 'size':'22'})
   sz.annotate_timestamp( time_unit='code_time', corner='upper_right', time_format='t = {time:.2f} grid$/c$', text_args={'color':'black'}
#   #sz.annotate_grids( periodic=False )
   sz.save( mpl_kwargs={"dpi":dpi} )
