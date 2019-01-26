import numpy as np
import matplotlib.pyplot as plt 
from matplotlib.pyplot import figure
import matplotlib.ticker as mtick

figure(figsize=(20, 10), dpi=80, facecolor='w', edgecolor='k')

X1, Y1 = [], []
X2, Y2 = [], []
data = []

data1 = np.loadtxt('Record__Performance_amd_16')
data2 = np.loadtxt('Record__Performance_amd_32')
data3 = np.loadtxt('Record__Performance_hulk_06')
data4 = np.loadtxt('Record__Performance_hulk_12')

step         = data1[:,  1]  
perf_amd_16  = data1[:,  6]
perf_amd_32  = data2[:,  6]
perf_hulk_06 = data3[:,  6]
perf_hulk_12 = data4[:,  6]

plt.plot(step, perf_amd_16, 'bo', label=' AMD 16 threads')
plt.plot(step, perf_amd_32, 'ro', label=' AMD 32 threads')
plt.plot(step, perf_hulk_06, 'bx', label='HULK 06 threads')
plt.plot(step, perf_hulk_12, 'rx', label='HULK 12 threads')

plt.tick_params(axis='both', labelsize='15')
plt.gca().yaxis.set_major_formatter(mtick.FormatStrFormatter('%.0e'))
plt.legend(fontsize='20', loc='center right',bbox_to_anchor=(1,1))
#plt.yscale('log')
plt.xlabel('Steps', size='25')
plt.ylabel('# of updated cells / sec', size='25')
plt.show()
#plt.savefig('Compare_Perf.png')
