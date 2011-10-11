from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import gzip, os
from netCDF4 import Dataset

# create a land/sea mask using GMT grdlandmask utility.
# this script reads the file generated by grdlandmask, plots it, 
# and saves it in the format that Basemap._readlsmask expects.
# Default lsmask_5min.bin created with:
# grdlandmask -F -Ggrdlandmask5min_i.nc -I5m -R-180/180/-90/90 -Di -N0/1/2/1/2 -A100+l


# run grdlandmask
resolution = 'i' # gshhs resolution
grid = '5' # grid size in minutes
filename = 'grdlandmask%smin_%s.nc' % (resolution,grid)
cmd = \
'grdlandmask -F -G%s -I%sm -R-180/180/-90/90 -Di -N0/1/2/1/2 -A100+l' % \
(filename, grid)
os.system(cmd)

# read in data.
nc = Dataset(filename)
lons = nc.variables['x'][:]
nlons = len(lons)
lats = nc.variables['y'][:]
nlats = len(lats)
lsmask = nc.variables['z'][:].astype(np.uint8)

# plot
m =\
Basemap(llcrnrlon=-180,llcrnrlat=-90,urcrnrlon=180,urcrnrlat=90,resolution=resolution,projection='mill')
m.drawcoastlines() # coastlines should line up with land/sea mask.
m.drawlsmask(land_color='coral',ocean_color='aqua',lsmask=lsmask,lsmask_lons=lons,lsmask_lats=lats,lakes=True)
plt.title('%s by %s land-sea mask (resolution = %s) from grdlandmask' %\
        (nlons,nlats,resolution))

# write out.
f = gzip.open('lsmask_%smin.bin' % grid,'wb')
f.write(lsmask.tostring())
f.close()

plt.show()
