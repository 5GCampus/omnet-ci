#!/bin/bash
source omnetpp/setenv
source inet4.4/setenv
cd plot
rm checklog.txt || true
./gitinfo.sh
python3 validation_ccdf-omnet2.py 
python3 gptp_CI.py  
python3 cut-through-plot.py  
python3 validation_combineFeature.py  
wait
cat checklog.txt

