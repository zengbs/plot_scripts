import sys
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument( '-f1',  action='store', required=True,  type=str, dest='File1' ,help='File1' )
parser.add_argument( '-f2',  action='store', required=True,  type=str, dest='File2' ,help='File2' )

args = parser.parse_args()
File1 = args.File1
File2 = args.File2


Input__TestProb1 = {}
Input__TestProb2 = {}

FilePtr1 = open(File1, "r")
FilePtr2 = open(File2, "r")


for line in FilePtr1:
    line, _, comment = line.partition('#')
    if line.strip():  # non-blank line
        key, value = line.split()
        Input__TestProb1[key] = value


for line in FilePtr2:
    line, _, comment = line.partition('#')
    if line.strip():  # non-blank line
        key, value = line.split()
        Input__TestProb2[key] = value

FilePtr1.close()
FilePtr2.close()

diffkeys = [k for k in Input__TestProb1 if Input__TestProb1[k] != Input__TestProb2[k]]

for k in diffkeys:
  print ( '%-30s%-1s%10s%10s%10s' %  ( k, ':', Input__TestProb1[k], '-->', Input__TestProb2[k] ) )
