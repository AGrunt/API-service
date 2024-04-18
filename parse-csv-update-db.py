import os
import pandas as pd
import mysql.connector


def open_csv(file):
    data = pd.open_csv

#Creating db connector
mydb = mysql.connector.connect(
  host="api-db",
  port="3306",
  user="sample",
  password="sample")

# Make a cursor
cursor = mydb.cursor()

cursor.execute("show databases")

for x in cursor:
    print(x) 

  #NOW I NEED TO WRITE THESE DATA TO DB
    # 1. make tables in db
    # 2. import mysql.connector
    # 3. insert data by fields. 
    # 4. figurout how to generate user id. It must be GUID
    #examples:

"""
    >>> import uuid

    >>> # make a random UUID
    >>> uuid.uuid4()
    UUID('bd65600d-8669-4903-8a14-af88203add38')

    >>> # Convert a UUID to a string of hex digits in standard form
    >>> str(uuid.uuid4())
    'f50ec0b7-f960-400d-91f0-c42a6d44e3d0'

    >>> # Convert a UUID to a 32-character hexadecimal string
    >>> uuid.uuid4().hex
    '9fe2c4e93f654fdbb24c02b15259716c'
"""

# TODO
# 1. Make reviews table for obtained data
# Нет одинаковых пользователей
# каждый ревью сделан от уникального полдьзователя
# значит на каждый ревью надо создать пользователя. сделать ему id, угадать его пол по имени. разбить его полное имя на имя и фамилию.  
# 2. do something with cafes data 
""" 
Заполнить по cafeId
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