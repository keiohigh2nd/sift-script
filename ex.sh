#!/bin/bash
set -xu

rm ../good_desc.txt
rm ../mal_desc.txt
rm ../query_desc.txt
rm text.txt
python=/home/appl/bin/python2.7

python2.7 sift_sh_NBNN.py
g++ -O2 tab.cpp
./a.out
sleep 2
python2.7 draw.py


echo done


