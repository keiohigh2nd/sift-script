#!/bin/bash
set -xu

files="/home/keiohigh2nd/local_tool/sample_images/101_ObjectCategories/*"
pre="/home/keiohigh2nd/local_tool/sample_images/good_1005/orig00021.jpg"
i=0

for filepath in ${files}
do
  python2.7 get_descriptor.py ${pre} ${filepath}/
  i=`expr $i + 1`
done

echo done
