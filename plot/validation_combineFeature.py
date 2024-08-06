#!/usr/bin/env python
# coding: utf-8

# # For combine feature box plot
# - A: no QoS, SF
# - B: no QoS, CT
# - C: TAS, CT
# - D: FP, SF
# - E: FP, CT
# - F: FP, TAS, CT

# In[1]:


from utils.parsePcap import TsnParsePcap
from utils.createPlot import TsnCreatePlot
from pandas import read_csv, concat, cut
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


# In[92]:


CONFIGURATION = {
    "Omnet_Howhang": {
                     "A": "omnet_robotic-NULL-NULL_final-A_1518_200.0percent.pcap",
                     "B": "omnet_robotic-NULL-NULL_final-B_1518_200.0percent.pcap",
                     "C": "omnet_robotic-NULL-NULL_final-C_1518_200.0percent.pcap",
                     "D": "omnet_robotic-NULL-NULL_final-D_1518_200.0percent.pcap",
                     "E": "omnet_robotic-NULL-NULL_final-E_1518_200.0percent.pcap",
                     "F": "omnet_robotic-NULL-NULL_final-F_1518_200.0percent.pcap"
    }
}

SOURCE_PATH_ROOT = "../workspace/network_validation/simulations/results/final"
OUTPUT_PATH_ROOT = "./"
mapping = {2: "robotic"}


# In[103]:


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


# In[104]:

def check_results(data,borders,testname):
	count=0
	logfile=open('checklog.txt', 'a')
	for limit in borders:

		if int(data[count].quantile(0.25))<limit[0]:
			logfile.write(testname+" "+str(count)+" lower:FAIL\n")
		else:
			logfile.write(testname+" "+str(count)+" lower:OK\n")
		if int(data[count].quantile(0.75))>limit[1]:
			logfile.write(testname+" "+str(count)+" upper:FAIL\n")
		else:
			logfile.write(testname+" "+str(count)+" upper:OK\n")
		count=count+1
	logfile.close()


df5 = pd.DataFrame(df["x-Omnet_Howhang-A"]).assign(configuration="SF").assign(id='A')
df5.rename(columns={'x-Omnet_Howhang-A': 'delay'}, inplace=True)
df6 = pd.DataFrame(df["x-Omnet_Howhang-B"]).assign(configuration="CT").assign(id='B')
df6.rename(columns={'x-Omnet_Howhang-B': 'delay'}, inplace=True)
df7 = pd.DataFrame(df["x-Omnet_Howhang-C"]).assign(configuration="TAS+CT").assign(id='C')
df7.rename(columns={'x-Omnet_Howhang-C': 'delay'}, inplace=True)
df8 = pd.DataFrame(df["x-Omnet_Howhang-D"]).assign(configuration="FP+SF").assign(id='D')
df8.rename(columns={'x-Omnet_Howhang-D': 'delay'}, inplace=True)
df9 = pd.DataFrame(df["x-Omnet_Howhang-E"]).assign(configuration="FP+CT").assign(id='E')
df9.rename(columns={'x-Omnet_Howhang-E': 'delay'}, inplace=True)
df10 = pd.DataFrame(df["x-Omnet_Howhang-F"]).assign(configuration="FP+CT+TAS").assign(id='F')
df10.rename(columns={'x-Omnet_Howhang-F': 'delay'}, inplace=True)
cdf = pd.concat([df5,df6,df7,df8,df9,df10]) 
mdf = pd.melt(cdf, id_vars=['configuration'])
mdf.set_flags(allows_duplicate_labels=False)

check_results([df5,df6,df7,df8,df9,df10],[[35,50],[15,30],[5,15],[30,38],[10,20],[5,15]],"Combinedtest")

# In[105]:
cdf.reset_index(level=0, inplace=True)

colors = ["#00305d",  # TUD Blue 100%
          "#2C94CC",  # ComNets Middle Blue
          "#E20074",  # ComNets Magenta
          #"#192D64",
          # "#326491",
          "#649BBE",
          # "#A0DCF0",
          "#0A9BA0",
          # "#37B48C",
          "#A0C850",
          # "#CDDC28"
          ]

sns.set_palette(sns.color_palette(colors))

fig, ax = plt.subplots(figsize=(6, 4))

plt.title("Combine Feature Measurement", loc='left', fontsize=18)
plt.title("", loc='right', fontsize=13, color='grey')
#plt.ylim(4800,5200)
sns.boxplot(x="id", y="delay",hue="configuration", data=cdf, fliersize=1, saturation=1, width=.6)

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

ax.set_ylabel("Delay [us]")
ax.set_xlabel('Config')

plt.tight_layout()

plt.savefig(OUTPUT_PATH_ROOT +'combineFeature.png', dpi=300)
#plt.show()


# ## OMNeT++ vector approach
# - extract meanBitLifeTime vector
