#!/bin/bash
set -xu

python=/home/appl/bin/python2.7
python2.7 sift_fn_NBNN.py

g++ -O2 tab.cpp
./a.out

echo done
