import time
import mysql.connector
import sklearn
import pandas as pd
from pandas import DataFrame
from sklearn.cluster import KMeans
import pickle
import mysql.connector as connection
from sqlalchemy import create_engine

pd.set_option('future.no_silent_downcasting', True)

def get_users_dataframe():

    engine = create_engine("mysql+mysqlconnector://sample:sample@localhost:33060/coffee-mate")

    try:
        query = "Select userId, age, postcode, gender from usersTable order by userId ASC"
        users_df = pd.read_sql(query,engine)
        
        query = "Select DISTINCT questionId from responses order by questionId ASC"
        questionId_df = pd.read_sql(query,engine)
        for questionId in questionId_df['questionId']:
            query = f"Select userId, questionValue as questionValue{questionId} from responses where questionId = {questionId}"
            questionId_dataFrame = pd.read_sql(query,engine, index_col='userId')
            users_df = pd.merge(users_df, questionId_dataFrame, on='userId')

        query = "Select DISTINCT postcode from usersTable order by postcode ASC"
        postcodes = pd.read_sql(query,engine)
        postcodes_map = { postcode[0]:postcode[1] for postcode in postcodes.itertuples()}
        users_df['postcode']= users_df['postcode'].map(postcodes_map)

        users_df = users_df.fillna(0)
        types_dictionaty = { column:int for column in users_df.loc[:, users_df.columns != 'userId'].columns.values.tolist() }
        users_df = users_df.astype(types_dictionaty)
        
        #print(users_df)
        return users_df
    except Exception as err:
        
        return str(err)

def get_group_rankings_dataframe():
    
    engine = create_engine("mysql+mysqlconnector://sample:sample@localhost:33060/coffee-mate")

    try:
        query = "Select userId, cafeId, rankingValue from rankings where rankingValue = 5"
        rankings_dataFrame = pd.read_sql(query,engine)
        
        pivoted_dataframe = rankings_dataFrame.pivot(index='userId', columns = 'cafeId', values='rankingValue')
        
        print(pivoted_dataframe)
    except Exception as e:
        print(str(e))


#get_group_labels()
users_df = get_users_dataframe()
print(users_df)
kmeans = KMeans(n_clusters=3, random_state=0, n_init="auto").fit(users_df.loc[:, users_df.columns != 'userId'].values)
labels_df = DataFrame(kmeans.labels_, columns=['category'])
#lables_df = lables_df.transpose()
df_list = [users_df, labels_df]
users_df = pd.concat(df_list, axis=1)
#put 

try:
    engine = create_engine("mysql+mysqlconnector://sample:sample@localhost:33060/coffee-mate")
    users_df.to_sql()
    query = "Select userId, cafeId, rankingValue from rankings where rankingValue = 5"
    rankings_dataFrame = pd.to_sql(query,engine)

except Exception as err:


