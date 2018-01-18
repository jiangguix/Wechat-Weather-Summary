import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.patches import PathPatch

filename = '17061608.000'
path = 'D:\\python\\myfiles\\matplot\\'
pathh = 'I:\\mdata\\500\\'
pathuv = 'I:\\mdata\\uv\\'
f = open(pathh+filename,'r')
rdata = f.readlines()
f.close()

lonnum = len(rdata[4:])/15

datanum = ['']*lonnum

for j in range(lonnum):
 data = ''
 for i in range(15):
  data += rdata[4+j*15+i]

 datanum[j] = [float(i) for i in data.split()]

f = open(pathuv+filename,'r')
rdata = f.readlines()
f.close()

lonnum = len(rdata[3:])/15/2

datanumu = ['']*lonnum
datanumv = ['']*lonnum

for j in range(lonnum):
 datau = ''
 datav = ''
 for i in range(15):
  datau = datau + rdata[3+j*15+i]
  datav = datav + rdata[3+j*15+lonnum*15+i]

 datanumu[j] = [float(i) for i in datau.split()]
 datanumv[j] = [float(i) for i in datav.split()]
# print datanumv[-1]
 
fig     = plt.figure()
ax      = fig.add_subplot(111)

seacolor = 'darkslategray'
landcolor = 'k'
bound = 'dimgray'
m = Basemap(projection='nsper',lat_0=38,lon_0=100,satellite_height=6000000,resolution='l')
m.drawcountries(linewidth=0.5,color = bound)
m.drawcoastlines(linewidth=0.5,color = bound)
m.drawmapboundary(fill_color = seacolor)
m.fillcontinents(color = landcolor,lake_color=seacolor,zorder = 0)
#m.warpimage(image='D:\python\Python2.7\land_shallow_topo_8192.tif')
# draw parallels.
#parallels = np.arange(0.,90,10.)
#m.drawparallels(parallels,labels=[1,0,0,0],fontsize=10)
# draw meridians
#meridians = np.arange(-180.,180.,10.)
#m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=10)

lats = np.linspace(90,-90,73)
lons = np.linspace(0,360,145)
lons,lats = np.meshgrid(lons,lats)
x,y = m(lons,lats)

u = np.array(datanumu)
v = np.array(datanumv)
speed = np.sqrt(u*u + v*v)
#u = np.ma.masked_where(speed<8,u)
#v = np.ma.masked_where(speed<8,v)
bondl = 0
bondr = 145
bondu = 73
m.quiver(x[:bondu,bondl:bondr], y[:bondu,bondl:bondr], u[:bondu,bondl:bondr], v[:bondu,bondl:bondr],speed[:bondu,bondl:bondr],
         cmap = 'gray', pivot='mid', scale=1000, zorder = 3)

##shapefile##
shapefile = path+'\\map\\CHN_adm0'
m.readshapefile(shapefile,'bbb',drawbounds =False, color = 'red', linewidth = 0.5)
#print type(m.bbb_info[0])
patches   = []
for info, shape in zip(m.bbb_info, m.bbb):
    if info['SOVEREIGN'] in ['China','Taiwan']:
        patches.append( Polygon(np.array(shape), True) )
        
ax.add_collection(PatchCollection(patches, facecolor= 'k', edgecolor='white', linewidths=0.5, zorder=1))

##draw the province boundaries##
shapefilep = path+'\\map\\'+'CHN_adm1'
m.readshapefile(shapefilep,'ppp',drawbounds =True, color = 'grey', linewidth = 0.5, zorder = 2)

cs = m.contour(x,y,datanum,20,linewidths = 1, colors = 'cyan')
plt.clabel(cs, fmt='%5.1f', fontsize=7)
#m.bluemarble()

plt.show()
