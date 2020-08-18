import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

figure(figsize=(10, 5), dpi=80, facecolor='w', edgecolor='k')

X1, Y1 = [], []
X2, Y2 = [], []
data = []

data = np.loadtxt(os.getcwd()+'/Record__Conservation')

step          = data[:,  1]
Mass_Gas      = data[:,  2]
Mass_Gas_RErr = data[:,  4]

MomX_Gas_RErr = data[:,  7]
MomY_Gas_RErr = data[:, 10]
MomZ_Gas_RErr = data[:, 13]

Etot_Gas      = data[:, 14]
Etot_Gas_RErr = data[:, 16]

plt.plot(step, Mass_Gas_RErr, 'bo', label='Mass_Gas_RErr')
plt.plot(step, Etot_Gas_RErr, 'ro', label='Etot_Gas_RErr')
plt.plot(step, MomX_Gas_RErr, 'gx', label='MomX_Gas_RErr')
plt.plot(step, MomX_Gas_RErr, 'ks', label='MomY_Gas_RErr')
plt.plot(step, MomX_Gas_RErr, 'y+', label='MomZ_Gas_RErr')

plt.legend(fontsize='20', loc='upper left')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Step', size='20')
plt.ylabel('Relative_Error', size='20')
plt.show()
