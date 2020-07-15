import yt
import matplotlib.pyplot as plt 
import numpy as np
from matplotlib.ticker import MultipleLocator
import matplotlib.font_manager as font_manager

import derived_field as df
import unit


NormalizedConst_Dens = 1
NormalizedConst_Pres = 1
#FileName = 'fig__benchmark_pizdaint'
DataName = 'Data_000000'
font = {'family': 'monospace','color': 'black', 'weight': 'heavy', 'size': 20}

# Start point
Xs1 = 0.0
Ys1 = 0.0
Zs1 = 0.0

Xe1 = 1.0
Ye1 = 1.0
Ze1 = 1.0



StarCoord1 = [Xs1, Ys1, Zs1]
EndCoord1  = [Xe1, Ye1, Ze1] 
NumPts1    = 9999
#NumPts1    = 1024
NumPts2    = 32
Field1 = 'proper_mass_density'


f, ax = plt.subplots( 1, 1, sharex=False, sharey=False )

df.ds = yt.load(DataName)
function, units = unit.ChooseUnit(Field1)
df.ds.add_field(("gamer", Field1), function=function, sampling_type="cell", units=units)

my_ray1 = yt.LineBuffer(df.ds,StarCoord1, EndCoord1, NumPts1)
my_ray2 = yt.LineBuffer(df.ds,StarCoord1, EndCoord1, NumPts2)


Xs1 *= df.ds.length_unit 
Ys1 *= df.ds.length_unit 
Zs1 *= df.ds.length_unit 

Xe1 *= df.ds.length_unit 
Ye1 *= df.ds.length_unit 
Ze1 *= df.ds.length_unit 



r1 = np.sqrt((my_ray1["x"]-Xs1)**2 + (my_ray1["y"]-Ys1)**2 + (my_ray1["z"]-Zs1)**2 )
r2 = np.sqrt((my_ray2["x"]-Xs1)**2 + (my_ray2["y"]-Ys1)**2 + (my_ray2["z"]-Zs1)**2 )

ax.plot( r2, my_ray2[Field1], 'bx', ms=8, label='BufferSize=32')
ax.plot( r1, my_ray1[Field1], 'ro', ms=2, label='BufferSize=9999')

ax.legend(loc='lower left')

print("size=%d" % my_ray1[Field1].size)

#ax.set_yscale('log')

plt.show()
