#!/bin/bash
source omnetpp/setenv
source inet4.4/setenv

cd workspace/network_validation
mv Makefile_sim Makefile
make makefiles
make
cd simulations
./run.sh
ls -allh results
ls -allh results/final
