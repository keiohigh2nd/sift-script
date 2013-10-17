#!/bin/bash
set -xu 

files="/home/keiohigh2nd/local_tool/sample_images/adj_images/DM/*"

i=0
for filepath in ${files}
do
  mv ${filepath} ../adj_images/DM/${i}.jpg
  i=`expr $i + 1`
done

echo done





