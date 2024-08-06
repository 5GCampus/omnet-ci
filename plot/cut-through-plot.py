from dpkt.pcap import Reader
from dpkt.ethernet import Ethernet
from decimal import Decimal
from pandas import DataFrame, cut, read_csv, concat
from math import sqrt
import matplotlib.pyplot as plt
import seaborn as sns
import os
from numpy import array, float64
CONFIGURATION = {"Omnet": {
                    "SF": "omnet_CT-NULL-NULL_nct_64-1460_0.0percent.pcap",
                    "CT": "omnet_CT-NULL-NULL_ct_64-1460_0.0percent.pcap"
                    }
                 }
                 
SOURCE_PATH_ROOT = "../workspace/network_validation/simulations/results/final"
OUTPUT_PATH_ROOT = "./"
def get_data(file, vendor, setting):
    os.system("tshark -F pcap -r "+file+" -w "+file+"_omnet") 
    file=file+"_omnet"
    f = open(file, "rb")
    pcap = Reader(f)

    framesizes = []
    latencies = []

    for ts, buf in pcap:
        hexstream = buf.hex()
        ts_send= Decimal(int(hexstream[96:112], 16))
        ts_recv = Decimal(int(hexstream[112:128], 16))

        latency = ts_recv * Decimal(0.001)  - ts_send * Decimal(0.001) 
        framesize = Ethernet(buf).ip.len + 18

        framesizes.append(framesize)
        latencies.append(float(latency))

    df = DataFrame(data=list(zip(framesizes, latencies)),
                   columns=["Framesize", "Latency us"])
    df.to_csv(OUTPUT_PATH_ROOT+"/{}{}measurements.csv".format(vendor, setting),
              index=False,
              header=True,
              sep="\t")

    return df
    df.describe()
    

    
dfs = []

for vendor, config in CONFIGURATION.items():
    for qos, pcap in config.items():
        dfs.append(get_data(SOURCE_PATH_ROOT+"/{}".format(pcap), vendor, qos))
        
#print(dfs)        
        
colors = ["#192D64",  #
          "#326491",  #
          "#649BBE",  #
          "#A0DCF0",  #
          "#0A9BA0",  #
          "#37B48C",  #
          "#A0C850",  #
          "#CDDC28",  #
          ]

# https://matplotlib.org/stable/api/markers_api.html
markers = ["o", "v"]

fig, ax = plt.subplots(figsize=(6, 4))

i = 0
for vendor, config in CONFIGURATION.items():
    for qos in config.keys():
        label = "{}: {}".format(vendor, qos)
        dfs[i].plot(x="Framesize", y="Latency us", kind="scatter", marker=markers[i], ax=ax, color=colors[i], label=label)
        dfs[i].describe().to_csv("Stream "+str(i)+"_description.csv")
        i += 1





plt.legend(bbox_to_anchor=(0.01, 0.985), loc='upper left', borderaxespad=0, markerscale=2)
ax.set_xlabel("Frame Size [B]")
ax.set_ylabel("Latency [us]")
plt.grid(dict(visible=True,
              which='major',
              color='#CCD6DF',
              linestyle='-'))
plt.grid(dict(visible=True,
              which='minor',
              color='#CCD6DF',
              linestyle='--'))

plt.xlim((0, 1600))
#plt.ylim((0, 16))

sns.despine(offset=10, trim=True)

plt.title("Forwarding Latency", loc='left', fontsize=18)
plt.title("1.Bit to 1.Bit", loc='right', fontsize=13, color='grey')

plt.tight_layout()

plt.savefig(OUTPUT_PATH_ROOT+"/plot-cts.png", dpi=300)

#plt.show()
