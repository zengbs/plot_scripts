import yt
from yt.units import G, kboltz, c, mp, qp

#ds=yt.load("RESTART")
ds=yt.load("Data_000002")

for key in ds:
 print (key, ds[key])
#print ('Step:', ds["Step"])
#print ('sha1:', ds["GitSha1"])
#print ('branch:', ds["GitBranch"])
#print ('Model:', ds["Model"])
#print ('DumpID:', ds["DumpID"])
#print ('Unit_L:', ds["Unit_L"])
#print ('EoS:', ds["Unit_L"]*ds.length_unit)
#print ( c )
