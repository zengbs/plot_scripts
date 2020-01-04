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
#parser.add_argument( '-i', action='store', required=False,  type=str, dest='prefix',
#                     help='data path prefix [%(default)s]', default='./' )

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
#prefix      = args.prefix


dpi         = 150

#Point1 = [ 0, 0.5, 0.5]
#Point2 = [ 1, 0.5, 0.5]
#Point1 = [0, 1.0, 1.0]
#Point2 = [2, 1.0, 1.0]
#Point1 = [0, 5.0, 5.0]
#Point2 = [10, 5.0, 5.0]
#Point1 = [0 ,  0,  0] 
#Point2 = [10, 10, 10]



# theta = angle between vector and z-axis 
# phi   = angle between vector and x-axis

##big box
#Center = [5.0, 5.0, 5.0]
## center --> side
#theta_1   = 90.0*np.pi/180.0
#phi_1     = 0.0*np.pi/180.0
#NPoints_1 = 12500 
#
#
## center --> edge
#theta_2   = 90.0*np.pi/180.0
#phi_2     = 45.0*np.pi/180.0
#NPoints_2 = 17676
#
## center --> corner
#theta_3   = np.arccos(1.0/np.sqrt(3.0)) 
#phi_3     = 45.0*np.pi/180.0
#NPoints_3 = 21649

##small box
#radius = 0.1148*0.5
#Center = [radius, radius, radius]
## center --> side
#theta_1   = 90.0*np.pi/180.0
#phi_1     = 0.0*np.pi/180.0
#NPoints_1 = 143
#
#
## center --> edge
#theta_2   = 90.0*np.pi/180.0
#phi_2     = 45.0*np.pi/180.0
#NPoints_2 = 202
#
## center --> corner
#theta_3   = np.arccos(1.0/np.sqrt(3.0)) 
#phi_3     = 45.0*np.pi/180.0
#NPoints_3 = 249
#
#
#phi     = [    phi_1,     phi_2,     phi_3]
#theta   = [  theta_1,   theta_2,   theta_3]
#NPoints = [NPoints_1, NPoints_2, NPoints_3]

#Point1 = [160, 160, 160]
#Point2 = [320, 160, 160]
Point1 = [80, 80, 80]
Point2 = [160, 80, 80]


prefix1='/projectY/tseng/gamer_jet/bin/isothermal_shpere'
prefix2='/projectY/tseng/gamer/bin/Halo'



for idx in range(idx_start, idx_end+1):

   FileName1='/Data_%06d' % (idx)
   FileName2='/Data_%06d' % (idx)

   df.ds1 = yt.load( prefix1+FileName1  )
   df.ds2 = yt.load( prefix2+FileName2  )


#  add new derived field
   field1='pressure'
   field2='pressure_sr'

   #df.ds1.add_field( ("gamer", 'proper_mass_density' ), function=df._proper_mass_density       , sampling_type="cell", units='g/cm**3'      )
   df.ds2.add_field( ("gamer",  'pressure_sr'         ), function=df._pressure_sr       , sampling_type="cell", units='g/(cm*s**2)'      )

   NPoints = 5000
   
#  It's dangerous to set x_min and x_max at boundary otherwise the points on boundary would not be found!
   ray = np.linspace(Point1[0]*1.0000001, Point2[0]*0.9999999, NPoints)

   
   for j in range(0, NPoints):
      point          = [ray[j], Point1[1], Point1[2]]

      point_obj1      = df.ds1.point(point*df.ds1.length_unit)
      field_at_point1 = point_obj1['gas', field1]
      np_ary1 = np.asarray(field_at_point1)

      point_obj2      = df.ds2.point(point*df.ds2.length_unit)
      field_at_point2 = point_obj2['gamer', field2]
      np_ary2 = np.asarray(field_at_point2)


      if (j is 0):
        field_gamer1 = np_ary1
        field_gamer2 = np_ary2
      else:
        field_gamer1 = np.hstack((field_gamer1,np_ary1))
        field_gamer2 = np.hstack((field_gamer2,np_ary2))

#  offset
   ray -= 80.0

#  plot
   plt.plot	( ray, field_gamer1, 'ro', markersize=1.0, label='Hydro' )
   plt.plot	( ray, field_gamer2, 'bx', markersize=1.0, label='SRHydro' )

   plt.legend(loc='lower left')

#  get extreme values
   x_min = np.amin(ray)
   x_max = np.amax(ray)
   plt.xlim(x_min, x_max)
   #plt.ylim(4e-28, 1e-23) # mass density

   #plt.xscale('log') 
   plt.yscale('log') 
   plt.xlabel('kpc')
   plt.ylabel('pressure (g/(cm*s**2))')
   FigName = 'Data_%06d_LinePlot_%s_ComparisonT.png' % ( df.ds1["DumpID"], field1 )
   plt.savefig( FigName )
   plt.close()
