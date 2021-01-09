import numpy as np
import os
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '/projectY/tseng/plot_scripts/Working__Space')
import argparse
from LineMultiple  import LinePlot


# Extract the directory storing parameter files from command line
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument( '-d', action='store', required=True, type=str, dest='Directory', help='the directory adopting attribute parameters' )
args = parser.parse_args()
Directory = args.Directory


# Put the name of parameter files stored in `Directory` into `ParameterPanel`
ParameterPanel = [f for f in os.listdir(Directory) if os.path.isfile(os.path.join(Directory, f))]

# Get the total number of panels
NumPanel = len(ParameterPanel)-1

# Get the number of columns in panel array
for j in range(100):
      PanelName = Directory+"/"+"_".join(("panel", "00", "%02d"% j))
      if not os.path.isfile(PanelName):
         NumCol = j
         break

# Get the number of rows in panel array
if ( NumPanel%NumCol == 0):
  NumRow = int(NumPanel/NumCol)
else:
  print( "NumPanel % NumCol = %d" % (NumPanel%NumCol) )
  exit()

# Make sure the file name in `ParameterPanel` is in row-major
ParameterPanel[-1] = os.path.join(Directory,'panel_common')
for i in range(NumRow):
    for j in range(NumCol):
      PanelName = Directory+"/"+"_".join(("panel", "%02d"%i, "%02d"%j))
      ParameterPanel[i*NumCol+j] = PanelName

# Check all parameter files exist
for PathPanel in ParameterPanel:
    if not os.path.isfile(PathPanel):
       print("%s does not exist!!" % PanelName)
       exit()
      

# The list of pointers pointing to the parameter files
ParamaterPanelPtr = []

# The nested dictionary storing parameter in multi-file
Plot__Paramater = {}

# Extract parameters from `ParameterPanel`
for Panel in ParameterPanel:
    ParamaterPanelPtr.append(open(Panel, "r"))
    Plot__Paramater[Panel] = {}                     # create nested dictionary
    FIdx = ParameterPanel.index(Panel)               # find the index
    for line in ParamaterPanelPtr[FIdx]:
        line, _,comment = line.partition('#')
        if line.strip():                           # non-blank line
            key, value = line.split()
            try:
                Plot__Paramater[Panel][key] = float(value)
            except ValueError:
                Plot__Paramater[Panel][key] = value
    ParamaterPanelPtr[FIdx].close()


# Extract parameters from `Input__TestProb`
Input__TestProb = {}
Input__TestProbPtr = open('Input__TestProb', "r")
for line in Input__TestProbPtr:
    line, _, comment = line.partition('#')
    if line.strip():  # non-blank line
        key, value = line.split()
        try:
            Input__TestProb[key] = float(value)
        except ValueError:
            Input__TestProb[key] = value
Input__TestProbPtr.close()




NormalizedConst_Dens = 0
NormalizedConst_Pres = 0




if (Plot__Paramater[ParameterPanel[-1]]['NormalizedConst_Dens'] == 'auto'):
    if "Jet_SrcDens" in Input__TestProb:
      NormalizedConst_Dens = Input__TestProb['Jet_SrcDens']
    if "Blast_Dens_Src" in Input__TestProb:
      NormalizedConst_Dens = Input__TestProb['Blast_Dens_Src']

    Plot__Paramater[ParameterPanel[-1]]['NormalizedConst_Dens'] = 'auto (%s)' % ( str(NormalizedConst_Dens) )

else:
    NormalizedConst_Dens = Plot__Paramater[ParameterPanel[-1]]['NormalizedConst_Dens']

if (Plot__Paramater[ParameterPanel[-1]]['NormalizedConst_Pres'] == 'auto'):
    if "Jet_SrcTemp" in Input__TestProb:
      NormalizedConst_Pres = Input__TestProb['Jet_SrcDens'] * Input__TestProb['Jet_SrcTemp']
    if "Blast_Temp_Src" in Input__TestProb:
      NormalizedConst_Pres = Input__TestProb['Blast_Dens_Src'] * Input__TestProb['Blast_Temp_Src']

    Plot__Paramater[ParameterPanel[-1]]['NormalizedConst_Pres'] = 'auto (%s)' % ( str(NormalizedConst_Pres) )

else:
    NormalizedConst_Pres = Plot__Paramater[ParameterPanel[-1]]['NormalizedConst_Pres']

for Panel in ParameterPanel:
    if "cylindrical_radial_4velocity" in Plot__Paramater[Panel].values() or "cylindrical_radial_Mach_number" in Plot__Paramater[Panel].values():
        cylindrical_axis = Plot__Paramater[Panel]['cylindrical_axis']


# Check `NormalizedConst_Pres` and `NormalizedConst_Dens` are positive
See  = NormalizedConst_Pres > 0
See |= NormalizedConst_Dens > 0
if ( not See ):
   print( "NormalizedConst_Dens=%e, NormalizedConst_Pres=%e" % ( NormalizedConst_Dens, NormalizedConst_Pres ) )
   exit(0)


if __name__ == '__main__':
   if Plot__Paramater[ParameterPanel[-1]]["PlotType"] == "line":
      LinePlot(Plot__Paramater, Input__TestProb, NumRow, NumCol)
   if Plot__Paramater[ParameterPanel[-1]]["PlotType"] == "slice":
      from SliceMultiple import SlicePlot
      SlicePlot(Plot__Paramater, Input__TestProb, NumRow, NumCol)

