import sys
import argparse


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


if (Plot__Paramater['NormalizedConst_Dens'] == 'auto'):
    if "Jet_SrcDens" in Input__TestProb:
      NormalizedConst_Dens = Input__TestProb['Jet_SrcDens']
    if "Blast_Dens_Src" in Input__TestProb:
      NormalizedConst_Dens = Input__TestProb['Blast_Dens_Src']

    Plot__Paramater['NormalizedConst_Dens'] = 'auto (%s)' % ( str(NormalizedConst_Dens) )

else:
    NormalizedConst_Dens = Plot__Paramater['NormalizedConst_Dens']
