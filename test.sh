#!/bin/sh

files="/home/keiohigh2nd/fundus/fundus-image-20130524/DM/*"

for filepath in ${files}
do
  filename=`basename ${filepath}`
  echo ${filename}
  echo ${filepath}
done

read wait
