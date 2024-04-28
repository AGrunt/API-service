import pickle
from sklearn.cluster import KMeans
from sqlalchemy import create_engine
import pandas as pd
import os
import mysql.connector
import sys


pd.set_option('future.no_silent_downcasting', True)
os.environ['LOKY_MAX_CPU_COUNT'] = '0' #exclude wornings

kmeans_model = pickle.load(open('./models/kmeans.pkl', 'rb'))

def get_users():

    engine = create_engine("mysql+mysqlconnector://sample:sample@localhost:33060/coffee-mate")

    try:
        query = "Select userId, age, postcode, gender from usersTable order by userId ASC"
        users_df = pd.read_sql(query,engine, index_col='userId').fillna(0)
        postcodes = users_df['postcode'].unique()
        postcodes_map = { postcode:index for index, postcode in enumerate(postcodes)}
        users_df['postcodeId'] = users_df['postcode'].map(postcodes_map)
        
        #get just last question by timestamp
        query = "Select tbl.userId, tbl.questionId, tbl.questionValue from (SELECT *, row_number() OVER (PARTITION BY userId, questionId ORDER BY STR_TO_DATE(responseTimeStamp, '%Y-%m-%d %H:%i:%s.%f') DESC) r FROM responses) tbl where r = 1 ORDER BY userId"
        questions_df = pd.read_sql(query,engine).fillna(0)
        
        pivoted_questions_df = questions_df.pivot(index = 'userId' , columns = 'questionId', values='questionValue')
        users_df = users_df.join(pivoted_questions_df).fillna(0)

        #change dtype of selected columns
        columns_names = users_df.loc[:, users_df.columns != 'postcode'].columns.values.tolist()
        types = { str(column): 'int32' for column in columns_names}
        users_df = users_df[columns_names].astype(types)
        return users_df
    except Exception as err:
        return print(str(err))


users_df = get_users()

result = kmeans_model.predict(users_df)

users_df['cluster'] = result


dbConnection = mysql.connector.connect(
        host="localhost",
        port="33060",
        user="sample",
        password="sample",
        database="coffee-mate"
        )

cursor = dbConnection.cursor()

for index, user in users_df.iterrows():
    try:
        print(f'User Clustrer updating. user: {index}. cluster: {user["cluster"]} ')
        update_stmt = ('UPDATE usersTable SET category = %(category)s WHERE userId = %(userId)s')
        cursor.execute(update_stmt, {'userId': index, 'category': int(user['cluster'])})
    except Exception as err:
        dbConnection.rollback()
        cursor.close()
        dbConnection.close()
        sys.exit(f'Database error: {err}')

dbConnection.commit()
cursor.close()
dbConnection.close()