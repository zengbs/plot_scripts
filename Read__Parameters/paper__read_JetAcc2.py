import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '/projectY/tseng/gamer/bin/plot_scripts/Working__Space')

import argparse
from paper__plot_JetAcc2 import _Plot


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


if (Plot__Paramater['Field'] == "cylindrical_radial_4velocity"):
    cylindrical_axis = Plot__Paramater['cylindrical_axis']

if __name__ == '__main__':
    _Plot(Plot__Paramater, Input__TestProb)
