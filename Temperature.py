import folium
import geopandas as gpd
import webbrowser
from pprint import pprint
from jenkspy import jenks_breaks
# Create new map.
m = folium.Map(
    location=[42.38172, -71.111408],
    tiles='Stamen Toner',
    zoom_start=13
)
temp = gpd.read_file('./data/Temp/temperature.shp')
temp = temp.dropna(subset=['tem'])
temp.unary_union


jenks_breaks = jenks_breaks(temp['tem'], nb_class=5)
quantile_breaks = temp['tem'].quantile([0, 0.2, 0.4, 0.6, 0.8, 1])

pprint(temp.head().to_json())
m = folium.Map(
    location=[42.38172, -71.111408],
    tiles='Stamen Toner',
    zoom_start=13
)
temp = temp.to_crs(epsg=4326)
Tchoro = folium.Choropleth(
    geo_data = temp.to_json(),
    data = temp,
    columns = ['id', 'tem'],
    key_on = 'feature.properties.id',
    fill_color = 'YlOrRd',
    fill_opacity = 0.7,
    line_color = 'Orange',
    line_opaciy = 0.1,
    legend_name = 'Temperature per Square Mile',
    bins = jenks_breaks,
    highlight = True
).add_to(m)

tooltips = Tchoro.geojson.add_child(
    folium.GeoJsonTooltip(
        fields=['tem'], 
        aliases=['Temperature per mile^2'],
        localize=True,
    )
).add_to(m)

folium.TileLayer('Stamen Toner').add_to(m)

print(m.crs)
print(temp.crs)
# Draw map.
m.save("temp.html")
webbrowser.open("temp.html")
