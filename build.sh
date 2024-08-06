#!/bin/bash
wget https://github.com/omnetpp/omnetpp/releases/download/omnetpp-6.0.1/omnetpp-6.0.1-linux-x86_64.tgz
tar xf omnetpp-6.0.1-linux-x86_64.tgz
rm omnetpp-6.0.1-linux-x86_64.tgz
mv omnetpp-6.0.1 omnetpp
cp configure.omnet omnetpp/configure.user
cd omnetpp
source setenv
./configure
make -j`nproc`

cd ..
cd inet4.4
source setenv
make makefiles
make -j`nproc`
