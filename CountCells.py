import yt

ds=yt.load("Data_000000")
ad = ds.print_stats() # include leaf patches
#ad = ds.all_data()   # exclude leaf patches
#print("Total number of cells = %i" %  ad.sum("ones"))
