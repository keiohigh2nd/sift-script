#!/bin/bash
set -xu


rm ../good_desc.txt
rm ../mal_desc.txt
rm ../query_desc.txt
rm ../classify_result_.txt
rm text.txt

python=/home/appl/bin/python2.7
files="/home/keiohigh2nd/local_tool/sample_images/adj_images/sample/*"
pre="/home/keiohigh2nd/local_tool/sample_images/adj_images/sample/11.jpg"

good="/home/keiohigh2nd/local_tool/sample_images/good_1005/"
mal="/home/keiohigh2nd/local_tool/sample_images/mal_1005/"
python2.7 sift_sh_NBNN.py ${pre} ${mal} ${good}

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
