import yt
import matplotlib.pyplot as plt 
import numpy as np
from matplotlib.ticker import MultipleLocator
import matplotlib.font_manager as font_manager

import derived_field as df
import unit

FileName  = 'Profile'
DataName1 = 'HorizontalFlow01HigRes_DT_0.12/Data_000000'

font = {'family': 'monospace','color': 'black', 'weight': 'heavy', 'size': 20}

# Start point
Xs1 = 12.5
Ys1 = 11.7
Zs1 = 12.5

#End point
Xe1 = 12.5
Ye1 = 13.3
Ze1 = 12.5


StartCoord1 = [Xs1, Ys1, Zs1]
EndCoord1  = [Xe1, Ye1, Ze1] 
NumPts1    = 2048
Field1 = '3_velocity_x'


f, ax = plt.subplots( 1, 1, sharex=False, sharey=False )

df.ds1 = yt.load(DataName1)

function, units = unit.ChooseUnit(Field1)

df.ds1.add_field(("gamer", Field1), function=function, sampling_type="cell", units=units)

my_ray1 = yt.LineBuffer(df.ds1,StartCoord1, EndCoord1, NumPts1)


StartCoord1[0] *= df.ds1.length_unit 
StartCoord1[1] *= df.ds1.length_unit 
StartCoord1[2] *= df.ds1.length_unit 

             
Xe1 *= df.ds1.length_unit 
Ye1 *= df.ds1.length_unit 
Ze1 *= df.ds1.length_unit 



r1 = np.sqrt((my_ray1["x"]-StartCoord1[0])**2 + (my_ray1["y"]-StartCoord1[1])**2 + (my_ray1["z"]-StartCoord1[2])**2 )

ax.plot( r1, my_ray1[Field1], 'ro', ms=2)

ax.legend(loc='upper right', fontsize=8)
#ax.set_ylim(0,10000)

plt.show()
