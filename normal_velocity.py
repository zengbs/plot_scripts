import yt
import numpy as np
import derived_field as df
from numpy import linalg as LA
import matplotlib.pyplot as plt

df.ds = yt.load('Data_000001')

# add new derived field
df.ds.add_field( ("gamer", 'Lorentz_factor')  , function=df._lorentz_factor  , sampling_type="cell", units='' )
df.ds.add_field( ("gamer", '4-velocity_x')    , function=df._4_velocity_x    , sampling_type="cell", units='code_length/code_time' )
df.ds.add_field( ("gamer", '4-velocity_y')    , function=df._4_velocity_y    , sampling_type="cell", units='code_length/code_time' )
df.ds.add_field( ("gamer", '4-velocity_z')    , function=df._4_velocity_z    , sampling_type="cell", units='code_length/code_time' )
   
df.ds.periodicity = (True, True, True)

ad = df.ds.all_data()

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

NormalLorentzFactor = np.sqrt( 1.0 + np.sum ( NormalVelocity**2, axis=1 ) )

#########################################################

UniqueVertice = np.unique(vertice1, axis=0)

IdxVertice = np.zeros(vertice1.shape[0])

for idx in range(vertice1.shape[0]):
    IdxVertice[idx:idx+1] = UniqueVertice.tolist().index(vertice1[idx:idx+1,:].tolist()[0])

IdxVertice.shape = (int(IdxVertice.shape[0]/3), 3)

IdxVertice.astype(int)

#########################################################

colormap = plt.get_cmap('jet')

NomalizationConst = 1.0/( np.amax(NormalLorentzFactor)-np.amin(NormalLorentzFactor) )

RGB = colormap(NormalLorentzFactor*NomalizationConst)*255

RGB = RGB.astype(int)

RGB = np.delete(RGB, 3, 1)

#########################################################

print ("RGB--------------------")
print ( RGB )
print("ndim:{0}".format(RGB.ndim))
print("shape:{0}".format(RGB.shape))
print ("IdxVertice--------------------")
print ( IdxVertice )
print("ndim:{0}".format(IdxVertice.ndim))
print("shape:{0}".format(IdxVertice.shape))
print ("UniqueVertice--------------------")
print ( UniqueVertice )
print("ndim:{0}".format(UniqueVertice.ndim))
print("shape:{0}".format(UniqueVertice.shape))
print ("vertice1--------------------")
print ( vertice1 )
print("ndim:{0}".format(vertice1.ndim))
print("shape:{0}".format(vertice1.shape))
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
print ("NormalLorentzFactor--------------------")
print ( NormalLorentzFactor )
print("ndim:{0}".format(NormalLorentzFactor.ndim))
print("shape:{0}".format(NormalLorentzFactor.shape))


