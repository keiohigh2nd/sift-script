#!/bin/bash
set -xu


rm ../good_desc.txt
rm ../mal_desc.txt
rm ../query_desc.txt
rm text.txt

python=/home/appl/bin/python2.7
files="/home/keiohigh2nd/local_tool/sample_images/dermatoscopy/ncn_test/*"
pre="/home/keiohigh2nd/local_tool/sample_images/dermatoscopy/ncn_test/1.jpg"

python2.7 sift_sh_NBNN.py ${pre} $1 $2

for filepath in ${files}
do
  python2.7 sift_sh_NBNN_file.py ${filepath}
  g++ -O2 tab.cpp
  ./a.out
  python2.7 draw_file.py ${filepath}
  rm text.txt
  rm ../query_desc.txt
done

echo done
