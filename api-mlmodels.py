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





def get_group_rankings_dataframe():
    
    engine = create_engine("mysql+mysqlconnector://sample:sample@localhost:33060/coffee-mate")

    try:
        query = "Select userId, cafeId, rankingValue from rankings where rankingValue = 5"
        rankings_dataFrame = pd.read_sql(query,engine)
        
        pivoted_dataframe = rankings_dataFrame.pivot(index='userId', columns = 'cafeId', values='rankingValue')
        
        print(pivoted_dataframe)
    except Exception as e:
        print(str(e))


#print(get_group_rankings_dataframe())


#get_group_labels()
#users_df = 

print(get_users_dataframe())
print(get_users_dataframe()['postcodeId'].unique())

#print(users_df)
#kmeans = KMeans(n_clusters=3, random_state=0, n_init="auto").fit(get_users_dataframe().values)
#labels_df = DataFrame(kmeans.labels_, columns=['category'])
#lables_df = lables_df.transpose()
#df_list = [users_df, labels_df]
#users_df = pd.concat(df_list, axis=1)
#put 

""" try:
    engine = create_engine("mysql+mysqlconnector://sample:sample@localhost:33060/coffee-mate")

    #trainee.to_sql('trainee2', engine, if_exists='replace', index=False)


    users_df.to_sql()
    query = "Select userId, cafeId, rankingValue from rankings where rankingValue = 5"
    rankings_dataFrame = pd.to_sql(query,engine)

except Exception as err:
    print(err) """