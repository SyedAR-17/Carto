import folium
import folium.plugins
import geopandas as gpd
import webbrowser
from pprint import pprint
from jenkspy import jenks_breaks
from folium.map import LayerControl
# Create new map.
map = folium.plugins.DualMap(
    location=[42.38172, -71.111408],
    zoom_start=13
)
trees = gpd.read_file('data/sq_trees.shp')
trees = trees.dropna(subset=['trees_p_sq'])
trees.unary_union


jenks_breaks = jenks_breaks(trees['trees_p_sq'], nb_class=5)
quantile_breaks = trees['trees_p_sq'].quantile([0, 0.2, 0.4, 0.6, 0.8, 1])

pprint(trees.head().to_json())
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
).add_to(map)

tooltips = choro.geojson.add_child(
    folium.GeoJsonTooltip(
        fields=['trees_p_sq'], 
        aliases=['Trees per mile^2'],
        localize=True,
        name="Trees"
    )
).add_to(map)


folium.TileLayer('Stamen Toner').add_to(map)
folium.TileLayer('cartodbdark_matter').add_to(map)

folium.LayerControl().add_to(map)

# Draw map.
map.save("Dualmap.html")
webbrowser.open("Dualmap.html")
