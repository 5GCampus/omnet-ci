# omnet-ci

## Paper 
- please see the paper for details: [Improving TSN Simulation Accuracy in OMNeT++: A Hardware-Aligned Approach](https://ieeexplore.ieee.org/abstract/document/10549887)
```
  @ARTICLE{10549887,
  author={Liu, How-Hang and Senk, Stefan and Ulbricht, Marian and Nazari, Hosein K. and Scheinert, Tobias and Reisslein, Martin and Nguyen, Giang T. and Fitzek, Frank H. P.},
  journal={IEEE Access}, 
  title={Improving TSN Simulation Accuracy in OMNeT++: A Hardware-Aligned Approach}, 
  year={2024},
  volume={12},
  number={},
  pages={79937-79956},
  keywords={Hardware;Protocols;Clocks;Switches;Delays;Time factors;Synchronization;Open source software;Sensitivity analysis;Frame preemption (FP);hardware testbed;measurement;OMNeT++;open-source software;simulation;time-aware shaper (TAS);time-sensitive networking (TSN);time synchronization},
  doi={10.1109/ACCESS.2024.3410109}}
```

## version
- We used version 6.0 of OMNeT++ and version 4.5.2 of INET. 

## Modified in INET
- For CT test
  - src/inet/queueing/common/PacketDelayer.cc
- For gPTP test
  - src/inet/linklayer/ieee8021as/Gptp.cc
## TO configure modified INET in the .ini file
- SF mode: ```*.switch1*.eth[4].processingDelayLayer.egress.delay = [SET THE DELAY VALUES]```
- CT mode:
  - ```*.switch2*.eth[1].processingDelayLayer.egress.interbuff_alpha = [ALPHA VALUE]```
  - ```*.switch2*.eth[1].processingDelayLayer.egress.interbuff_beta = [BETA VALUE]```
  - ```*.switch2*.eth[1].processingDelayLayer.egress.threshold_pktsize = [PKT THRESHOLD]```

## HW measurement
- Please see our [TSN-FlexTest](https://github.com/5GCampus/tsn-testbed)
