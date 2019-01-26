import numpy as np

a=np.zeros(3)
a[0]=-1
a[1]=-20
a[2]=3

print np.where((a>-5)&(a<1),0,a)
