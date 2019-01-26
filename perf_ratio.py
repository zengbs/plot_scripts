import numpy as np
import matplotlib.pyplot as plt 
#from matplotlib.pyplot import figure
import matplotlib.ticker as mtick

#figure(figsize=(20, 10), dpi=80, facecolor='w', edgecolor='k')


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

ratio_1 = perf_amd_32 / perf_hulk_12
ratio_2 = perf_amd_16 / perf_hulk_06

plt.xlim([0, 80])

plt.hlines(6.0, 0, 80, 'red' , linestyles='dashed')
plt.hlines(5.0, 0, 80, 'blue' , linestyles='dashed')


plt.plot(step, ratio_1, 'ro', label=r'$\frac{AMD (32 threads)}{HULK (12 threads)}$')
plt.plot(step, ratio_2, 'bx', label=r'$\frac{AMD (16 threads)}{HULK (06 threads)}$')

plt.tick_params(axis='both', labelsize='15')
#plt.gca().yaxis.set_major_formatter(mtick.FormatStrFormatter('%.0e'))
plt.legend(fontsize='20', loc='center right')
#plt.yscale('log')
plt.xlabel('Steps', size='25')
plt.ylabel('Performance Ratio', size='25')
plt.show()
#plt.savefig('Compare_Perf_Ratio.png')
