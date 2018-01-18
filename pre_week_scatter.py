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

predic = {}
for dat in date:
    f = open(path+'1706'+str(dat)+'08.000','r')
    rdata = f.readlines()
    f.close()
    print dat
    for i in range(14,len(rdata)):
        temp = rdata[i]
        if temp.split()[0] in predic.keys():
            predic[temp.split()[0]][3] += np.array(float(temp.split()[4]))
        else:
            predic[temp.split()[0]] = np.array(map(float,temp.split()[1:]))

points = np.array(predic.values())[:,0:2]
pre = np.array(predic.values())[:,3]
sta = predic.keys()

#print max(pre)

fig     = plt.figure()
ax      = fig.add_subplot(111)

#draw basemap
h=2000
m = Basemap(projection='nsper',lat_0=34,lon_0=108,satellite_height=h*1000.,resolution='l')

seacolor = 'darkslategrey'
landcolor = 'k'
bound = 'dimgray'
m.drawcountries(linewidth=0.5,color = bound)
m.drawcoastlines(linewidth=0.5,color = bound)
m.drawmapboundary(fill_color = seacolor)
m.fillcontinents(color = landcolor,lake_color=seacolor,zorder = 0)

##shapefile##
shapefile = 'D:\\python\\myfiles\\matplot\\map\\'+'CHN_adm0'
m.readshapefile(shapefile,'bbb',drawbounds =False, color = 'red', linewidth = 0.5)

patches   = []
for info, shape in zip(m.bbb_info, m.bbb):
    if info['SOVEREIGN'] in ['China','Taiwan']:
        patches.append( Polygon(np.array(shape), True) )
       
ax.add_collection(PatchCollection(patches, facecolor= 'k', edgecolor='white', linewidths=1, zorder=1))

##draw the province boundaries##
shapefilep = 'D:\\python\\myfiles\\matplot\\map\\'+'CHN_adm1'
m.readshapefile(shapefilep,'ppp',drawbounds =True, color = 'grey', linewidth = 0.5, zorder = 2)

####draw dots
points = np.array(points)
pre = np.array(pre)

indmx = [pre<=50, pre<=150, pre<=250, pre<=350, pre<=1000]
indmn = [pre>0, pre>50, pre>150, pre>250, pre>350]
label = ['0-50','50-100','100-150','150-200','>200']
color = ['c','aqua','aqua','aqua','aqua']
scale = [3.,8.,25.,30.,30.]
alphaindex = [1,1,1,1,1]

#for i in range(5):
#    ind = indmx[i] & indmn[i]
#    xx,yy = m(points[ind,0],points[ind,1])
#    m.scatter(xx, yy, pre[ind]/scale[i], marker='o',c = color[i], label = label[i], edgecolors='none', alpha = 1, zorder = 3)

for i in range(0,5):
    ind = indmx[i] & indmn[i]
    xx,yy = m(points[ind,0],points[ind,1])
    m.scatter(xx, yy, pre[ind]/scale[i], marker='o',c = color[i], label = label[i], edgecolors='none', alpha = alphaindex[i], zorder = 3)

#ax.legend(loc=7,facecolor = 'none',edgecolor = 'none')
plt.show()

for i in range(9):
    temp = max(pre)
    ind = np.argwhere(pre == temp)
    print temp , sta[ind]
    pre = np.delete(pre,ind)
    sta.remove(sta[ind])