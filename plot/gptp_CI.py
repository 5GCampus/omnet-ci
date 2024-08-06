#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# import
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import shutil
import seaborn as sns

'''
command_cd = "cd ../workspace/network_validation/simulations"
os.system(command_cd)
'''

tsn_results_path = "../workspace/network_validation/simulations/results/gPTP-test"
csv_output_path = "../workspace/network_validation/simulations/results/csv"
csv_file_name = "ptp"
os.system(f"opp_scavetool x {tsn_results_path}/*.vec -o {csv_output_path}/{csv_file_name}.csv")

df_mod = pd.read_csv(f"../workspace/network_validation/simulations/results/csv/ptp.csv")
df_filter_mod = df_mod[(df_mod.type == "vector") & (df_mod.name == "timeDifference:vector")].sort_values(by=["run"])

print(os.getcwd())

###    
#                plot the overtime clock deviation
###

#### Take 8 sync for example ####
def plot_clockchangeOverTime(df, subtitle):    
    # TSN Clock -- MASTER
    df_timeChange = df[(df.type == "vector") & (df.name == "timeChanged:vector") & (df.module == "gptp_withclock.tsnClock.clock")].sort_values(by=["run"])
    data1 = df_timeChange.iloc[0]
    master_value = np.array(str(data1.vecvalue).split(' '), dtype=np.float64)
    master_time = np.array(str(data1.vectime).split(' '), dtype=np.float64)

    #TSN Switch -- SLAVE
    df_timeChange = df[(df.type == "vector") & (df.name == "timeChanged:vector") & (df.module == "gptp_withclock.switch.clock")].sort_values(by=["run"])
    sync_8 = df_timeChange.iloc[0]
    sync_8_value = np.array(str(sync_8.vecvalue).split(' '), dtype=np.float64)
    sync_8_time = np.array(str(sync_8.vectime).split(' '), dtype=np.float64)

    #print(sync_8_time)
    timeDiff_master = (master_value-master_time)*10**9
    timeDiff_slave = (sync_8_value-sync_8_time)*10**9
    sns.reset_defaults()
    fig, ax = plt.subplots(figsize=(6, 4))
    colors = ["#00305d", "#2C94CC"]
    sns.set_palette(sns.color_palette(colors))
    plt.title("INET Synchronization", loc='left', fontsize=18)
    plt.title(subtitle, loc='right', fontsize=13, color='grey')
    #plt.title("Clock Deviation", loc='right', fontsize=13, color='grey')
    ax.set_ylabel("Deviation to Simulation Time [ns]")
    ax.set_xlabel('Simulation Time [s]')
    plt.plot(master_time, timeDiff_master, label="Master (Ideal Oscillator)", linewidth=2)
    plt.plot(sync_8_time, timeDiff_slave, label="Slave (Random Drift Oscillator)", linewidth=2)
    plt.legend()
    plt.grid(dict(visible=True,
                      which='major',
                      color='#CCD6DF',
                      linestyle='-'))
    plt.xlim([0,5])
    plt.savefig("gptp_overtime.png")
    plt.show()


plot_clockchangeOverTime(df_mod, "INET Modified")


###    
#                plot the clock deviation boxplot
###
def provide_dataArray(df_filter):
    sync_8 = df_filter.iloc[0]
    sync_16 = df_filter.iloc[1]
    sync_32 = df_filter.iloc[2]
    sync_64 = df_filter.iloc[3]
    sync_128 = df_filter.iloc[4]
    # convert data frame to array
    sync_8_floatarray=np.array(str(sync_8.vecvalue).split(' '),dtype=np.float64)*10**9
    sync_16_floatarray=np.array(str(sync_16.vecvalue).split(' '),dtype=np.float64)*10**9
    sync_32_floatarray=np.array(str(sync_32.vecvalue).split(' '),dtype=np.float64)*10**9
    sync_64_floatarray=np.array(str(sync_64.vecvalue).split(' '),dtype=np.float64)*10**9
    sync_128_floatarray=np.array(str(sync_128.vecvalue).split(' '),dtype=np.float64)*10**9
    # comine the nonzero arrays
    data_array = [sync_8_floatarray, sync_16_floatarray, sync_32_floatarray, sync_64_floatarray, sync_128_floatarray]
    return data_array

ptp_mod = provide_dataArray(df_filter_mod)

def box_plot(data_array, subtitle):
    import seaborn as sns
    sns.reset_defaults() 
     # sns.set_theme()
    colors = ["#00305d", "#2C94CC"]
    sns.set_palette(sns.color_palette(colors))
    fig, ax = plt.subplots(figsize=(6, 4))
    plt.title("INET Synchronization ", loc='left', fontsize=18)
    plt.title(subtitle, loc='right', fontsize=13, color='grey')
    #sns.boxplot(x="SyncInterval", y="value", hue="Switch", data=data_array, fliersize=1, saturation=1, width=.6)
    sns.boxplot(data=data_array,  showfliers = True,fliersize=1,color="#2C94CC", saturation=1, width=.6,linewidth=2,flierprops={"markersize": "3"})
    sns.despine(offset=10, trim=True)
    ax.set_xticklabels(['8','16','32','64','128'])
    plt.grid(dict(visible=True,
                  which='major',
                  color='#CCD6DF',
                  linestyle='-'))
    ax.set_ylabel("Deviation to GM [ns]")
    ax.set_xlabel('Sync Messages [1/s]')
    #plt.ylim([0, 10])
    plt.tight_layout()
    plt.savefig('gptp_boxplot.png')
    plt.show()

box_plot(ptp_mod, "Modified Design")

def check_results(data,borders,testname):
	count=0
	logfile=open('checklog.txt', 'a')
	for limit in borders:
		df_describe = pd.DataFrame(data[count])
		
		if int(df_describe.quantile(0.25))<limit[0]:
			logfile.write(testname+" "+str(count)+" lower:FAIL\n")
		else:
			logfile.write(testname+" "+str(count)+" lower:OK\n")
		if int(df_describe.quantile(0.75))>limit[1]:
			logfile.write(testname+" "+str(count)+" upper:FAIL\n")
		else:
			logfile.write(testname+" "+str(count)+" upper:OK\n")
		count=count+1
	logfile.close()
check_results(ptp_mod,[[-5,5],[-5,5],[-5,5],[-5,5],[-5,5]],"PTPtest")

