import json
import requests

#START SCRAPING NOW

#Надо написать закпрос на получение кафе

# Params initialisation       
# Key for API
APIKEY = "AIzaSyDjo40rexGJZbQYLzMrPLuzgZ4Li62n_1s"


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

#requested fields
#Available fields
#places.accessibilityOptions, places.addressComponents, places.adrFormatAddress, places.businessStatus, places.displayName, places.formattedAddress, places.googleMapsUri, places.iconBackgroundColor, places.iconMaskBaseUri, places.id, places.location, places.name*, places.photos, places.plusCode, places.primaryType, places.primaryTypeDisplayName, places.shortFormattedAddress, places.subDestinations, places.types, places.utcOffsetMinutes, places.viewport
#places.currentOpeningHours, places.currentSecondaryOpeningHours, places.internationalPhoneNumber, places.nationalPhoneNumber, places.priceLevel, places.rating, places.regularOpeningHours, places.regularSecondaryOpeningHours, places.userRatingCount, places.websiteUri
#places.allowsDogs, places.curbsidePickup, places.delivery, places.dineIn, places.editorialSummary, places.evChargeOptions, places.fuelOptions, places.goodForChildren, places.goodForGroups, places.goodForWatchingSports, places.liveMusic, places.menuForChildren, places.parkingOptions, places.paymentOptions, places.outdoorSeating, places.reservable, places.restroom, places.reviews, places.servesBeer, places.servesBreakfast, places.servesBrunch, places.servesCocktails, places.servesCoffee, places.servesDesserts, places.servesDinner, places.servesLunch, places.servesVegetarianFood, places.servesWine, places.takeout 

nearbyFields = ["places.id", "places.location", "places.displayName", "places.formattedAddress", "places.servesCoffee", "places.takeout", "places.delivery", "places.goodForChildren", "places.goodForGroups", "places.reviews"]

#request's headers 
nearbyHeaders = {
    "Content-Type": "application/json",
    "X-Goog-Api-Key": APIKEY,
    "X-Goog-FieldMask": ",".join(nearbyFields)
}

# A get request to the API
response = requests.post(nearbyURL, json=nearbyParams, headers=nearbyHeaders)

# Print the response
response_json = response.json()

locationIndex = "test"
with open(f"./output/{locationIndex}_location.json", "w") as outfile:
    json.dump(response_json, outfile)

# Check google license for map api. How i can use data from API.