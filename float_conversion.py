import h5py
import numpy as np


f = h5py.File("Data_000000","r")

for key in f.keys():
    print(key) #Names of the groups in HDF5 file.

#Get the HDF5 group
group = f['Info']

#Checkout what keys are inside that group.
for key in group.keys():
    print(key)

print( f['Info']['InputPara']['BoxSize'])
print( 'NPatch: ', sum(f['Info']['KeyInfo']['NPatch']))
print( f["Info"]["InputPara"]["Flu_GPU_NPGroup"])


data = f['GridData']['Dens'][()]

data_single = data.astype('float32')


print(data.shape)
print(data.ndim)
print(data.dtype)
print(data_single.dtype)
#print(data[0][0])

#After you are done
f.close()
