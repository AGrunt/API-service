import os
import pandas as pd
import uuid

# file maker function
def csv_maker(filename, columns):
    file = f"./docs/generated/{filename}.csv"
    header = ""
    for index, column in enumerate(columns):
        if index < len(columns) - 1:
            header += f"{column}|"
        else:
            header += f"{column}\n"
    with open(file, "a") as file:
        file.write(header)   
    return True

#load csv with probabilities of gender regarding person name sorted by ASC
df_genders_names = pd.read_csv('./docs/name_gender_dataset.csv')

#create csv files for venues and reviews
csv_files = [
    {'filename': 'cafes', 'columns': ['fileN', 'fileName', 'cafeId', 'displayName', 'formattedAddress', 'latitude', 'longitude', 'servesCoffee', 'takeout', 'goodForChildren','delivery', 'goodForGroups']},
    {'filename': 'reviews', 'columns': ['fileN', 'fileName', 'userId', 'cafeId', 'rating', 'userFirstName', 'userSecondName', 'gender']}]
for file in csv_files:
    csv_maker(file['filename'], file['columns'])

# Get the list of all files and directories
def get_files(path):
    return os.listdir(path)

# load json file to dataframe
def load_json(path, fileJSON):
    data = pd.read_json(f'{path}{fileJSON}')
    if 'places' not in data:
        return None
    return data

# extract cafelist from dataframe
def cafes_list(data, fileIndex, fileJSON):
    places = []
    if data is None:
        return None
    for index, place in data.iterrows():
        placeCombined = {'fileN': fileIndex,
                         'fileName': fileJSON,
                         'cafeId':  place['places']['id'],
                         'displayName': place['places']['displayName']['text'],
                         'formattedAddress': place['places']['formattedAddress'],
                         'latitude': place['places']['location']['latitude'],
                         'longitude': place['places']['location']['longitude'],
                         'servesCoffee': f"{place['places']['servesCoffee'] if 'servesCoffee' in place['places'] else 'false'}",
                         'takeout': f"{place['places']['takeout'] if 'takeout' in place else 'false'}",
                         'goodForChildren': f"{place['places']['goodForChildren'] if 'goodForChildren' in place['places'] else 'false'}",
                         'delivery': f"{place['places']['delivery'] if 'delivery' in place['places'] else 'false'}",
                         'goodForGroups': f"{place['places']['goodForGroups'] if 'goodForGroups' in place['places'] else 'false'}"} 
        places.append(placeCombined)
    return places

# extract reviews from dataframe
def reviews_list(data, fileIndex, fileJSON):
    reviews = []
    if data is None:
        return None
    for index, place in data.iterrows():
        if 'reviews' in place['places']:
            for review in place['places']['reviews']:
                userName = review['authorAttribution']['displayName'].split(" ")
                if len(userName) == 1:
                    userName.append("")
                genders_list = df_genders_names.loc[df_genders_names['Name'] == userName[0], 'Gender'].tolist()
                if len(genders_list) > 0:
                    gender = genders_list[0]
                else:
                    gender = 'NA'
                reviewCombined = {'fileN': fileIndex,
                                'fileName': fileJSON,
                                'userId':  str(uuid.uuid4()),
                                'cafeId': place['places']['id'],
                                'rating': review['rating'],
                                'userFirstName': userName[0],
                                'userSecondName': userName[1],
                                'gender': gender}
                reviews.append(reviewCombined)
        else:
            continue 
    return reviews

# write output to file
def file_write(path, file, data):
    if data is None:
        return None
    with open(f'{path}{file}.csv', 'a') as file:
        for value in data:
            for index, key in enumerate(value.keys()):
                string = ''
                if index < len(value.keys()) - 1:
                    string += f"{value[key]}|"
                else:
                    string += f"{value[key]}\n"
                file.write(string)
    file.close()
    return True

# Creation of cafelist and reviews
path = './output/'
for index, fileJSON in enumerate(get_files(path)):
    file_write('./docs/generated/', 'cafes', cafes_list(load_json(path, fileJSON), index, fileJSON))
    file_write('./docs/generated/', 'reviews', reviews_list(load_json(path, fileJSON), index, fileJSON))