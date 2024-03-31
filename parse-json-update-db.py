import os
import json
#import mysql.connector
import csv

#make csv for cafes write header
cafes_file = "./output/cafes.csv"
columns = ['fileN', 'file', 'id', 'displayName', 'formattedAddress', 'latitude', 'longitude', 'servesCoffee', 'takeout', 'goodForChildren', 'goodForGroups']
header = ""
for index, column in enumerate(columns):
    if index < len(columns) - 1:
        header += f"{column}, "
    else:
        header += f"{column}\n"

with open(cafes_file, "a") as file:
    file.write(header)

#make csv for reviews write header
review_file = "./output/reviews.csv"
columns = ['fileN', 'file', 'id', 'rating', 'userFirstName', 'userSecondName']
header = ""
for index, column in enumerate(columns):
    if index < len(columns) - 1:
        header += f"{column}, "
    else:
        header += f"{column}\n"

with open(review_file, "a") as file:
    file.write(header)


# Creating db connector
#mydb = mysql.connector.connect(
#  host="api-db",
#  port="3306",
#  user="sample",
#  password="sample"
#)

# Make a cursor
#cursor = mydb.cursor()


# Get the list of all files and directories
path = "./output/"
dir_list = os.listdir(path)

# prints all files
#print(dir_list)
files = 0
for fileJSON in dir_list:
    files += 1
    # Opening JSON file
    f = open(f'{path}{fileJSON}')
    
    # returns JSON object as a dictionary
    data = dict(json.load(f))

    if 'places' not in data.keys():
        f.close()
        continue
    # get places one by one
    for place in data['places']:
        place.setdefault('servesCoffee', 'false')
        place.setdefault('takeout', 'false')
        place.setdefault('goodForChildren', 'false')
        place.setdefault('goodForGroups', 'false')
        place.setdefault('delivery', 'false')

        placeCombined = {'id':  place['id'], 'displayName': place['displayName']['text'], 'formattedAddress': place['formattedAddress'], 'latitude': place['location']['latitude'], 'longitude': place['location']['longitude'], 'servesCoffee': place['servesCoffee'], 'takeout': place['takeout'], 'goodForChildren': place['goodForChildren'], 'goodForGroups': place['goodForGroups']}

        #print(placeCombined)
        placeCombvinedStr = f"{files}, {fileJSON}, {placeCombined['id']}, {placeCombined['displayName']}, {placeCombined['formattedAddress']}, {placeCombined['latitude']}, {placeCombined['longitude']}, {placeCombined['servesCoffee']}, {placeCombined['takeout']}, {placeCombined['goodForChildren']}, {placeCombined['goodForGroups']}\n"

        with open(cafes_file, "a") as file:
            file.write(placeCombvinedStr)
        file.close()

        # Gather reviews
        if 'reviews' not in place.keys():
            f.close()
            continue 

        for review in place['reviews']:        
            # Split displayed name 
            userName = review['authorAttribution']['displayName'].split(" ")
            if len(userName) == 1:
                userName.append("")

            reviewCombined = {'id': place['id'], 'rating': review['rating'], 'userFirstName': userName[0], 'userSecondName': userName[1]}
            #print(reviewCombined)

            reviewCombinedStr = f"{files}, {fileJSON}, {reviewCombined['id']}, {reviewCombined['rating']}, {reviewCombined['userFirstName']}, {reviewCombined['userSecondName']}\n"        

            with open(review_file, "a") as file:
                file.write(reviewCombinedStr)
            file.close()
    f.close()
    #NOW I NEED TO WRITE THESE DATA TO DB
    # 1. make tables in db
    # 2. import mysql.connector
    # 3. insert data by fields. 



#export to csv




# REFERENCE
# Requested fields
#nearbyFields = ["places.id", "places.location", "places.displayName", "places.formattedAddress", "places.servesCoffee", "places.takeout", "places.delivery", "places.goodForChildren", "places.goodForGroups", "places.reviews"]


""" TABLE
-- This table holds recomendations for each cafe for each user
CREATE TABLE jsonData(
jsonDataIndex int AUTO_INCREMENT,
cafeId varchar(255), --id
userName varchar(255), 
ranking int(1), --rating


predicitonValue DECIMAL(3, 2),
predictionTimeStamp varchar(255),
PRIMARY KEY (jsonDataIndex)
); """



# TODO
# 1. Make reviews table for obtained data
# Нет одинаковых пользователей
# каждый ревью сделан от уникального полдьзователя
# значит на каждый ревью надо создать пользователя. сделать ему id, угадать его пол по имени. разбить его полное имя на имя и фамилию.  
# 2. do something with cafes data 
""" Заполнить по cafeId
Название
Полный Адресс
takeout
delivery
servesCoffee
goodForChildren
goodForGroups
latitude
longitude

Make a table for cafe:
cafeId
latitude
longitude
displayName
formattedAddress
servesCoffee
takeout
delivery
goodForChildren
goodForGroups 

"""