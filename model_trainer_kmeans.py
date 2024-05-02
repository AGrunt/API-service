import os
import pandas as pd
from sklearn.cluster import KMeans
import pickle
from sqlalchemy import create_engine

pd.set_option('future.no_silent_downcasting', True)
os.environ['LOKY_MAX_CPU_COUNT'] = '0' #exclude warnings

def get_users_dataframe():

    engine = create_engine("mysql+mysqlconnector://sample:sample@api-db:3306/coffee-mate")

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

def train_kmeans_model():
    
    print('Starting kmeans model training...')
    
    kmeans = KMeans(n_clusters=3, random_state=0, n_init="auto").fit(get_users_dataframe().values)

    pickle.dump(kmeans, open(f'./models/kmeans.pkl','wb'))
    
    print('Kmeans model training complete.')