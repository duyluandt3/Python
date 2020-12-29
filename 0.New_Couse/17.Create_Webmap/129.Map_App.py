import folium
import pandas

# Read data from txt file
data = pandas.read_csv("Volcanoes_USA.txt")
# Get coordinate from txt file
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])
name = list(data["NAME"])

# Link to google search
html = """
Volcano name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""

map = folium.Map(location=[38.58, -99.09], zoom_start=6, tiles="Stamen Terrain")

# Add a child map and control layer
fgv = folium.FeatureGroup(name="Volcanoes")

# add multi coordinate
#user_location = [[38.2, -99.1], [37.2, -97.1]]
#for coordinates in user_location:

# Change color of item depend elevation
def chang_color(elevation):
    if elevation < 1000:
        return "green"
    elif not 1000 >= elevation and elevation < 3000:
        return "orange"
    else:
        return "red"

# read coordinate at the same times (Layer 1)
for lt, ln, el, name in zip(lat, lon, elev, name):
    iframe = folium.IFrame(html=html % (name, name, el), width=200, height=100)
    # Maker
    #fg.add_child(folium.Marker(location=[lt, ln], popup=folium.Popup(iframe),
    #                           icon = folium.Icon(color = chang_color(el), icon='info-sign')))
    #Circurle Maker
    fgv.add_child(folium.CircleMarker(location=[lt, ln], radius=6,popup=folium.Popup(iframe),
                                     fill_color=chang_color(el), color="grey", fill_opacity=1,
                                     fill=True))
######## Layer 2 #########
fgp = folium.FeatureGroup(name="Population")
# Add polygon for map (Layer 2)
fgp.add_child(folium.GeoJson(data=open("world.json", "r", encoding="utf-8-sig").read(),
                            style_function=lambda x: {"fillColor": "green"
                            if x["properties"]["POP2005"]<10000000 else "orange"
                            if 10000000<=x["properties"]["POP2005"]<20000000 else "red"}))
# Add layer 1 (Location)
map.add_child(fgv)
# Add layer 2 (Polygon)
map.add_child(fgp)
#add a map controller (Layer 3)
map.add_child(folium.LayerControl())
map.save("Map1.html")