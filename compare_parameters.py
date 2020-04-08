import sys
import argparse


#parser = argparse.ArgumentParser(description='Process some integers.')
#parser.add_argument( '-p',  action='store', required=True,  type=str, dest='File', help='file' )
#
#args = parser.parse_args()
#File = args.File

Input__TestProb = {}



FilePtr1 = open('d03/Input__TestProb', "r")


for line in FilePtr1:
    line, _, comment = line.partition('#')
    if line.strip():  # non-blank line
        key, value = line.split()
        Input__TestProb[key] = value

FilePtr1.close()


diffkeys = [k for k in dict1 if dict1[k] != dict2[k]]
for k in diffkeys:
  print k, ':', dict1[k], '->', dict2[k]
