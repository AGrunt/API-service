import json
import requests

#START SCRAPING NOW

#Надо написать закпрос на получение кафе

# Params initialisation       
# Key for API
APIKEY = ""


#TEST LOCATION:
#-34.2977, 150.94208
latitude = -34.2977
longitude = 150.94208
#Nearbyserach url
nearbyURL = "https://places.googleapis.com/v1/places:searchNearby"

#Request's location params: types of places, max number of results (20 is max for API), center of circle location with radius.
nearbyParams = {
    "includedTypes": ["restaurant", "cafe"],
    "maxResultCount": 20,
    "locationRestriction": {
        "circle": {
        "center": {
        "latitude": latitude,
        "longitude": longitude},
        "radius": 1000.0
        }
    }
}

print(nearbyParams)

string = 'IncludedTypes: [restaurant, cafe], maxResultCount: 20, locationRestriction: {circle: {center: {latitude: -34.2977, longitude: 150.94208}, radius: 1000.0}}}'

print(string) 

#requested fields
#Available fields
#places.accessibilityOptions, places.addressComponents, places.adrFormatAddress, places.businessStatus, places.displayName, places.formattedAddress, places.googleMapsUri, places.iconBackgroundColor, places.iconMaskBaseUri, places.id, places.location, places.name*, places.photos, places.plusCode, places.primaryType, places.primaryTypeDisplayName, places.shortFormattedAddress, places.subDestinations, places.types, places.utcOffsetMinutes, places.viewport
#places.currentOpeningHours, places.currentSecondaryOpeningHours, places.internationalPhoneNumber, places.nationalPhoneNumber, places.priceLevel, places.rating, places.regularOpeningHours, places.regularSecondaryOpeningHours, places.userRatingCount, places.websiteUri
#places.allowsDogs, places.curbsidePickup, places.delivery, places.dineIn, places.editorialSummary, places.evChargeOptions, places.fuelOptions, places.goodForChildren, places.goodForGroups, places.goodForWatchingSports, places.liveMusic, places.menuForChildren, places.parkingOptions, places.paymentOptions, places.outdoorSeating, places.reservable, places.restroom, places.reviews, places.servesBeer, places.servesBreakfast, places.servesBrunch, places.servesCocktails, places.servesCoffee, places.servesDesserts, places.servesDinner, places.servesLunch, places.servesVegetarianFood, places.servesWine, places.takeout 

nearbyFields = ["places.id", "places.displayName", "places.formattedAddress", "places.servesCoffee"]

#request's headers 
nearbyHeaders = {
    "Content-Type": "application/json",
    "X-Goog-Api-Key": APIKEY,
    "X-Goog-FieldMask": ",".join(nearbyFields)
}

print(", ".join(nearbyFields))

""" nearbyHeadersStr = "{"
for key in nearbyHeaders.keys():
    nearbyHeadersStr += f"\"{key}\" : \"{nearbyHeaders[key]}\", "
nearbyHeadersStr += "}"
 """

# A get request to the API
response = requests.post(nearbyURL, json=nearbyParams, headers=nearbyHeaders)

# Print the response
response_json = response.json()

import json
locationIndex = "test"
with open(f"./docs/{locationIndex}_location.json", "w") as outfile:
    json.dump(response_json, outfile)



""" 
for index, point in enumerate(centerPoints):
    blablabla = 0        
 """


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


# https://places.googleapis.com/v1/places:searchNearby?

""" # The API endpoint
url = "https://jsonplaceholder.typicode.com/posts/"

# Adding a payload
payload = {"id": [1, 2, 3], "userId":1}

# A get request to the API
response = requests.get(url, params=payload)

# Print the response
response_json = response.json() """


""" HEADRES REFS


headers = {
    "projectName": "zhikovapp",
    "Authorization": "Bearer HZCdsf="
}
response = requests.get(bl_url, headers=headers) """



""" 
-H 'Content-Type: application/json' -H "X-Goog-Api-Key: API_KEY" \
-H "X-Goog-FieldMask: places.displayName"  """