from SOlib.outputfile import OutputFile
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.patheffects as PathEffects
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import cartopy.feature as cfeature
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature
from matplotlib import colors

file = OutputFile("AnnuallyOut.nc")

pftVariables = file.PFTVarNames
patchVariables = file.PatchVarNames
nGridcells = file.gridcellDim.size
nPFTs = file.pftDim.size

print("This dataset ranges from "+ str(file.yearBegin)  + " to " + str(file.yearEnd))
print("and has "+ str(nGridcells) + " gridcells")
print("and has " + str(nPFTs) + " PFTs")
print("PFT variables: " + str(pftVariables))
print("Patch variables: " + str(patchVariables))
#Todo this has to be read out
#print("and contains the following PFTS: " + str(file.PFTVarNames))

yearBegin = 1995
yearEnd = 2010
var = "gpp"

#Read data
#For example variable "npp" using all gridcells of this file and the range from 1995 to 2010 (inclusive!)
#The last dimension nPFTS refelects the selecte pftID, this last entry (nPFTs is the total of all the PFTS before)
#e.g. ["TrBE", "C4G", "C3G", "Total"]
data = file.GetMultiPFT(var, 0, nGridcells, yearBegin, yearEnd, nPFTs - 1)



#Set some custom colors and boundaries
bounds = np.arange(1.5, 2.8, step=0.1)
norm = colors.BoundaryNorm(boundaries=bounds, ncolors=256)
cmap = 'YlGn'



fig = plt.figure(figsize=(16,18))
for i in range(0,16):

    img = file.CreateImage(data[:, i], 0.5)
    img_extent = file.IMG_extent
    offset = [-3, 3, -3, 3]

    axGeo = fig.add_subplot(4, 4, i + 1 , projection=ccrs.PlateCarree())
    lon_formatter = LongitudeFormatter(zero_direction_label=True, number_format='g')
    lat_formatter = LatitudeFormatter()
    axGeo.xaxis.set_major_formatter(lon_formatter)
    axGeo.yaxis.set_major_formatter(lat_formatter)
    axGeo.add_feature(cfeature.BORDERS, edgecolor='tab:grey')
    axGeo.coastlines(resolution='110m', linewidth=1, color='tab:grey')

    axGeo.set_extent(list(np.array(img_extent) + np.array(offset)), crs=ccrs.PlateCarree())

    axGeo.text(-80, 4, yearBegin + i ,
               fontsize=10,  horizontalalignment='left', verticalalignment='center',
               bbox=dict(facecolor='white', alpha=0.8, edgecolor='white'))

    axGeo.set_xticks([-80, -70, -60, -50], crs=ccrs.PlateCarree())
    axGeo.set_yticks([-20, -15, -10, -5, 0, 5], crs=ccrs.PlateCarree())
    axGeo.set_xlabel(r'Longitude')
    axGeo.set_ylabel(r'Latitude')

    imsh = axGeo.imshow(img, transform=ccrs.PlateCarree(), extent=img_extent, cmap=cmap, norm = norm)

plt.subplots_adjust(bottom=0.1, top=0.85, hspace=0.3)
cax = plt.axes([0.126, 0.95, 0.775, 0.02])
bar = plt.colorbar(imsh, cax=cax, orientation="horizontal")
bar.set_label(var + ' [' + file.GetUnit((var)) + ']', size = 14)
plt.show()
