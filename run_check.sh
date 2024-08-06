#!/bin/bash
if [ "$(cat plot/checklog.txt | wc -l)" -ne "30" ]; then
   echo "ERROR some Simulations are missing, expected 22" 
   exit 1
fi
while IFS= read -r line
do
  echo "$line" | grep FAIL && exit 1
done < "plot/checklog.txt"
