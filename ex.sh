#!/bin/bash
set -xu

if [ $# -ne 1 ]; then
   echo "No argument" 1>&2
   exit 1
fi



rm ../good_desc.txt
rm ../mal_desc.txt
rm ../query_desc.txt
rm text.txt
python=/home/appl/bin/python2.7

python2.7 sift_sh_NBNN.py $1
g++ -O2 tab.cpp
./a.out
sleep 2
python2.7 draw.py $1


echo done


