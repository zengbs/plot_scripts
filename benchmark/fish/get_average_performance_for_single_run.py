import argparse
import sys
import numpy as np
import os.path

# load command-line parameters
parser = argparse.ArgumentParser( description='Calculate the average GAMER performance from the table Record__Performance' )

parser.add_argument( '-i', action='store', required=True, type=str,   dest='Filename_In',
                     help='input performance table'  )
parser.add_argument( '-o', action='store', required=True, type=str,   dest='Filename_Out',
                     help='output table'  )
parser.add_argument( '-n', action='store', required=True,  type=int,  dest='NGPU',
                     help='number of gpus' )

args=parser.parse_args()

print( '\nCommand-line arguments:' )
print( '-------------------------------------------------------------------' )
for t in range( len(sys.argv) ):
   print str(sys.argv[t]),
print( '' )
print( '-------------------------------------------------------------------\n' )

print 'Filename_In  = %s' % args.Filename_In
print 'Filename_Out = %s' % args.Filename_Out
print 'NGPU         = %d' % args.NGPU


# check
assert args.NGPU > 0, '-n (%d) < 1 !!' % (args.NGPU)
assert os.path.isfile( args.Filename_In ), 'file \"%s\" does not exist !!' % args.Filename_In


# load the input table
Table_In = np.loadtxt( args.Filename_In, usecols=(3,4,5), unpack=True )


# calculate various quantities
NRow       = Table_In[0].size
AveNCell   = sum( Table_In[0] ) / NRow
NUpdate    = sum( Table_In[1] )
TotalTime  = sum( Table_In[2] )
PerfAll    = NUpdate / TotalTime
PerfPerGPU = PerfAll / args.NGPU


# output
# header
if os.path.isfile( args.Filename_Out ) is False:
   File = open( args.Filename_Out, "w" )
   File.write( "# NGPU         : total number of GPUs\n" )
   File.write( "# NStep        : total number of evolution steps to get the average performance\n" )
   File.write( "# <NCell>      : average number of cells in NStep steps\n" )
   File.write( "# NUpdate      : total number of cell updates in NStep steps\n" )
   File.write( "# ElapsedTime  : total amount of simulation time in NStep steps [sec]\n" )
   File.write( "# Perf_Overall : overall performance using NGPU GPUs [# of cell updates / sec]\n" )
   File.write( "# Perf_per_GPU : performance per GPU [# of cell updates / sec]\n" )
   File.write( "#-------------------------------------------------------------------------------------------------------------\n" )
   File.write( "#%9s   %13s   %13s   %13s   %13s   %13s   %13s\n" %
               ("NGPU", "NStep", "<NCell>", "NUpdate", "ElapsedTime", "Perf_Overall", "Perf_per_GPU") )
   File.close()

# results
File = open( args.Filename_Out, "a" )
File.write( "%10d   %13d   %13.7e   %13.7e   %13.7e   %13.7e   %13.7e\n" %
            (args.NGPU, NRow, AveNCell, NUpdate, TotalTime, PerfAll, PerfPerGPU) )
File.close()
