import yt

ds=yt.load("RESTART")

#for key in ds:
#  print (key, ds[key])
print ('Step:', ds["Step"])
print ('DumpID:', ds["DumpID"])
print ('EoS:', ds["EoS"])
