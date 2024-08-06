import json
import pandas as pd
import matplotlib.pyplot as plt
from collections import ChainMap
  
# Opening JSON file
f = open('packetsizedelay_ct.json')
data = dict(ChainMap(*json.load(f).values())) 
packetsizes=data["vectors"][0]
df1=pd.DataFrame({"time":packetsizes["time"],"value":packetsizes["value"],"eventnumber":packetsizes["eventnumber"]})
packetdelays=data["vectors"][1]
df2=pd.DataFrame({"time":packetdelays["time"],"value":packetdelays["value"],"eventnumber":packetdelays["eventnumber"]})
combine=pd.merge(df1,df2,on=['time'],how='inner')
combine.plot(x='value_x', y='value_y', kind='scatter')	
#plt.show()
plt.savefig('delay_ct.png')
#print(combine)
f.close()

f = open('packetsizedelay.json')
data = dict(ChainMap(*json.load(f).values())) 
packetsizes=data["vectors"][0]
df1=pd.DataFrame({"time":packetsizes["time"],"value":packetsizes["value"],"eventnumber":packetsizes["eventnumber"]})
packetdelays=data["vectors"][1]
df2=pd.DataFrame({"time":packetdelays["time"],"value":packetdelays["value"],"eventnumber":packetdelays["eventnumber"]})
combine=pd.merge(df1,df2,on=['time'],how='inner')
combine.plot(x='value_x', y='value_y', kind='scatter')	
#plt.show()
plt.savefig('delay.png')
#print(combine)
f.close()
