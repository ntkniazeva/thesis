### The code processes spatial data from two DataFrames,
### finds the nearest geothermal plant for each vertex,
### assigns relevant information.

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

#Read shapefiles into GeoDataFrames.
ver = gpd.read_file('shp/vertices.shp')
geothermal = gpd.read_file('districtHeatingPlants_results/geothermalPlant.shp/geothermalPlant.shp.shp')

#GeoDataFrames have different CRS. We convert CRS of vertices to EPSG 4326.
ver.to_crs(4326, inplace=True)

#Find the nearest geothermal plant indices for each vertex in 'ver':
[_, indices] = geothermal.sindex.nearest(geometry=ver.geometry)
print(indices)

#Plot geothermal plants(default - in blue) and vertices(in red) on the same plot.
vis1 = geothermal.plot()
ver.plot(ax=vis1, color='red')
plt.show()

#For each vertex, assign the 'inst_cap' and 'Name' values from the corresponding geothermal plant (from 'geothmMWt' and 'Name').
for i, v in enumerate(indices):
    ver.loc[i, 'inst_cap'] = geothermal.loc[v, 'geothmMWt']
    ver.loc[i, 'Name'] = geothermal.loc[v, 'Name']

#Set a value for 'cost_heat' for each vertices.
ver.loc[ver['cost_heat'] == 0, 'cost_heat'] = 0.05

#Reorder columns.
ver.insert(2, 'Name', ver.pop('Name'))
print(ver)

#Save the GeoDataFrame to a new shapefile.
ver.to_file('shp/filter.shp')