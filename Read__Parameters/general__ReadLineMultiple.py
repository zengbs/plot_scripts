import numpy as np
import os
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '/projectY/tseng/plot_scripts/Working__Space')
import argparse
from LineMultiple import _Plot


# Extract options from command line
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument( '-d',  action='store', required=True,  type=str, dest='Directory',
                     help='the directory adopting attribute parameters' )

args = parser.parse_args()
Directory = args.Directory


# Put the name of parameter files in `Directory` into `ParameterFile`
ParameterFile = [f for f in os.listdir(Directory) if os.path.isfile(os.path.join(Directory, f))]

# Get the total number of panels
NumPanel = len(ParameterFile)-1

# Get the number of columns in panel matrx
for j in range(100):
      FileName = Directory+"/"+"_".join(("panel", "00", "%02d"% j))
      if not os.path.isfile(FileName):
         NumCol = j
         break

# Get the number of rows in panel matrx
if ( NumPanel%NumCol == 0):
  NumRow = int(NumPanel/NumCol)
else:
  print( "NumPanel % NumCol = %d" % NumPanel%NumCol )
  exit()


# Check all parameter files exist
for i in range(NumCol):
    for j in range(NumRow):
      FileName = Directory+"/"+"_".join(("panel", "%02d"%i, "%02d"% j))
        if not os.path.isfile(FileName):
           print("%s does not exist!!" % FileName)
           exit()
   



Plot__Paramater = {}
Input__TestProb = {}

DirectoryPtr1 = open('Input__TestProb', "r")
DirectoryPtr2 = open(Directory, "r")


for line in DirectoryPtr1:
    line, _, comment = line.partition('#')
    if line.strip():  # non-blank line
        key, value = line.split()
        try:
            Input__TestProb[key] = float(value)
        except ValueError:
            Input__TestProb[key] = value

for line in DirectoryPtr2:
    line, _, comment = line.partition('#')
    if line.strip():  # non-blank line
        key, value = line.split()
        print(key, value)
        try:
            Plot__Paramater[key] = float(value)
        except ValueError:
            Plot__Paramater[key] = value

DirectoryPtr1.close()
DirectoryPtr2.close()

NormalizedConst_Dens = 0
NormalizedConst_Pres = 0




if (Plot__Paramater['NormalizedConst_Dens'] == 'auto'):
    if "Jet_SrcDens" in Input__TestProb:
      NormalizedConst_Dens = Input__TestProb['Jet_SrcDens']
    if "Blast_Dens_Src" in Input__TestProb:
      NormalizedConst_Dens = Input__TestProb['Blast_Dens_Src']

    Plot__Paramater['NormalizedConst_Dens'] = 'auto (%s)' % ( str(NormalizedConst_Dens) )

else:
    NormalizedConst_Dens = Plot__Paramater['NormalizedConst_Dens']

if (Plot__Paramater['NormalizedConst_Pres'] == 'auto'):
    if "Jet_SrcTemp" in Input__TestProb:
      NormalizedConst_Pres = Input__TestProb['Jet_SrcDens'] * Input__TestProb['Jet_SrcTemp']
    if "Blast_Temp_Src" in Input__TestProb:
      NormalizedConst_Pres = Input__TestProb['Blast_Dens_Src'] * Input__TestProb['Blast_Temp_Src']

    Plot__Paramater['NormalizedConst_Pres'] = 'auto (%s)' % ( str(NormalizedConst_Pres) )

else:
    NormalizedConst_Pres = Plot__Paramater['NormalizedConst_Pres']

if "cylindrical_radial_4velocity" in Plot__Paramater.values() or "cylindrical_radial_Mach_number" in Plot__Paramater.values():
    cylindrical_axis = Plot__Paramater['cylindrical_axis']

if __name__ == '__main__':
    _Plot(Plot__Paramater, Input__TestProb)
