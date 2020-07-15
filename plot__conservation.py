import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

figure(figsize=(20, 10), dpi=80, facecolor='w', edgecolor='k')

X1, Y1 = [], []
X2, Y2 = [], []
data = []

data = np.loadtxt('Record__Conservation')

step          = data[:,  1]
Mass_Gas_RErr = data[:,  4]
Etot_Gas_RErr = data[:, 22]

plt.plot(step, Mass_Gas_RErr, 'bo', label='Mass_Gas_RErr')
plt.plot(step, Etot_Gas_RErr, 'ro', label='Etot_Gas_RErr')

plt.legend(fontsize='20', loc='upper left')
plt.yscale('log')
plt.xlabel('Step', size='20')
plt.ylabel('Relative_Error', size='20')
plt.savefig('Record__Conservation.png')
