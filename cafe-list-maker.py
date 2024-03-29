import urllib.request, json 

with urllib.request.urlopen("https://maps.googleapis.com/maps/api/geocode/json?address=google&key=AIzaSyCo0U_grJFvSAc5SLPFFn9mipWIZ3uTjEA") as url:
    data = json.load(url)
    print(data)

PARAMS = {'address':location}


# Spliting area for equal rectangles for search


#Function for getting latitude and longitude.

from math import asin, atan2, cos, degrees, radians, sin

def get_point_at_distance(lat1, lon1, d, bearing, R=6371):
    """
    lat: initial latitude, in degrees
    lon: initial longitude, in degrees
    d: target distance from initial
    bearing: (true) heading in degrees
    R: optional radius of sphere, defaults to mean radius of earth

    Returns new lat/lon coordinate {d}km from initial, in degrees
    """
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    a = radians(bearing)
    lat2 = asin(sin(lat1) * cos(d/R) + cos(lat1) * sin(d/R) * cos(a))
    lon2 = lon1 + atan2(
        sin(a) * sin(d/R) * cos(lat1),
        cos(d/R) - sin(lat1) * sin(lat2)
    )
    return (degrees(lat2), degrees(lon2),)


#test
#   
#
#
#
lat = 52.20472
lon = 0.14056
distance = 15
bearing = 90
lat2, lon2 = get_point_at_distance(lat, lon, distance, bearing)

# lat2  52.20444 - the lat result I'm hoping for
# lon2  0.36056 - the long result I'm hoping for.

print(lat2, lon2)
# prints "52.20451523755824 0.36067845713550956"
