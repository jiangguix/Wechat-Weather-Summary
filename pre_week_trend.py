from matplotlib.patches import PathPatch
from matplotlib.path import Path
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

#read in data and save them as lat,lon, pre, respectively
path = 'I:\\mdata\\pre\\'

date = range(12,19)

trend = []
#scopesw = [24,30,110,123]
scopesw = [20,25,105,118]
for dat in date:
    f = open(path+'1706'+str(dat)+'08.000','r')
    rdata = f.readlines()
    f.close()
    print dat
    count = 0
    pre = 0.
    for i in range(14,len(rdata)):
        temp = map(float,rdata[i].split())
        if temp[2]>scopesw[0] and temp[2]<scopesw[1] and temp[1]>scopesw[2] and temp[1]<scopesw[3]:
            pre += temp[4]
            count +=1
    pre /=count
    trend.append(pre)

#print max(pre)

fig     = plt.figure()
ax      = fig.add_subplot(111)

x = range(1,8)
#ax.plot(x,trend,'-',color = 'cyan',lw=3)
ax.fill_between(x,0,trend,color = 'c')
plt.grid(True)

plt.show()