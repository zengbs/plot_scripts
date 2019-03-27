import numpy as np
import matplotlib.pyplot as plt 
from matplotlib.pyplot import figure
import matplotlib.ticker as mtick

figure(figsize=(20, 10), dpi=80, facecolor='w', edgecolor='k')

data1 = []
#data2 = []

data1 = np.loadtxt('Perf_Avg')
#data1 = np.loadtxt('Table__WeakScaling_AMR-o_srhydro')
#data2 = np.loadtxt('Table__WeakScaling_AMR-o_hydro')

Node                 = data1[:,  0]
Perf_Overall_srhydro = data1[:,  2]

#Perf_Overall_hydro   = data2[:,  5]

Ideal_SR    = (Node/Node[0])*Perf_Overall_srhydro[0]
#Ideal_Hydro = (Node/Node[0])*Perf_Overall_hydro[0]

plt.plot(Node, Perf_Overall_srhydro, 'bo', label='SRHydro', linestyle='solid')
plt.plot(Node, Ideal_SR     , label='Ideal scaling(SRHydro)', color='blue',linestyle='--')
#plt.plot(Node, Perf_Overall_hydro  , 'ro', label='Hydro', linestyle='solid')
#plt.plot(Node, Ideal_Hydro  , label='Ideal scaling(Hydro)', color='red',linestyle='--')

plt.tick_params(axis='both', labelsize='15')
plt.gca().yaxis.set_major_formatter(mtick.FormatStrFormatter('%.0e'))
#plt.legend(fontsize='20', loc='lower left',bbox_to_anchor=(1,1))
plt.legend(fontsize='20', loc='upper left')
plt.yscale('log')
plt.xscale('log')
plt.xlabel('Number of Nodes', size='25')
plt.ylabel('Cells/sec', size='25')
plt.show()
#plt.savefig('weak_scaling.png')
