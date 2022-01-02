import folium
import geopandas as gpd
import webbrowser
from pprint import pprint
from jenkspy import jenks_breaks
from ctypes.test.test_pickling import name
# Create new map.
m = folium.Map(
    location=[42.38172, -71.111408],
    tiles='Stamen Toner',
    zoom_start=13
)
trees = gpd.read_file('data/sq_trees.shp')
trees = trees.dropna(subset=['trees_p_sq'])
trees.unary_union


jenks_breaks = jenks_breaks(trees['trees_p_sq'], nb_class=5)
quantile_breaks = trees['trees_p_sq'].quantile([0, 0.2, 0.4, 0.6, 0.8, 1])

pprint(trees.head().to_json())
m = folium.Map(
    location=[42.38172, -71.111408],
    tiles='Stamen Toner',
    zoom_start=13
)
trees = trees.to_crs(epsg=4326)
choro = folium.Choropleth(
    geo_data = trees.to_json(),
    data = trees,
    columns = ['id', 'trees_p_sq'],
    key_on = 'feature.properties.id',
    fill_color = 'YlGn',
    fill_opacity = 0.7,
    line_color = 'Green',
    line_opaciy = 0.1,
    legend_name = 'Public Trees per Square Mile',
    bins = jenks_breaks,
    highlight = True
).add_to(m)

tooltips = choro.geojson.add_child(
    folium.GeoJsonTooltip(
        fields=['trees_p_sq'], 
        aliases=['Trees per mile^2'],
        localize=True,
        name="Trees"
    )
).add_to(m)





print(m.crs)
print(trees.crs)
# Draw map.
m.save("trees.html")
webbrowser.open("trees.html")
