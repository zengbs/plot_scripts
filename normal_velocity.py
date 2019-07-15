import argparse
import sys
import yt
import numpy as np
import yt.visualization.eps_writer as eps
import derived_field as df
import time
from numpy import linalg as LA

df.ds = yt.load('Data_000001')

# add new derived field
df.ds.add_field( ("gamer", 'Lorentz_factor')  , function=df._lorentz_factor  , sampling_type="cell", units='' )
df.ds.add_field( ("gamer", '4-velocity_x')    , function=df._4_velocity_x    , sampling_type="cell", units='code_length/code_time' )
df.ds.add_field( ("gamer", '4-velocity_y')    , function=df._4_velocity_y    , sampling_type="cell", units='code_length/code_time' )
df.ds.add_field( ("gamer", '4-velocity_z')    , function=df._4_velocity_z    , sampling_type="cell", units='code_length/code_time' )
   
# df.ds.add_gradient_fields(("gamer",field))
df.ds.periodicity = (True, True, True)

ad = df.ds.all_data()
# cr = ad.cut_region(["obj['Lorentz_factor'] >= 10.0"])
#surf = df.ds.surface(ad, 'Lorentz_factor', 1.0)

vertice1, Ux = ad.extract_isocontours('Lorentz_factor', 10.5, sample_values='4-velocity_x')
vertice2, Uy = ad.extract_isocontours('Lorentz_factor', 10.5, sample_values='4-velocity_y')
vertice3, Uz = ad.extract_isocontours('Lorentz_factor', 10.5, sample_values='4-velocity_z')

vector1 = vertice1[1::3,:] - vertice1[::3,:]
vector2 = vertice1[2::3,:] - vertice1[::3,:]

normal = np.cross(vector1,vector2)

U = np.vstack((Ux, Uy, Uz))
U = np.transpose(U)
U = U.to_ndarray()

NormalDotU = np.sum(U * normal, axis=1)


NormSquare = LA.norm( normal, axis=1 )**2


NormalVelocity = np.transpose( [NormalDotU / NormSquare] ) * normal



print ("vector1--------------------")
print ( vector1 )
print("ndim:{0}".format(vector1.ndim))
print("shape:{0}".format(vector1.shape))
print ("vector2--------------------")
print ( vector2 )
print("ndim:{0}".format(vector2.ndim))
print("shape:{0}".format(vector2.shape))
print ("normal--------------------")
print ( normal )
print("ndim:{0}".format(normal.ndim))
print("shape:{0}".format(normal.shape))
print ( "Ux--------------------" )
print ( Ux )
print ( "Uy--------------------" )
print ( Uy )
print ( "Uz--------------------" )
print ( Uz )
print("ndim:{0}".format(Uz.ndim))
print("shape:{0}".format(Uz.shape))
print ("U--------------------")
print ( U )
print("ndim:{0}".format(U.ndim))
print("shape:{0}".format(U.shape))
print ("NormalDotU--------------------")
print ( NormalDotU )
print("ndim:{0}".format(NormalDotU.ndim))
print("shape:{0}".format(NormalDotU.shape))
print ("NormSquare--------------------")
print ( NormSquare )
print("ndim:{0}".format(NormSquare.ndim))
print("shape:{0}".format(NormSquare.shape))
print ("NormalVelocity--------------------")
print ( NormalVelocity )
print("ndim:{0}".format(NormalVelocity.ndim))
print("shape:{0}".format(NormalVelocity.shape))
