#!/bin/bash

echo $1 #pagesdir
echo $2 #outname
echo "$2.tif"

echo "$1*.tif" "$1$2.tif"

cd $1
tiffcp *.tif "$2.tif"
tesseract "$2.tif" "$2.pdf" -l eng pdf
