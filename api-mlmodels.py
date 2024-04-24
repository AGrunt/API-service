import time
import mysql.connector
import sklearn
import pandas as pd
from pandas import DataFrame

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

def Get_usersTable_data(**kwargs):
    table = 'usersTable'
    table_columns = ['userId', 'gender', 'age', 'postcode']
    if kwargs.get('columns'):
        return table_columns
    columns_string = ''
    for index, column in enumerate(table_columns):
        if index < len(table_columns) - 1:
            columns_string += f'{column}, '
        else:
            columns_string += f'{column}'
    select_stmt = (
            f'SELECT {columns_string} FROM {table} '
            )
    cursor.execute(select_stmt)
    result = cursor.fetchall()
    return result

#example data_dict ={
    # 'tableName': 'somename',
    # 'tableColumns': [list_of_columns_name],
    # 'conditions': {'columnname': 'condition_value'}
    # }

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
    else:
        conditions_string = ''
    #print(f'conditions_string: {conditions_string}')
    #print(f'conditions_values: {conditions_values}')
    select_stmt = (
        f'SELECT {columns_string} FROM {table_name}' + conditions_string
            )
    #print(f'select_stmt: {select_stmt}')
    
    if kwargs.get('conditions'):
        cursor.execute(select_stmt, conditions_values)
        result = cursor.fetchall()
        return result 
    else:
        cursor.execute(select_stmt)
        result = cursor.fetchall()
        return result
    
    if kwargs.get('statement'):
        select_stmt = kwargs['statement']['statement']
        if 'values' in kwargs['statement'].keys():
            conditions_values = kwargs['statement']['values']
            cursor.execute(select_stmt, conditions_values)
        else:
            cursor.execute(select_stmt)
    result = cursor.fetchall()
        
    return result


# example of usage: 
# print(Get_data(tableName=table, tableColumns=table_columns, conditions = conditions_data))

# Make users dataframe
# Dataframe data params
table = 'usersTable'
table_columns = ['userId', 'gender', 'age', 'postcode']
conditions_data = {'userId': '273cf928-a41f-43c6-9dac-c13385b2a29e'}
df_users = DataFrame(Get_data(tableName=table, tableColumns=table_columns))
#df_users.columns = table_columns
print(df_users)

# Make responces dataframe

# Dataframe data params
table = 'responses'
table_columns = ['userId', 'questionId', 'questionValue', 'responseTimeStamp']
conditions_data = {'userId': '273cf928-a41f-43c6-9dac-c13385b2a29e'}

# Make a dataframe
df_responses = DataFrame(Get_data(tableName=table, tableColumns=table_columns))
#df_responses.columns = table_columns
print(df_responses)

stmt = {
    'statement': 'SELECT cafeId FROM cafes'
             }

df_cafes = DataFrame(Get_data(statement = stmt))
df_cafes.columns = ['cafeId']
print
#statement = {
#    'statement': 'SELECT * FROM cafes',
#    'values': ('value1', 'value2')
#             }


#statement = {
    # 'statement': 'statement_string', 
    # 'values': (values tuple)
    # }


#print(Get_usersTable_data()[0])
#columns = Get_usersTable_data(columns=True)
#df = DataFrame(Get_usersTable_data())
#df.columns = columns
#print(df.head(10))



    
    
    