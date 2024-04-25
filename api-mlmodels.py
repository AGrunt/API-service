import time
import mysql.connector
import sklearn
import pandas as pd
from pandas import DataFrame
from sklearn.cluster import KMeans
import pickle

while True:
    try:
        #Creating db connector
        dbConnection = mysql.connector.connect(
            host="localhost",
            port="33060",
            user="sample",
            password="sample",
            database="coffee-mate"
            )

        # Make a cursor
        cursor = dbConnection.cursor()
        #print(f'Mysql woke up. Now Mysql service status is <CONNECTED>')
        break
    except Exception as err:
        print(f'Something wrong with Mysql service: <{err}>. It is slow. Let`s just wait for 5 seconds')
        time.sleep(5)

def put_data(**kwargs):
# Expected that data is a dictionarry. With {columnName:value} format
    if kwargs.get('tableName'):
        table_name = kwargs.get('tableName')
        #print(table_name)

    if kwargs.get('data'):
        columns_string = ''
        values_string = ''
        values = ()
        for index, column in enumerate(data.keys()):
            if index < len(data.keys()) - 1:
                columns_string += f'{column}, '
                values_string +=  f'%s, '
            else:
                columns_string += f'{column}'
                values_string +=  f'%s'
            values += tuple([data[column]])

    if kwargs.get('conditions'):
        conditions = kwargs.get('conditions')
        condition_type = conditions.get['conditionType']
        #makle a conditions string for statement
        # 'conditions': {'columnname': 'condition_value'}
        # 'conditionType': 'AND' / 'OR'
        conditions_string = ' WHERE '
        conditions_values = ()
        for index, key in enumerate(conditions.keys()):
            column = key
            value = conditions[key]
            if index < len(conditions.keys()) - 1:
                conditions_string += f'{column} = %s {condition_type}'
            else:
                conditions_string += f'{column} = %s'
            conditions_values += tuple([value])         
        values += conditions_values
    
    #make statement
    insert_stmt = (
        f'INSERT INTO {table} ({columns_string}) '
        f'VALUES ({values_string})' + conditions_string
        )
    
    try:
        cursor.execute(insert_stmt, values)
        dbConnection.commit()
    except Exception as err:
        return False, table, err
    return True

""" 

# Make insert stetement
insert_stmt = (
f'INSERT INTO {table_name} ({columns_string}) '
f'VALUES ({values_string})'
)
cursor.execute(insert_stmt, values)
dbConnection.commit()
except Exception as err:
return False, table, err, 500
return True

 """
        

#universal get data function
def Get_data(**kwargs):
    if kwargs.get('tableName'):
        table_name = kwargs.get('tableName')
        #print(table_name)
    if kwargs.get('tableColumns'):
        table_columns = kwargs.get('tableColumns')
        #print(table_columns)
        #makle a columns string for statement
        columns_string = ''
        for index, column in enumerate(table_columns):
            if index < len(table_columns) - 1:
                columns_string += f'{column}, '
            else:
                columns_string += f'{column}'
        
    if kwargs.get('conditions'):
        conditions = kwargs.get('conditions')
        #makle a conditions string for statement
        # 'conditions': {'columnname': 'condition_value'}
        conditions_string = ' WHERE '
        conditions_values = ()
        for index, key in enumerate(conditions.keys()):
            column = key
            value = conditions[key]
            if index < len(conditions.keys()) - 1:
                conditions_string += f'{column} = %s AND '
            else:
                conditions_string += f'{column} = %s'
            conditions_values += tuple([value])
        select_stmt = (
        f'SELECT {columns_string} FROM {table_name}' + conditions_string
            )
        cursor.execute(select_stmt, conditions_values)
        result = cursor.fetchall()
        return result

    # just execute precompiled SQL statement. Not safe. will redo as i have enough time  
    if kwargs.get('statement'):
        select_stmt = kwargs['statement']
        cursor.execute(select_stmt)
        result = cursor.fetchall()
        return result
    
    select_stmt = (
        f'SELECT {columns_string} FROM {table_name}'
            )
    cursor.execute(select_stmt)
    result = cursor.fetchall()
    return result
    # Example of usage: Get_data(tableName=table, tableColumns=table_columns, conditions = conditions_data)

def users_group_model(**kwargs):
    # Making list of question ids
    table = 'responses'
    table_columns = ['distinct questionId']
    questionCategories = Get_data(tableName = table, tableColumns = table_columns)

    # Start making users dataframe for kmeans
    stmt = 'select userId, gender, age, postcode from usersTable order by userId DESC'
    users_df = DataFrame(Get_data(statement=stmt), columns = ['userId', 'gender', 'age', 'postcode'])

    # Combining question datasets with users dataset
    convert_dictionary = {'age': int,
                        'gender': int,
                        'postcode': int}
    for category in questionCategories:
        stmt = f'select questionValue from responses where questionId = "{category[0]}" order by userId DESC'
        category_df = DataFrame(Get_data(statement=stmt), columns = [f'questionId{category[0]}'])
        users_df = pd.concat([users_df, category_df], axis=1)
        convert_dictionary[f'questionId{category[0]}'] = int
        
    # Replace postcodes with its category index
    
    # Getting postcodes from database
    stmt = 'select distinct postcode from usersTable order by postcode ASC'
    postcodes = Get_data(statement=stmt)
    replacements = {} # create a dictionary for 'postcode' categorical values replacement
    for index, postcode in enumerate(postcodes):
        replacements[f'{postcode[0]}'] = index
    users_df['postcode'] = users_df['postcode'].map(replacements) # replace 'postcode' values
    users_df = users_df.fillna(0) # Convert NaN values to 0s
    users_df = users_df.astype(convert_dictionary) # Convert data types of dataframe columns
    if kwargs.get('df'):
        return users_df
    #applying kmeans to data
    kmeans = KMeans(n_clusters=3, random_state=0, n_init="auto").fit(users_df.loc[:, users_df.columns != 'userId' ].values)
    return kmeans
    
#Dump model to file function
def dump_model(model, filename):
    pickle.dump(model, open(f'.\\models\\{filename}.pkl','wb'))

#Make prediction for user's data
def get_users_group_prediction(userString):
    model = pickle.load(open('.\\models\\kmeans.pkl','rb'))
    return model.predict([userString])

#Get all users labels from model
def get_users_group_labels():
    model = pickle.load(open('.\\models\\kmeans.pkl','rb'))
    return model.labels_

#Make model, dump to file
dump_model(users_group_model(), 'kmeans')
#Get labels
print(get_users_group_labels())

#combine dataframes and write labels to database
#combine dataframes
df_combined = pd.concat(users_group_model(df=True), DataFrame(get_users_group_labels()))

print(df_combined)



print(df_labels)








#$ENV:LOKY_MAX_CPU_COUNT = 0
#NOTES: 
#stmt = 'select usersTable.userId, gender, age, postcode, questionId, questionValue 
# from usersTable 
# join responses ON usersTable.userId = responses.userId
# where questionId not like "test" order by usersTable.userId, responseTimeStamp, questionId DESC'