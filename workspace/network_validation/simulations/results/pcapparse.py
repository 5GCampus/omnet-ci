from dpkt.pcap import Reader
from decimal import Decimal
from math import ceil, floor
import pandas as pd
import matplotlib.pyplot as plt
f = open("server2.pcap", "rb")
pcap = Reader(f)
x=[]
y=[]
# omnet pcaps are strange, use dd if="server.pcap" of="server2.pcap" bs=1 skip=8  
for ts, buf in pcap:
  hexstream = buf.hex()
#  print(hexstream[92:108])
  tx_ts= int(hexstream[96:112], 16)
  rx_ts= int(hexstream[112:128], 16)
#  print(str(hexstream[96:112])+" "+str(hexstream[112:128]))
  delay=rx_ts-tx_ts
  length=len(buf)
#  print(str(length)+"  "+str(delay))
  x.append(length)
  y.append(delay)
  
df=pd.DataFrame({"length":x,"delay":y})
#print(df)
df.plot(x='length', y='delay', kind='scatter')	
plt.show()
