import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

figure(figsize=(20, 10), dpi=80, facecolor='w', edgecolor='k')

X1, Y1 = [], []
X2, Y2 = [], []
A = []

for i in range(10, 81):
    print i
    A = np.loadtxt("../data/4/Xline_y0.000_z0.000_0000" + str(i))
    B = np.loadtxt("../data/9/Xline_y0.000_z0.000_0000" + str(i))
    C = (A[:, 11] - B[:, 11])
    C = C / A[:, 11]
    A_X = A[:, 3]
    plt.plot(A_X, C)
    plt.xlabel('$X$')
    fig = plt.gcf()
    plt.close()
    fig.savefig("A" + str(i)) 
