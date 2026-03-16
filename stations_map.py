import json
import folium
from math import radians, sin, cos, sqrt, atan2

def distance(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = radians(lat2-lat1)
    dlon = radians(lon2-lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1))*cos(radians(lat2))*sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c

stations = []

with open("abcTransmissions.json") as f:
    for line in f:
        stations.append(json.loads(line))

max_distance = 0
isolated_station = None

for s1 in stations:
    lon1, lat1 = s1["location"]["coordinates"]
    min_distance = 999999

    for s2 in stations:
        if s1 == s2:
            continue

        lon2, lat2 = s2["location"]["coordinates"]
        d = distance(lat1, lon1, lat2, lon2)

        if d < min_distance:
            min_distance = d

    if min_distance > max_distance:
        max_distance = min_distance
        isolated_station = s1

print("Most isolated station:", isolated_station["name"])

m = folium.Map(location=[-25,133], zoom_start=4)

for s in stations:
    lon, lat = s["location"]["coordinates"]

    folium.CircleMarker(
        location=[lat, lon],
        radius=3,
        color="blue",
        fill=True
    ).add_to(m)

lon, lat = isolated_station["location"]["coordinates"]

folium.Marker(
    location=[lat, lon],
    popup="Most isolated: " + isolated_station["name"],
    icon=folium.Icon(color="red")
).add_to(m)

m.save("stations_map.html")

print("Map with isolated station saved")