#!/bin/bash

cp -r ./søren ./$1
mv ./$1/gold_border_søren.png ./$1/gold_border_$1.png
mv ./$1/silver_border_søren.png ./$1/silver_border_$1.png
mv ./$1/søren.png ./$1/$1.png
