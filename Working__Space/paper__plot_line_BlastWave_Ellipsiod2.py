import yt
import numpy as np
import derived_field as df
import unit
from mpl_toolkits.mplot3d import Axes3D


def Spherical2Cartesian( R, theta, phi ):
    X = R * np.sin(theta) * np.cos(phi)
    Y = R * np.sin(theta) * np.sin(phi)
    Z = R * np.cos(theta)
    return X, Y, Z   


f = open("test.dat","w+")

DataName = 'Data_000009'
font = {'family': 'monospace','color': 'black', 'weight': 'heavy', 'size': 20}


df.ds = yt.load(DataName)
NumPts = 170
Field  = 'Lorentz_factor'
function, units = unit.ChooseUnit(Field)
df.ds.add_field(("gamer", Field), function=function, sampling_type="cell", units=units)

NumLine_Theta = 100
NumLine_Phi   = 200



CenterX = 0.5
CenterY = 0.5
CenterZ = 0.5

R_s     = 0.39
theta_s = 0
phi_s   = 0

R_e     = 0.41
theta_e = 180
phi_e   = 360

theta_s *= np.pi/180  
phi_s   *= np.pi/180
theta_e *= np.pi/180
phi_e   *= np.pi/180



Theta = np.linspace( theta_s, theta_e, NumLine_Theta )
Phi   = np.linspace( phi_s  , phi_e  , NumLine_Phi   )



Theta_mesh, Phi_mesh = np.meshgrid( Theta, Phi, sparse=False, indexing='ij' )

f.write( "#%19s%20s%20s%20s\n" % (  "X", "Y", "Z", "MaxGamma" ) )

for j in range(NumLine_Phi):

    for i in range(NumLine_Theta):
        print("phi=%f, theta=%f" % ( Phi_mesh[i,j]*180/np.pi,Theta_mesh[i,j]*180/np.pi))

        Xs, Ys, Zs = Spherical2Cartesian( R_s, Theta_mesh[i,j], Phi_mesh[i,j] )
        Xe, Ye, Ze = Spherical2Cartesian( R_e, Theta_mesh[i,j], Phi_mesh[i,j] )

        Xs += CenterX
        Ys += CenterY
        Zs += CenterZ
        Xe += CenterX
        Ye += CenterY
        Ze += CenterZ
        
        StarCoord = [Xs, Ys, Zs]
        EndCoord  = [Xe, Ye, Ze] 
        
        my_ray = yt.LineBuffer(df.ds,StarCoord, EndCoord, NumPts)
        
        
        Xs *= df.ds.length_unit 
        Ys *= df.ds.length_unit 
        Zs *= df.ds.length_unit 
        
        MaxIdx = np.argmax(np.array(my_ray[Field]))
 
        X        = my_ray["x"][MaxIdx] 
        Y        = my_ray["y"][MaxIdx] 
        Z        = my_ray["z"][MaxIdx] 
        MaxGamma = my_ray[Field][MaxIdx]

        f.write( "%20.7e%20.7e%20.7e%20.7e\n" % (  X, Y, Z, MaxGamma ) )
    f.write( "\n" )
    f.flush()
