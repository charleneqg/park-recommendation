# pip3 install basemap
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt


def plot_on_map(curlat, curlon, latlst, lonlst, names):
    min_lon = -119
    max_lon = -64
    min_lat = 22
    max_lat = 49
    min_lon = min(lonlst+[curlon]) - 0.2
    max_lon = max(lonlst+[curlon]) + 0.2
    min_lat = min(latlst+[curlat]) - 0.2
    max_lat = max(latlst+[curlat]) + 0.2
    map = Basemap(llcrnrlon=min_lon,llcrnrlat=min_lat,urcrnrlon=max_lon,urcrnrlat=max_lat,
            projection='lcc',lat_1=33,lat_2=45,lon_0=-95)
    shp_info = map.readshapefile('st99_d00','states',drawbounds=True,
                               linewidth=0.45,color='gray')

    map.drawmapboundary(fill_color='aqua')
    map.fillcontinents(color='coral',lake_color='aqua')
    # map.drawparallels(np.arange(0., 90., 5.), color='gray', dashes=[1, 3], labels=[1, 0, 0, 0])
    # map.drawmeridians(np.arange(0., 360., 15.), color='gray', dashes=[1, 3], labels=[0, 0, 0, 1])

    # map.fillcontinents(color='beige', lake_color='lightblue')
    map.drawcountries()

    # lons = [-118.2851]
    # lats = [34.0224]

    x, y = map([curlon], [curlat])
    map.scatter(x, y, marker='*',color='yellow')

    x2, y2 = map(lonlst, latlst)
    map.scatter(x2, y2, marker='.', color='green')

    idx = 0
    for name in names:
        # xa, ya = map(x2[idx]+0.3, y2[idx]+0.3)
        # plt.annotate(name, xy=(x2[idx], y2[idx]), xycoords='data',
        #              # xytext=(xa, ya),
        #              textcoords='data',
        #              color='white',
        #
        #              # arrowprops=dict(arrowstyle="->")
        #              )
        plt.text(x2[idx], y2[idx], name, fontsize=6, fontweight='bold',
                 ha='left', va='center', color='k',
                 # bbox=dict(facecolor='b', alpha=0.2)
                 )
        idx += 1
    line1 = plt.Line2D(range(10), range(10), marker='*', color="yellow")
    line2 = plt.Line2D(range(10), range(10), marker='.', color="green")
    plt.legend((line1, line2), ('Your Location', 'Park Location'), numpoints=1,
               loc=1)

    parallels = np.arange(0., 81, 0.1)
    # labels = [left,right,top,bottom]
    map.drawparallels(parallels, labels=[False, True, True, False])
    meridians = np.arange(10., 351., 0.1)
    map.drawmeridians(meridians, labels=[True, False, False, True])
    plt.show()
