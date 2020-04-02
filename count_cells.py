import yt

ds=yt.load("Data_000000")
ad = ds.print_stats()
#ad = ds.all_data()
#print("Total number of cells = %i" %  ad.sum("ones"))
