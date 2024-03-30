from math import asin, atan2, cos, degrees, radians, sin

# Spliting area for equal rectangles for search
#Function for getting latitude and longitude.
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

"""
Area of interest:
start laitude:
   -34.29770246404621
start longitude:
   150.94208464547222
"""

startLat = -34.29770
startLon = 150.94208

"""
end laitude:
   -34.59866418267474 
end longitude:
   150.74770345360713
"""

endLat = -34.59866
endLon = 150.74770

#Get initial points for lat and lon
iniLats = [startLat] 
iniLons = [startLon] 

lat = startLat
lon = startLon

distance = 3
bearing = 180

while lat > endLat:
    lat2, lon2 = get_point_at_distance(lat, lon, distance, bearing)
    iniLats.append(round(lat2,5))
    lat = lat2
iniLats.append(endLat)

if iniLats[-2] < iniLats[-1]:
    del(iniLats[-2])

distance = 1.7
bearing = 270

while lon > endLon:
    lat2, lon2 = get_point_at_distance(lat, lon, distance, bearing)
    iniLons.append(round(lon2, 5))
    lon = lon2
iniLons.append(round(endLon, 5)) 

# Sometime calculations go beyond the boundaries.
if iniLons[-2] < iniLons[-1]:
    del(iniLons[-2])

# Print resulted lists
#print(f"iniLats {iniLats}")
#print(f"iniLons {iniLons}")

# Make list for center points of each cell 
centerPoints = []

# Set initial values
lat = startLat
lon = startLon

# Generating starting poionts
for lonItem in iniLons:
    centerPoints.append([startLat, lonItem])

for index, latItem in enumerate(iniLats):
    if index > 0:
        centerPoints.append([latItem, startLon])

# Generating center poionts for each cell
for point in centerPoints:    
    bearing = 213
    distance = 1.79
    lat2, lon2 = get_point_at_distance(point[0], point[1], distance, bearing)
    if lat2 > endLat and lon2 > endLon:
        centerPoints.append([round(lat2,5), round(lon2,5)])

#Print results
#print(f"centerPoints \n{centerPoints}")
#print(f"Statistic\nInitial latitudes: {len(iniLats)}\nInitial longitudes: {len(iniLons)}\nnumber of center points indide the area: {len(centerPoints)} ")

#START SCRAPING NOW

#Надо написать закпрос на получение кафе

for index, point in enumerate(centerPoints):
    blablabla = 0        



#Надо написать запрос на получение отзывов по каждлому кафе по времени. Нужно имя и оценка по placeId

#REQUESTS HERE
    

#required steps:
# 1. Create table for cafes. Table for features. Table for 
#
#

""" 
places.accessibilityOptions, places.addressComponents, places.adrFormatAddress, places.businessStatus, places.displayName, places.formattedAddress, places.googleMapsUri, places.iconBackgroundColor, places.iconMaskBaseUri, places.id, places.location, places.name*, places.photos, places.plusCode, places.primaryType, places.primaryTypeDisplayName, places.shortFormattedAddress, places.subDestinations, places.types, places.utcOffsetMinutes, places.viewport

* The places.name field contains the place resource name in the form: places/PLACE_ID. Use places.displayName to access the text name of the place.

The following fields trigger the Nearby Search (Advanced) SKU:

places.currentOpeningHours, places.currentSecondaryOpeningHours, places.internationalPhoneNumber, places.nationalPhoneNumber, places.priceLevel, places.rating, places.regularOpeningHours, places.regularSecondaryOpeningHours, places.userRatingCount, places.websiteUri

The following fields trigger the Nearby Search (Preferred) SKU:

places.allowsDogs, places.curbsidePickup, places.delivery, places.dineIn, places.editorialSummary, places.evChargeOptions, places.fuelOptions, places.goodForChildren, places.goodForGroups, places.goodForWatchingSports, places.liveMusic, places.menuForChildren, places.parkingOptions, places.paymentOptions, places.outdoorSeating, places.reservable, places.restroom, places.reviews, places.servesBeer, places.servesBreakfast, places.servesBrunch, places.servesCocktails, places.servesCoffee, places.servesDesserts, places.servesDinner, places.servesLunch, places.servesVegetarianFood, places.servesWine, places.takeout """
