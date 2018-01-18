from matplotlib.patches import PathPatch
from matplotlib.path import Path
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

#read in data and save them as lat,lon, pre, respectively
path = 'D:\\python\\myfiles\\black charts\\'

filer = 'macbok.txt'

f = open(path+filer,'r')
rdata = f.readlines()
f.close()

lat = []
lon = []
inten = []
for i in rdata:
    lat.append(float(i.split()[1]))
    lon.append(float(i.split()[2]))
    inten.append(int(i.split()[3]))

fig     = plt.figure()
ax      = fig.add_subplot(111)

#draw basemap
#h=1000
#m = Basemap(projection='nsper',lat_0=20,lon_0=112,satellite_height=h*1000.,resolution='l')
m = Basemap(width=3000000,height=2000000,projection='lcc',
            resolution='f',lat_1=22.,lat_2=30,lat_0=26,lon_0=112.)

seacolor = 'white'
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
xx,yy = m(lon,lat)
m.scatter(xx, yy, inten, marker='o',c = 'cyan', edgecolors='none', alpha = 1, zorder = 3)

plt.show()