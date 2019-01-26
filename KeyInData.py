import yt

ds=yt.load("RESTART")

#for key in ds:
#  print key, ds[key]
print ds["Step"]
print ds["DumpID"]
