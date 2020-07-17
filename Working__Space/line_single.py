import yt
import matplotlib.pyplot as plt 
import numpy as np
from matplotlib.ticker import MultipleLocator
import matplotlib.font_manager as font_manager

import derived_field as df
import unit

FileName  = 'Profile'
DataName1 = '/projectZ/tseng/product__BlastWave_Triaxial/Data_000005'
DataName2 = '/projectZ/tseng/product__BlastWave_spherical/Data_000005'

font = {'family': 'monospace','color': 'black', 'weight': 'heavy', 'size': 20}

# Start point
Xs1 = 1.0
Ys1 = 1.0
Zs1 = 0.0

#End point
Xe1 = 0.0
Ye1 = 0.0
Ze1 = 1.0

# Start point
Xs2 = 1.0
Ys2 = 1.0
Zs2 = 0.0

#End point
Xe2 = 0.0
Ye2 = 0.0
Ze2 = 1.0


StartCoord1 = [Xs1, Ys1, Zs1]
EndCoord1  = [Xe1, Ye1, Ze1] 
NumPts1    = 2048
Field1 = 'Lorentz_factor'

StartCoord2 = [Xs2, Ys2, Zs2]
EndCoord2  = [Xe2, Ye2, Ze2] 
NumPts2    = 2048
Field2 = 'Lorentz_factor'

f, ax = plt.subplots( 1, 1, sharex=False, sharey=False )

df.ds1 = yt.load(DataName1)
df.ds2 = yt.load(DataName2)

function, units = unit.ChooseUnit(Field1)
function, units = unit.ChooseUnit(Field2)

df.ds1.add_field(("gamer", Field1), function=function, sampling_type="cell", units=units)
df.ds2.add_field(("gamer", Field1), function=function, sampling_type="cell", units=units)

my_ray1 = yt.LineBuffer(df.ds1,StartCoord1, EndCoord1, NumPts1)
my_ray2 = yt.LineBuffer(df.ds2,StartCoord2, EndCoord2, NumPts2)


StartCoord1[0] *= df.ds1.length_unit 
StartCoord1[1] *= df.ds1.length_unit 
StartCoord1[2] *= df.ds1.length_unit 

StartCoord2[0] *= df.ds1.length_unit 
StartCoord2[1] *= df.ds1.length_unit 
StartCoord2[2] *= df.ds1.length_unit 
             
Xe1 *= df.ds1.length_unit 
Ye1 *= df.ds1.length_unit 
Ze1 *= df.ds1.length_unit 

EndCoord1[0] *= df.ds2.length_unit 
EndCoord1[1] *= df.ds2.length_unit 
EndCoord1[2] *= df.ds2.length_unit 
             
Xe2 *= df.ds2.length_unit 
Ye2 *= df.ds2.length_unit 
Ze2 *= df.ds2.length_unit 


r1 = np.sqrt((my_ray1["x"]-StartCoord1[0])**2 + (my_ray1["y"]-StartCoord1[1])**2 + (my_ray1["z"]-StartCoord1[2])**2 )
r2 = np.sqrt((my_ray2["x"]-StartCoord2[0])**2 + (my_ray1["y"]-StartCoord2[1])**2 + (my_ray1["z"]-StartCoord2[2])**2 )
r3 = np.sqrt((my_ray2["x"]-EndCoord1[0])**2   + (my_ray2["y"]-EndCoord1[1])**2   + (my_ray2["z"]-EndCoord1[2])**2   )

ax.plot( r1, my_ray1[Field1], 'ro', ms=2, label='triaxial')
ax.plot( r2, my_ray2[Field2], 'bo', ms=2, label='spherical (r2)')
ax.plot( r3, my_ray2[Field2], 'gx', ms=2, label='spherical (r3)')

ax.legend(loc='upper right', fontsize=8)

#ax.set_yscale('log')

plt.show()
