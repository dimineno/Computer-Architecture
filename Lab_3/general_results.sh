#!/bin/bash

mcpat_results='mcpat/mcpat/mcpat_results'
gem5_outputs='Lab_2/spec_results'
energy_outputs='energy_results'

output='results.json'
echo [ > $output

for file in $(ls $mcpat_results/*.txt)
do
  name=$(echo $file | rev | cut -d'/' -f1 | rev | cut -d'.' -f1)
  energy=$(cat $energy_outputs/$name.txt | grep energy | cut -d' ' -f3)
  runtime=$(cat $energy_outputs/$name.txt | grep runtime | cut -d' ' -f9)
  area=$(cat $mcpat_results/$name.txt | grep Area | head -1 | cut -d' ' -f5)
  peak_power=$(cat $mcpat_results/$name.txt | grep "Peak Power" | head -1 | cut -d' ' -f6)

  echo { >> $output
  echo \"benchmark\": \"$name\", >> $output
  echo \"energy\": $energy, >> $output
  echo \"runtime\": $runtime, >> $output
  echo \"area\": $area, >> $output
  echo \"peak_power\": $peak_power >> $output
  echo }, >> $output
done

echo ] >> $output
