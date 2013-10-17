#!/bin/bash
set -xu

files="/home/keiohigh2nd/local_tool/sample_images/mal_1005/*"
i=0

for filepath in ${files}
do
  convert -crop 410x763+299+86 ${filepath} ${i}.jpg
  i=`expr $i + 1`
done

echo done
