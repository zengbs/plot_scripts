import yt
from yt.units import G, kboltz, c, mp, qp

#ds=yt.load("RESTART")
ds=yt.load("Data_000004")

#for key in ds:
# print (key, ds[key])
#print (ds["BoxSize"])
#print ('Step:', ds["Step"])
#print ('Step:', ds["Step"])
#print ('sha1:', ds["GitSha1"])
#print ('branch:', ds["GitBranch"])
#print ('Model:', ds["Model"])
#print ('DumpID:', ds["DumpID"])
#print ('Unit_L:', ds["Unit_L"])
print ('Time:', ds["Time"].shape)
#print ( c )
#print ( ds["Time"][0] )
