import pandas as pd
import mysql.connector
from datetime import datetime

#Creating db connector
mydb = mysql.connector.connect(host="localhost", port="33060", user="sample", password="sample",database="coffee-mate")

# Make a cursor
cursor = mydb.cursor()

# load csv to dataframe
def load_csv(path, file):
  data = pd.read_csv(f'{path}{file}.csv', delimiter= '|')
  return data

#gender user's param transform to int
def transform_gender(gender_string):
  match gender_string:
    case 'NA':
      return 0
    case 'F':
      return 1  
    case 'M':
      return 2

#is primary key value already in a database?
def check_primary_key(table_name, primary_key):
  #check if key value or values already in the database
  key_value_tuple = ()
  conditions_string = ''
  for index, key in enumerate(primary_key):
    if index < len(primary_key) - 1:
      conditions_string += f'{key} = %s AND '
    else:
      conditions_string += f'{key} = %s'
    key_value_tuple += tuple([primary_key[key]])
  select_stmt = (
  f'SELECT COUNT(*) FROM {table_name} ' 
  f'WHERE {conditions_string}'
  )
  cursor.execute(select_stmt, key_value_tuple)
  myresult = cursor.fetchone()  
  if int(myresult[0]) > 0:
    return True
  return False

#function of database data existence and data insertion  
def insert_data(table_name, primary_key, data):
  if check_primary_key(table_name, primary_key):
    print('Primary key already exists.')
    return
      
  #make a string with table columns, string with values placeholders, and a tuple with keys values.
  columns_string = ''
  values_string = ''
  key_value_tuple = ()
  for index, key in enumerate(data.keys()):
    if index < len(data.keys()) - 1 :
      columns_string += f'{key}, '
      values_string += f'%s, '
    else:
      columns_string += f'{key}'
      values_string += f'%s'
    key_value_tuple += tuple([data[key]])

  #make insert statement string
  insert_stmt = (
  f'INSERT INTO {table_name} ({columns_string}) '
  f'VALUES ({values_string})'
  )
  cursor.execute(insert_stmt, key_value_tuple)
  return None

def process_users_table():
  row_counter = 0
  path = './docs/generated/'
  #inserting data and commit insertion every 200 rows
  for index, row in load_csv(path, 'reviews').iterrows():
    data = {
      'userId': row['userId'],
      'gender': transform_gender(row['gender']),
      'registrationTimeStamp': datetime.now()
    }
    primary_key = {
      'userId': row['userId']
      }
    print(f'primary_key:{primary_key}')
    insert_data('usersTable', primary_key, data)
    row_counter += 1
    if row_counter > 200:
      row_counter = 0
      mydb.commit()
  mydb.commit()

def process_responces_table():
  row_counter = 0
  path = './docs/generated/'
  questionValue = 0
  responseTimeStamp = '2024-04-19 20:33:21.744073'
  #inserting data and commit insertion every 200 rows
  for index, row in load_csv(path, 'reviews').iterrows():
    for questionId in range(1,8):
      data = {
        'userId': f'{row['userId']}',
        'responseTimeStamp': responseTimeStamp,
        'questionId': questionId,
        'questionValue': questionValue
      }
      primary_key = {
        'userId': f'{row['userId']}',
        'responseTimeStamp': responseTimeStamp,
        'questionId': questionId,
        'questionValue': questionValue
        }
      print(f'primary_key:{primary_key}')
      insert_data('responses', primary_key, data)
      row_counter += 1
    if row_counter > 200:
      row_counter = 0
      mydb.commit()
  mydb.commit()

def process_rankings_table():
  total = 0 
  row_counter = 0
  path = './docs/generated/'
  rankingTimeStamp = '2024-04-19 20:33:21.744073'
  #inserting data and commit insertion every 200 rows
  for index, row in load_csv(path, 'reviews').iterrows():
    data = {
      'userId': f'{row['userId']}',
      'cafeId': f'{row['cafeId']}',
      'categoryId': 1,
      'rankingValue': f'{row['rating']}',
      'rankingTimeStamp': rankingTimeStamp,
    }
    primary_key = {
      'userId': f'{row['userId']}',
      'cafeId': f'{row['cafeId']}',
      'categoryId': f'1',
      'rankingValue': row['rating'],
      'rankingTimeStamp': rankingTimeStamp,
      }
    print(f'primary_key:{primary_key}')
    insert_data('rankings', primary_key, data)
    row_counter += 1
    total += 1
    if row_counter > 200:
      row_counter = 0
      mydb.commit()
  mydb.commit()
  print(f'Total records: {total}')
  return

def process_cafes_table():
  total = 0 
  row_counter = 0
  path = './docs/generated/'
  #inserting data and commit insertion every 200 rows
  for index, row in load_csv(path, 'cafes').iterrows():
    data = {
      'cafeId': f'{row['cafeId']}',
      'displayName': f'{row['displayName']}',
      'formattedAddress': f'{row['formattedAddress']}',
      'latitude': f'{row['latitude']}',
      'longitude': f'{row['longitude']}',
      'servesCoffee': (f'{row['servesCoffee']}').upper(),
      'takeout': (f'{row['takeout']}').upper(),
      'goodForChildren': (f'{row['goodForChildren']}').upper(),
      'delivery': (f'{row['delivery']}').upper(),
      'goodForGroups': (f'{row['goodForGroups']}').upper()
    }
    primary_key = {
      'cafeId': f'{row['cafeId']}'
      }
    print(f'primary_key:{primary_key}')
    insert_data('cafes', primary_key, data)
    row_counter += 1
    total += 1
    if row_counter > 200:
      row_counter = 0
      mydb.commit()
  mydb.commit()
  print(f'Total records: {total}')
  return

start = datetime.now()
process_users_table()
process_responces_table()
process_rankings_table()
process_cafes_table()
print(f'Elapsed time: {datetime.now() - start}')





# TODO
# 1. Make reviews table for obtained data
# Нет одинаковых пользователей
# каждый ревью сделан от уникального полдьзователя
# значит на каждый ревью надо создать пользователя. сделать ему id, угадать его пол по имени. разбить его полное имя на имя и фамилию.  
# 2. do something with cafes data 

#NOW I NEED TO WRITE THESE DATA TO DB
# 1. make tables in db
# 2. import mysql.connector
# 3. insert data by fields. 
# 4. figurout how to generate user id. It must be GUID
#examples:

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