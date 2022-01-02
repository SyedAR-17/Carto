import geopandas as gpd
import matplotlib.pyplot as plt
cambridge_trees = gpd.read_file('data/cambridge_trees.shp')
hex_bins = gpd.read_file('data/hex_bins.shp')
tree_count = gpd.sjoin(cambridge_trees, hex_bins, how='inner', op='intersects')
tree_count = tree_count.dissolve(by='id', aggfunc='count')
tree_count = tree_count.rename({'index_right': 'tree_count'}, axis='columns')
tree_count = tree_count.drop(columns='geometry')
hex_bins = hex_bins.merge(tree_count, left_on='id', right_on='id', how='left')
hex_bins['area'] = hex_bins.geometry.area
hex_bins['area_sqmi'] = hex_bins.area / 2.788e+7
water = gpd.read_file('data/water.shp')
water = water.to_crs(hex_bins.crs)
hex_bins_water = gpd.overlay(hex_bins, water, how='intersection')
hex_bins_water = hex_bins_water[['id', 'geometry']]
hex_bins_water['water_area'] = hex_bins_water.area
hex_bins_water = hex_bins_water.dissolve(by='id', aggfunc='sum')
hex_bins_water = hex_bins_water.drop(columns='geometry')
hex_bins = hex_bins.merge(hex_bins_water, left_on='id', right_on='id', how='left')
values = {'water_area': 0}
hex_bins = hex_bins.fillna(value=values)
hex_bins['land_area'] = hex_bins.area - hex_bins.water_area
hex_bins['land_area_sqmi'] = hex_bins.land_area / 2.788e+7
hex_bins['trees_p_sqft'] = hex_bins['tree_count'] / hex_bins['land_area']
hex_bins['trees_p_sqmi'] = hex_bins['tree_count'] / hex_bins['land_area_sqmi']
hex_bins.plot(column='trees_p_sqmi')
hex_bins.to_file('trees_p_area.shp')
hex_bins.to_file('trees_p_area.geojson', driver='GeoJSON')
hex_bins.to_file('trees_p_area.gpkg', driver='GPKG')
plt.show()






