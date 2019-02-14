import yt

ds=yt.load("Data_000031")

#for key in ds:
#  print key, ds[key]
print ds["Step"]
print ds["DumpID"]
print ds["EoS"]
