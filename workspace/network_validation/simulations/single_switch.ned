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

package validation_paper.simulations;

import inet.node.ethernet.Eth100M;
import inet.node.ethernet.Eth1G;
import inet.examples.bgpv4.BgpUpdate.BGPRouterEx;
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
import inet.physicallayer.wired.ethernet.TSNtimestamper;


network single_switch extends TsnNetworkBase
{
    parameters:
        *.eth[*].bitrate = default(1000Mbps);
    submodules:
        tsnClock: TsnClock {
            @display("p=350,100");
        }
        priority: TsnDevice {
            @display("p=250,200");
        }
        switch1: TsnSwitch {
            @display("p=350,200");
        }
        server: TsnDevice {
            @display("p=550,200");
            @signal[packetReceived](type=inet::Packet);
            @statistic[packetReceived](title="packets received"; source=packetReceived; record=dataAge(packetReceived));

        }
 //       timestamp1 : TSNtimestamper{
 //        @display("p=550,300");   
            
 //       }
    connections:
        tsnClock.ethg++ <--> EthernetLink <--> switch1.ethg++;
        priority.ethg++ <--> EthernetLink <--> switch1.ethg++;
        switch1.ethg++ <--> EthernetLink <--> server.ethg++;
 //       switch1.ethg++ <--> EthernetLink <--> timestamp1.interface1;
   //     timestamp1.interface2  <--> EthernetLink <-->  server.ethg++;

}
