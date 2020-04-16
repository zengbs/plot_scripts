import yt
import matplotlib.pyplot as plt 
import numpy as np
from matplotlib.ticker import MultipleLocator
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.font_manager as font_manager
from cycler import cycler

import derived_field as df
import unit


def Spherical2Cartesian( R, theta, phi ):
    X = R * np.sin(theta) * np.cos(phi)
    Y = R * np.sin(theta) * np.sin(phi)
    Z = R * np.cos(theta)
    return X, Y, Z   


DataName = 'Data_000009'
font = {'family': 'monospace','color': 'black', 'weight': 'heavy', 'size': 20}

f, ax = plt.subplots( 1,1 )
df.ds = yt.load(DataName)
NumPts = 170
Field  = 'Lorentz_factor'
function, units = unit.ChooseUnit(Field)
df.ds.add_field(("gamer", Field), function=function, sampling_type="cell", units=units)

cm_line = plt.get_cmap('gist_rainbow')

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


NumLine_Theta = 4
NumLine_Phi   = 4 

NUM_COLORS = NumLine_Theta*NumLine_Phi

dTheta = abs( theta_e - theta_s ) / NumLine_Theta
dPhi   = abs( phi_e - phi_s     ) / NumLine_Phi

colors =[cm_line(float(i)/NUM_COLORS) for i in range(NUM_COLORS)] 
ax.set_prop_cycle(cycler('color', colors))

X = []
Y = []
Z = []
MaxGamma = []

theta = theta_s
for i in range(NumLine_Theta):

    phi   = phi_s
    for j in range(NumLine_Phi):
        print("phi=%f, theta=%f" % (phi*180/np.pi, theta*180/np.pi))

        Xs, Ys, Zs = Spherical2Cartesian( R_s, theta, phi )
        Xe, Ye, Ze = Spherical2Cartesian( R_e, theta, phi )

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
        
        Xe *= df.ds.length_unit 
        Ye *= df.ds.length_unit 
        Ze *= df.ds.length_unit 
        
        
        r = np.sqrt((my_ray["x"]-Xs)**2 + (my_ray["y"]-Ys)**2 + (my_ray["z"]-Zs)**2 )
        
        ax.plot( r, my_ray[Field], marker='o')


        MaxIdx = np.argmax(np.array(my_ray[Field]))
 
        X.append( np.array(my_ray["x"][MaxIdx]) )  
        Y.append( np.array(my_ray["y"][MaxIdx]) )
        Z.append( np.array(my_ray["z"][MaxIdx]) )

        MaxGamma.append( np.amax(np.array(my_ray[Field][MaxIdx])) )

        phi += dPhi
        
    theta += dTheta


#plt.show()
#plt.savefig("Fig__test.png")
