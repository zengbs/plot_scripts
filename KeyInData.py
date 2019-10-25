import yt
from yt.units import G, kboltz, c, mp, qp

#ds=yt.load("RESTART")
ds=yt.load("Data_000000")

#for key in ds:
# print (key, ds[key])
print ('Step:', ds["Step"])
print ('Model:', ds["Model"])
print ('DumpID:', ds["DumpID"])
print ('EoS:', ds["Unit_L"]*ds.length_unit)
print ( c )
