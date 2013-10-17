#!/bin/bash
set -xu


rm ../good_desc.txt
rm ../mal_desc.txt
rm ../query_desc.txt
rm text.txt

python=/home/appl/bin/python2.7
files="/home/keiohigh2nd/local_tool/sample_images/adj_images/AMD/*"
tmp="100.txt"

good_files="/home/keiohigh2nd/local_tool/sample_images/adj_images/AMD"
good="/home/keiohigh2nd/local_tool/sample_images/good/"
mal="/home/keiohigh2nd/local_tool/sample_images/mal/"

pre="/home/keiohigh2nd/local_tool/sample_images/adj_images/AMD/112.jpg"

for i in `seq 100`; do

  for i in `seq 8`; do
    num_image_id=$((RANDOM % 111))
    mv $good_files/$num_image_id'.jpg' $good
  done

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

  mv $good* $good_files/

  cat ../classify_result_.txt | grep Malignant | wc >> $tmp
  rm ../classify_result_.txt

done

echo done
