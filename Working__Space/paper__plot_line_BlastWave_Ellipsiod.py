import yt
import matplotlib.pyplot as plt 
import numpy as np
from matplotlib.ticker import MultipleLocator
import matplotlib.font_manager as font_manager

import derived_field as df
import unit

#FileName = 'fig__benchmark_pizdaint'
DataName = 'Data_000009'
font = {'family': 'monospace','color': 'black', 'weight': 'heavy', 'size': 20}

# Start point
Xs1 = 0.0
Ys1 = 1.0
Zs1 = 0.5

Xe1 = 1.0
Ye1 = 0.0
Ze1 = 0.5

#End point
Xs2 = 0.0
Ys2 = 0.0
Zs2 = 0.5

Xe2 = 1.0
Ye2 = 1.0
Ze2 = 0.5


StarCoord1 = [Xs1, Ys1, Zs1]
EndCoord1  = [Xe1, Ye1, Ze1] 
NumPts1    = 2048
Field1 = 'Lorentz_factor'

StarCoord2 = [Xs2, Ys2, Zs2]
EndCoord2  = [Xe2, Ye2, Ze2] 
NumPts2    = 2048
Field2 = 'Lorentz_factor'

f, ax = plt.subplots( 1, 1, sharex=False, sharey=False )

df.ds = yt.load(DataName)
function, units = unit.ChooseUnit(Field1)
df.ds.add_field(("gamer", Field1), function=function, sampling_type="cell", units=units)

my_ray1 = yt.LineBuffer(df.ds,StarCoord1, EndCoord1, NumPts1)
my_ray2 = yt.LineBuffer(df.ds,StarCoord2, EndCoord2, NumPts2)


Xs1 *= df.ds.length_unit 
Ys1 *= df.ds.length_unit 
Zs1 *= df.ds.length_unit 

Xe1 *= df.ds.length_unit 
Ye1 *= df.ds.length_unit 
Ze1 *= df.ds.length_unit 

Xs2 *= df.ds.length_unit 
Ys2 *= df.ds.length_unit 
Zs2 *= df.ds.length_unit 

Xe2 *= df.ds.length_unit 
Ye2 *= df.ds.length_unit 
Ze2 *= df.ds.length_unit 


r1 = np.sqrt((my_ray1["x"]-Xs1)**2 + (my_ray1["y"]-Ys1)**2 + (my_ray1["z"]-Zs1)**2 )
r2 = np.sqrt((my_ray2["x"]-Xs2)**2 + (my_ray2["y"]-Ys2)**2 + (my_ray2["z"]-Zs2)**2 )

ax.plot( r1, my_ray1[Field1], 'ro', ms=2)
ax.plot( r2, my_ray2[Field2], 'bo', ms=2)

#ax.set_yscale('log')

plt.show()
