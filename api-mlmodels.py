import time
import mysql.connector
import sklearn
import pandas as pd
from pandas import DataFrame
from sklearn.cluster import KMeans

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
        print(f'Mysql woke up. Now Mysql service status is <CONNECTED>')
        break
    except Exception as err:
        print(f'Something wrong with Mysql service: <{err}>. It is slow. Let`s just wait for 5 seconds')
        time.sleep(5)

#universal get data function
def Get_data(**kwargs):
    #if (not kwargs.get('tableName') or not kwargs.get('tableColumns')) and not kwargs.get('conditions'):
    #    return f'One of the required args is empty. Check tableName and tableColumns arguments'

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


# example of usage: 
# print(Get_data(tableName=table, tableColumns=table_columns, conditions = conditions_data))

# Making list of question ids
table = 'responses'
table_columns = ['distinct questionId']
questionCategories = Get_data(tableName = table, tableColumns = table_columns)
stmt = 'select userId, gender, age, postcode from usersTable order by userId DESC'
users_df = DataFrame(Get_data(statement=stmt), columns = ['userId', 'gender', 'age', 'postcode'])

# Combining question datasets with users dataset
convert_dictionary = {'age': int,
                      'gender': int}
for category in questionCategories:
    stmt = f'select questionValue from responses where questionId = "{category[0]}" order by userId DESC'
    category_df = DataFrame(Get_data(statement=stmt), columns = [f'questionId{category[0]}'])
    users_df = pd.concat([users_df, category_df], axis=1)
    convert_dictionary[f'questionId{category[0]}'] = int
    
#Convert NaN values to 0s
users_df = users_df.fillna(0)
#Convert data types of dataframe columns
users_df = users_df.astype(convert_dictionary)
print(users_df)
#print(users_df.dtypes)

#apply kmeans


kmeans = KMeans(n_clusters=3, random_state=0, n_init="auto").fit(users_df.loc[:, users_df.columns != 'userId' ])
#kmeans.labels_


#write lables to db


print(kmeans.labels_)



#NOTES: 
#stmt = 'select usersTable.userId, gender, age, postcode, questionId, questionValue 
# from usersTable 
# join responses ON usersTable.userId = responses.userId
# where questionId not like "test" order by usersTable.userId, responseTimeStamp, questionId DESC'