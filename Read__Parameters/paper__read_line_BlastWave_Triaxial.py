import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '/projectY/tseng/gamer/bin/plot_scripts/Working__Space')

import argparse
from paper__plot_line_BlastWave_Triaxial import _Plot


parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument( '-p',  action='store', required=True,  type=str, dest='File', help='file' )

args = parser.parse_args()
File = args.File

Plot__Paramater = {}
Input__TestProb = {}



FilePtr1 = open('Input__TestProb', "r")
FilePtr2 = open(File, "r")


for line in FilePtr1:
    line, _, comment = line.partition('#')
    if line.strip():  # non-blank line
        key, value = line.split()
        try:
            Input__TestProb[key] = float(value)
        except ValueError:
            Input__TestProb[key] = value

for line in FilePtr2:
    line, _, comment = line.partition('#')
    if line.strip():  # non-blank line
        key, value = line.split()
        try:
            Plot__Paramater[key] = float(value)
        except ValueError:
            Plot__Paramater[key] = value

FilePtr1.close()
FilePtr2.close()

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

if "cylindrical_radial_4velocity" in Plot__Paramater.values():
    cylindrical_axis = Plot__Paramater['cylindrical_axis']

if __name__ == '__main__':
    _Plot(Plot__Paramater, Input__TestProb)
