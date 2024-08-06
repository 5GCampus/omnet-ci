#!/usr/bin/env python
# coding: utf-8

# # Validation Paper: CCDF Measurements/Plots

# In[125]:


from utils.parsePcap import TsnParsePcap
from utils.createPlot import TsnCreatePlot
from pandas import read_csv, concat, cut
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


# In[126]:


# In[138]:


CONFIGURATION = {
                 "Omnet": {
#                     "Baseline no CTS": "omnet_robotic-NULL-NULL_P1_1518_0.0percent.pcap"
                    "CTS 128B"   : "omnet_robotic-NULL-NULL_no-FP-TAS-CTS_128_200.0percent.pcap",
                    "CTS 1518B"  : "omnet_robotic-NULL-NULL_no-FP-TAS-CTS_1518_200.0percent.pcap",
                    "noCTS 128B" : "omnet_robotic-NULL-NULL_no-FP-TAS-no-CTS_128_200.0percent.pcap",
                    "noCTS 1518B": "omnet_robotic-NULL-NULL_no-FP-TAS-no-CTS_1518_200.0percent.pcap",
#                    "A": "omnet_robotic-NULL-NULL_final-A_1518_200.0percent.pcap",
#                     "B": "omnet_robotic-NULL-NULL_final-B_1518_200.0percent.pcap",
#                     "C": "omnet_robotic-NULL-NULL_final-C_1518_200.0percent.pcap",
#                     "D": "omnet_robotic-NULL-NULL_final-D_1518_200.0percent.pcap",
#                     "E": "omnet_robotic-NULL-NULL_final-E_1518_200.0percent.pcap",
#                     "F": "omnet_robotic-NULL-NULL_final-F_1518_200.0percent.pcap"
                     
#                     "A":"Config_A_SF_1518B.pcap",
#                     "B":"Conifg_B_CT_1518B.pcap",
#                     "D":"Conifg_D_FP_SF.pcap"
#                    },
#                 "FibroLAN": {
                    #"SF 128B": "FibroLAN_NULL-1ms-60s-128B-NULL_txinject-TAS-no-CTS_1518_200.0percent.pcap",
#                    "CT 128B": "FibroLAN_NULL-1ms-60s-128B-NULL_txinject-TAS-CTS_1518_200.0percent.pcap"
#                    "SF 1518B": "FibroLAN_NULL-1ms-60s-1518B-NULL_txinject-TAS-no-CTS_1518_200.0percent.pcap",
#                    "CT 1518B": "FibroLAN_NULL-1ms-60s-1518B-NULL_txinject-TAS-CTS_1518_200.0percent.pcap"
                    }
                 }

#SOURCE_PATH_ROOT = "/mnt/harddrive/data/pcaps"
SOURCE_PATH_ROOT = "../workspace/network_validation/simulations/results/final"
OUTPUT_PATH_ROOT = "./"
mapping = {2: "robotic"}


# In[139]:


dfs = []

for vendor, config in CONFIGURATION.items():
    for qos, pcap in config.items():
        input_path = "{}/{}".format(SOURCE_PATH_ROOT, pcap)
        output_path = "{}/{}/{}".format(OUTPUT_PATH_ROOT, vendor, qos)

        pp = TsnParsePcap(path=input_path,
                          mapping=mapping,
                          output_path=output_path,
                          omnet_ts=True)
        pp.pcap_to_dfs()
        d = pp.get_dfs()
        dfs.append(d)

        cp = TsnCreatePlot(dfs=d,
                           output_path=output_path,
                           mapping=mapping,
                           bg_load=0,
                           bg_framesize=1518,
                           qos_type="None")
        cp.generate_plots(plot_type="latency_over_time", output="csv")
        # cp.generate_plots(plot_type="latency_ccdf", output="mpl")

dfs = []

for vendor, config in CONFIGURATION.items():
    for qos, pcap in config.items():
        filepath = "{}/{}/{}/csv/latency_over_time_robotic.csv".format(OUTPUT_PATH_ROOT, vendor, qos)
        print(filepath)
        df = read_csv(filepath)        
        df = df[["Latency (ns)"]]
        df.rename(columns={"Latency (ns)": "x-{}-{}".format(vendor, qos)},errors="raise",inplace=True)
        dfs.append(df)
del df
#df.describe()
df = concat(dfs,
            axis=1,
            join="outer",
            ignore_index=False)

del dfs
# change ps to us
df = df * 10**-6
df.describe()


# In[140]:


#filepath = "{}/{}/{}/csv/latency_ccdf_robotic.csv".format(OUTPUT_PATH_ROOT, vendor, qos)
#df = read_csv(filepath)


# In[141]:

def check_results(data,borders,testname):
	count=0
	logfile=open('checklog.txt', 'a')
	for limit in borders:

		if int(data[count]["delay"].quantile(0.25))<limit[0]:
			logfile.write(testname+" "+str(count)+" lower:FAIL\n")
		else:
			logfile.write(testname+" "+str(count)+" lower:OK\n")
		if int(data[count]["delay"].quantile(0.75))>limit[1]:
			logfile.write(testname+" "+str(count)+" upper:FAIL\n")
		else:
			logfile.write(testname+" "+str(count)+" upper:OK\n")
		count=count+1
	logfile.close()
df.describe()


# In[144]:


df1 = pd.DataFrame(df["x-Omnet-CTS 128B"]).assign(switch="Omnet-CTS 128B").assign(id=2)
df1.rename(columns={'x-Omnet-CTS 128B': 'delay'}, inplace=True)

df2 = pd.DataFrame(df["x-Omnet-CTS 1518B"]).assign(switch="Omnet-CTS 1518B").assign(id=4)
df2.rename(columns={'x-Omnet-CTS 1518B': 'delay'}, inplace=True)
df3 = pd.DataFrame(df["x-Omnet-noCTS 128B"]).assign(switch="Omnet-noCTS 128B").assign(id=1)
df3.rename(columns={'x-Omnet-noCTS 128B': 'delay'}, inplace=True)
df4 = pd.DataFrame(df["x-Omnet-noCTS 1518B"]).assign(switch="Omnet-noCTS 1518B").assign(id=3)
df4.rename(columns={'x-Omnet-noCTS 1518B': 'delay'}, inplace=True)
#df5 = pd.DataFrame(df["x-Omnet-A"]).assign(switch="Omnet-A").assign(id=5)
#df5.rename(columns={'x-Omnet-A': 'delay'}, inplace=True)
#df6 = pd.DataFrame(df["x-Omnet-B"]).assign(switch="Omnet-B").assign(id=6)
#df6.rename(columns={'x-Omnet-B': 'delay'}, inplace=True)
#df7 = pd.DataFrame(df["x-Omnet-C"]).assign(switch="Omnet-C").assign(id=7)
#df7.rename(columns={'x-Omnet-C': 'delay'}, inplace=True)
#df8 = pd.DataFrame(df["x-Omnet-D"]).assign(switch="Omnet-D").assign(id=8)
#df8.rename(columns={'x-Omnet-D': 'delay'}, inplace=True)
#df9 = pd.DataFrame(df["x-Omnet-E"]).assign(switch="Omnet-E").assign(id=9)
#df9.rename(columns={'x-Omnet-E': 'delay'}, inplace=True)
#df10 = pd.DataFrame(df["x-Omnet-F"]).assign(switch="Omnet-F").assign(id=10)
#df10.rename(columns={'x-Omnet-F': 'delay'}, inplace=True)
cdf = pd.concat([df1,df2,df3,df4]) 
#cdf =df1
mdf = pd.melt(cdf, id_vars=['switch'])
df1.describe().to_csv(OUTPUT_PATH_ROOT +"/Omnet-CTS 128B.csv")
df2.describe().to_csv(OUTPUT_PATH_ROOT +"/Omnet-CTS 1518B.csv")
df3.describe().to_csv(OUTPUT_PATH_ROOT +"/Omnet-noCTS 128B.csv")
df4.describe().to_csv(OUTPUT_PATH_ROOT +"/Omnet-noCTS 1518B.csv")
check_results([df1,df2,df3,df4],[[0,5],[0,5],[10,20],[2.5,7]],"TAStest")

# In[145]:


colors = ["#00305d",  # TUD Blue 100%
          "#2C94CC",  # ComNets Middle Blue
          "#E20074",  # ComNets Magenta
          ]

sns.set_palette(sns.color_palette(colors))

#fig, ax = plt.subplots(figsize=(6, 4))

plt.title("Packet delay", loc='left', fontsize=18)
#plt.title("Slave Clock Deviation", loc='right', fontsize=13, color='grey')
#plt.ylim(4800,5200)
sns.boxplot(x="id", y="delay us",hue="switch", data=cdf, fliersize=1, saturation=1, width=.6)

#sns.despine(offset=10, trim=True)

#plt.legend(bbox_to_anchor=(0.6, 0.85), loc='lower center', borderaxespad=0, ncol=3)

plt.grid(dict(visible=True,
              which='major',
              color='#CCD6DF',
              linestyle='-'))
plt.grid(dict(visible=True,
              which='minor',
              color='#CCD6DF',
              linestyle='--'))

#ax.set_ylabel("Deviation to GM [ns]")
#ax.set_xlabel('Sync Messages [1/s]')

plt.tight_layout()

plt.savefig(OUTPUT_PATH_ROOT +'/boxplot_omnet_TAS.png', dpi=300)
#plt.show()



