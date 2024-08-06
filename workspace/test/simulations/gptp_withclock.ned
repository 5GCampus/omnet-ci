//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Lesser General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
// 
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Lesser General Public License for more details.
// 
// You should have received a copy of the GNU Lesser General Public License
// along with this program.  If not, see http://www.gnu.org/licenses/.
// 

package test.simulations;

import inet.networks.base.TsnNetworkBase;
import inet.node.contract.IEthernetNetworkNode;
import inet.node.ethernet.EthernetLink;
import inet.common.scenario.ScenarioManager;
import inet.networks.base.TsnNetworkBase;
import inet.node.ethernet.EthernetLink;
import inet.node.ethernet.EthernetSwitch;
import inet.node.tsn.TsnClock;
import inet.node.tsn.TsnDevice;
import inet.node.tsn.TsnSwitch;
import inet.node.inet.StandardHost;
import inet.applications.clock.SimpleClockSynchronizer;


network gptp_withclock extends TsnNetworkBase
{
    parameters:
        *.eth[*].bitrate = default(1000Mbps);
    submodules:
        switch: TsnSwitch {
            @display("p=550,200");
        }
        server: TsnDevice {
            @display("p=750,200");
        }
        tactile: TsnDevice {
            @display("p=350,194");
        }
        tsnClock: TsnClock {
            @display("p=558,94");
        }
        //synchronizer: SimpleClockSynchronizer {
        // 	@display("p=558,94");
        // 	synchronizationClockTimeError = default(0s);
        //}
        //besteff: TsnDevice {
        //    @display("p=358,300");
        //}
    connections:
        tactile.ethg++ <--> EthernetLink <--> switch.ethg++;
        //besteff.ethg++ <--> EthernetLink <--> switch.ethg++;
        switch.ethg++ <--> EthernetLink <--> server.ethg++;
        tsnClock.ethg++ <--> EthernetLink <--> switch.ethg++;
}
