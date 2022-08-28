#!/bin/bash

mcpat_results='mcpat/mcpat/mcpat_results'
gem5_outputs='Lab_2/spec_results'
print_energy='mcpat/Scripts/print_energy.py'


for file in $(ls $mcpat_results/*.txt)
do
  name=$(echo $file | rev | cut -d'/' -f1 | rev | cut -d'.' -f1)
  echo "$name"
  python2 $print_energy $mcpat_results/$name.txt $gem5_outputs/$name/stats.txt > energy_results/"$name.txt"
done




