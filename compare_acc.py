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

Center = [5.0, 5.0, 5.0]


# theta = angle between vector and z-axis 
# phi   = angle between vector and x-axis

# center --> side
theta_1   = 90.0*np.pi/180.0
phi_1     = 0.0*np.pi/180.0
NPoints_1 = 12500 


# center --> edge
theta_2   = 90.0*np.pi/180.0
phi_2     = 45.0*np.pi/180.0
NPoints_2 = 17676

# center --> corner
theta_3   = np.arccos(1.0/np.sqrt(3.0)) 
phi_3     = 45.0*np.pi/180.0
NPoints_3 = 21649



phi     = [    phi_1,     phi_2,     phi_3]
theta   = [  theta_1,   theta_2,   theta_3]
NPoints = [NPoints_1, NPoints_2, NPoints_3]



yt.enable_parallelism()

ts = yt.load( [ prefix+'/Data_%06d'%idx for idx in range(idx_start, idx_end+1, didx) ] )

for df.ds in ts.piter():

# add new derived field
   field='gravitational_potential'

   df.ds.add_field( ("gamer", 'specific_enthalpy_sr'        ), function=df._specific_enthalpy_sr        , sampling_type="cell", units=''                      )
   df.ds.add_field( ("gamer", '4_velocity_x'                ), function=df._4_velocity_x                , sampling_type="cell", units='code_length/code_time' )
   df.ds.add_field( ("gamer", '4_velocity_y'                ), function=df._4_velocity_y                , sampling_type="cell", units='code_length/code_time' )
   df.ds.add_field( ("gamer", '4_velocity_z'                ), function=df._4_velocity_z                , sampling_type="cell", units='code_length/code_time' )
   df.ds.add_field( ("gamer", 'Lorentz_factor'              ), function=df._lorentz_factor              , sampling_type="cell", units=''                      )
   df.ds.add_field( ("gamer", '3_velocity_magnitude'        ), function=df._3_velocity_magnitude        , sampling_type="cell", units='code_length/code_time' )
   df.ds.add_field( ("gamer", 'proper_number_density'       ), function=df._proper_number_density       , sampling_type="cell", units='1/code_length**3'      )
   df.ds.add_field( ("gamer", 'pressure_sr'                 ), function=df._pressure_sr                 , sampling_type="cell", units='code_mass/(code_length*code_time**2)')
   df.ds.add_field( ("gamer", 'gravitational_potential'     ), function=df._gravitational_potential     , sampling_type="cell", units='(code_length/code_time)**2')
   
   for i in range(0,3):
#     load data from table
      FileName   = 'Input__HydrostaticEquilibrium'
      Table_ODE  = np.loadtxt( FileName,  usecols=(1,4), unpack=True, max_rows=NPoints[i] )

#     extract field stored in gamer data
      xyz = np.full((NPoints[i], 3), 0.0)

      xyz[:,0] += Center[0] + Table_ODE[0,]*np.sin(theta[i])*np.cos(phi[i])
      xyz[:,1] += Center[1] + Table_ODE[0,]*np.sin(theta[i])*np.sin(phi[i])
      xyz[:,2] += Center[2] + Table_ODE[0,]*np.cos(theta[i])

      
      for j in range(0, NPoints[i]):
         point          = xyz[j].reshape(3,1)
         point_obj      = df.ds.point(point*df.ds.length_unit)
         field_at_point = point_obj['gamer', field]
         np_ary = np.asarray(field_at_point)

         if (j is 0):
           field_gamer = np_ary
         else:
           field_gamer = np.hstack((field_gamer,np_ary))


#     field in table
      field_table    = np.asarray(Table_ODE[1,])

#     potential=(x0, x1, x2, x3), gradient=pot1-pot2, where pot1 = (x0, x1, x2), pot2=(x1, x2, x3)
      Pot1_field_table = np.delete(field_table, NPoints[i]-1)
      Pot2_field_table = np.delete(field_table,            0)

      Pot1_field_gamer = np.delete(field_gamer, NPoints[i]-1)
      Pot2_field_gamer = np.delete(field_gamer,            0)

#     compute acceleration
      gradient_field_table = Pot1_field_table - Pot2_field_table
      gradient_field_gamer = Pot1_field_gamer - Pot2_field_gamer


 
#     compute relative error
      relative_error = np.full((1, NPoints[i]-1), 1.0)
      #relative_error -= gradient_field_table/gradient_field_gamer
      relative_error -= gradient_field_gamer/gradient_field_table

#     plot
      plt.plot	( np.delete(Table_ODE[0,], 0), np.transpose(relative_error), 'ro', markersize=1.0 )
#      plt.xlim ( Table_ODE[0,0],Table_ODE[0,NPoints[i]-1] )
#      plt.yscale('log') 
#      plt.plot	(Table_ODE[0,], np.transpose(field_gamer), 'ro')
#      plt.plot	(Table_ODE[0,], np.transpose(field_table), 'bo')
      FigName = 'relative_error_potential_gradient_Data_%06d_%d.png' % (df.ds["DumpID"], i)
      plt.savefig( FigName )
      plt.close()
