#/bin/bash
id=0
max=4
while read -r line
do
echo $line
#opp_runall ../src/validation_paper -j4 -c $line   -m -u Cmdenv -n .:../src:../../../inet4.4/examples:../../../inet4.4/showcases:../../../inet4.4/src:../../../inet4.4/tests/validation:../../../inet4.4/tests/networks:../../../inet4.4/tutorials -x inet.applications.voipstream;inet.common.selfdoc;inet.emulation;inet.examples.emulation;inet.examples.voipstream;inet.linklayer.configurator.gatescheduling.z3;inet.showcases.emulation;inet.showcases.visualizer.osg;inet.transportlayer.tcp_lwip;inet.visualizer.osg --image-path=../../../inet4.4/images -l ../../../inet4.4/src/INET omnetpp.ini
#opp_runall ../src/validation_paper -c $line -m -u Cmdenv -n .:../src:../../../inet4.4/examples:../../../inet4.4/showcases:../../../inet4.4/src:../../../inet4.4/tests/validation:../../../inet4.4/tests/networks:../../../inet4.4/tutorials -x inet.applications.voipstream;inet.common.selfdoc;inet.emulation;inet.examples.emulation;inet.examples.voipstream;inet.linklayer.configurator.gatescheduling.z3;inet.showcases.emulation;inet.showcases.visualizer.osg;inet.transportlayer.tcp_lwip;inet.visualizer.osg --image-path=../../../inet4.4/images -l ../../../inet4.4/src/INET omnetpp.ini &
./runsim.sh $line & 
i=$((i+1))
echo "$i"
if [ $i -gt $max ]; then
echo "waiting..."
	for job in `jobs -p`
	do
	echo $job
	    wait $job || let "FAIL+=1"
	done

	echo $FAIL
	id=0
fi
done < runs.txt
for job in `jobs -p`
  do
  echo $job
    wait $job || let "FAIL+=1"
  done
echo $FAIL
echo "done"
killall -9 validation_paper
