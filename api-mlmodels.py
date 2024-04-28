import os
import time
from datetime import datetime
import mysql.connector
import sklearn
import pandas as pd
from pandas import DataFrame
from sklearn.cluster import KMeans
import pickle
import mysql.connector as connection
from sqlalchemy import create_engine
import tensorflow.compat.v1 as tf
import numpy as np

tf.compat.v1.disable_v2_behavior()


pd.set_option('future.no_silent_downcasting', True)
os.environ['LOKY_MAX_CPU_COUNT'] = '0' #exclude wornings

def create_table(table_name, columns, primary_key):

    try:
        dbConnection = mysql.connector.connect(
        host="localhost",
        port="33060",
        user="sample",
        password="sample",
        database="coffee-mate"
        )

        cursor = dbConnection.cursor()
        
        #UsersData
        #make string from columns
        stmt_string = 'CREATE TABLE %(table_name)s ('
        values_dict = {'table_name': table_name}
        for column in columns:
            stmt_string += f', %({column}) varchar(255) DEFAULT NULL'
            values_dict[column] = column
        stmt_string += ', PRIMARY KEY (%(primary_key)s) )'
        values_dict['primary_key'] = primary_key

        stmt = (stmt_string)

        cursor.execute(stmt, {'table_name': table_name})
        cursor.close()
        dbConnection.close()
        return True
    except Exception as err:
        cursor.close()
        dbConnection.close()
        return f'Error: {err}'

def drop_table(table_name):

    try:
        dbConnection = mysql.connector.connect(
        host="localhost",
        port="33060",
        user="sample",
        password="sample",
        database="coffee-mate"
        )

        cursor = dbConnection.cursor()

        stmt = ('DROP TABLE IF EXISTS %(table_name)s')
        cursor.execute(stmt, {'table_name': table_name})
        cursor.close()
        dbConnection.close()
        return True
    except Exception as err:
        cursor.close()
        dbConnection.close()
        return f'Error: {err}'

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

def get_cluster_rankings_dataframe():

    engine = create_engine("mysql+mysqlconnector://sample:sample@localhost:33060/coffee-mate")

    try:
        query  = "Select distinct tbl2.cafeId as cafeId, ud.cluster as cluster, avg(tbl2.rankingValue) over ( partition by cluster, cafeid) as ranking from ("
        query += "Select tbl.userId, tbl.cafeId, tbl.rankingValue "
        query += "from (SELECT *, row_number() OVER (PARTITION BY userId, cafeId ORDER BY STR_TO_DATE(rankingTimeStamp, '%Y-%m-%d %H:%i:%s.%f') DESC) r FROM rankings WHERE categoryId = 1) tbl "
        query += "WHERE r = 1 ORDER BY userId ) tbl2 left join usersData ud on tbl2.userId = ud.userId"
        rankings_df = pd.read_sql(query,engine)
        
        pivoted_rankings_df = rankings_df.pivot(index='cafeId', columns = 'cluster', values='ranking').fillna(0)
        return pivoted_rankings_df.T
    except Exception as e:
        print(str(e))

def get_user_rankings_dataframe():

    engine = create_engine("mysql+mysqlconnector://sample:sample@localhost:33060/coffee-mate")

    try:
        query = "Select tbl.userId as userId, tbl.cafeId as cafeId, tbl.rankingValue as ranking "
        query += "from (SELECT *, row_number() OVER (PARTITION BY userId, cafeId ORDER BY STR_TO_DATE(rankingTimeStamp, '%Y-%m-%d %H:%i:%s.%f') DESC) r FROM rankings WHERE categoryId = 1) tbl "
        query += "WHERE r = 1 ORDER BY userId"
        rankings_df = pd.read_sql(query,engine)
        pivoted_rankings_df = rankings_df.pivot(index='cafeId', columns = 'userId', values='ranking')
        return pivoted_rankings_df.T
    except Exception as e:
        print(str(e))

#KMEANS =================================================================================================

df = get_users_dataframe()
kmeans = KMeans(n_clusters=3, random_state=0, n_init="auto").fit(get_users_dataframe().values)
#print(kmeans.labels_)
df.loc[:,"cluster"] = kmeans.labels_

pickle.dump(kmeans, open(f'.\\models\\kmeans2.pkl','wb'))

#print(df)

engine = create_engine("mysql+mysqlconnector://sample:sample@localhost:33060/coffee-mate")

df.reset_index().to_sql('usersData', engine, if_exists='replace', index=False)

#Matrices
cluster_rankings_dataframe = get_cluster_rankings_dataframe()
cluster_cafe_matrix = cluster_rankings_dataframe.copy()
users_cafe_matrix = get_user_rankings_dataframe()

print(f'cluster_cafe_matrix: {cluster_cafe_matrix}')


# MODELING
# make a model on:
# cluster_matrix



users = cluster_cafe_matrix.index.tolist()
cafes = cluster_cafe_matrix.columns.tolist()
cluster_cafe_matrix = cluster_cafe_matrix.to_numpy()

#directly from manual

num_input = len(cafes)
num_hidden_1 = 10
num_hidden_2 = 5

X = tf.compat.v1.placeholder(tf.float64, [None, num_input])

weights = {
    'encoder_h1': tf.Variable(tf.random_normal([num_input, num_hidden_1], dtype=tf.float64)),
    'encoder_h2': tf.Variable(tf.random_normal([num_hidden_1, num_hidden_2], dtype=tf.float64)),
    'decoder_h1': tf.Variable(tf.random_normal([num_hidden_2, num_hidden_1], dtype=tf.float64)),
    'decoder_h2': tf.Variable(tf.random_normal([num_hidden_1, num_input], dtype=tf.float64)),
}

biases = {
    'encoder_b1': tf.Variable(tf.random_normal([num_hidden_1], dtype=tf.float64)),
    'encoder_b2': tf.Variable(tf.random_normal([num_hidden_2], dtype=tf.float64)),
    'decoder_b1': tf.Variable(tf.random_normal([num_hidden_1], dtype=tf.float64)),
    'decoder_b2': tf.Variable(tf.random_normal([num_input], dtype=tf.float64)),
}


def encoder(x):
    layer_1 = tf.nn.sigmoid(tf.add(tf.matmul(x, weights['encoder_h1']), biases['encoder_b1']))
    layer_2 = tf.nn.sigmoid(tf.add(tf.matmul(layer_1, weights['encoder_h2']), biases['encoder_b2']))
    return layer_2

def decoder(x):
    layer_1 = tf.nn.sigmoid(tf.add(tf.matmul(x, weights['decoder_h1']), biases['decoder_b1']))
    layer_2 = tf.nn.sigmoid(tf.add(tf.matmul(layer_1, weights['decoder_h2']), biases['decoder_b2']))
    return layer_2


encoder_op = encoder(X)
decoder_op = decoder(encoder_op)
y_pred = decoder_op
y_true = X

loss = tf.compat.v1.losses.mean_squared_error(y_true, y_pred)
optimizer = tf.compat.v1.train.RMSPropOptimizer(0.03).minimize(loss)
eval_x = tf.placeholder(tf.int32, )
eval_y = tf.placeholder(tf.int32, )
pre, pre_op = tf.compat.v1.metrics.precision(labels=eval_x, predictions=eval_y)

init = tf.global_variables_initializer()
local_init = tf.local_variables_initializer()
pred_data = pd.DataFrame()

# training

with tf.Session() as session:
    epochs = 100
    batch_size = 35

    session.run(init)
    session.run(local_init)

    print(f'cluster_cafe_matrix.shape[0]: {cluster_cafe_matrix.shape[0]}')

    #just 3 users now
    num_batches = int(cluster_cafe_matrix.shape[0] / batch_size)
    if num_batches < 1:
        num_batches = 1
    cluster_cafe_matrix = np.array_split(cluster_cafe_matrix, num_batches)
    
    for i in range(epochs):

        avg_cost = 0
        for batch in cluster_cafe_matrix:
            _, l = session.run([optimizer, loss], feed_dict={X: batch})
            avg_cost += l

        avg_cost /= num_batches

        #print("epoch: {} Loss: {}".format(i + 1, avg_cost))

    cluster_cafe_matrix = np.concatenate(cluster_cafe_matrix, axis=0)

    preds = session.run(decoder_op, feed_dict={X: cluster_cafe_matrix})

    pred_data = pred_data._append(pd.DataFrame(preds))
    #print(f'pred_data: {pred_data}')

    pred_data = pred_data.stack().reset_index(name='userId')
    pred_data.columns = ['userId', 'cafeId', 'rankingValue']
    print(f'pred_data: {pred_data}')
    pred_data['userId'] = pred_data['userId'].map(lambda value: users[value])
    pred_data['cafeId'] = pred_data['cafeId'].map(lambda value: cafes[value])
    
    keys = ['userId', 'cafeId']
    index_1 = pred_data.set_index(keys).index
    index_2 = cluster_rankings_dataframe.set_index(keys).index

    top_ten_ranked = pred_data[~index_1.isin(index_2)]
    top_ten_ranked = top_ten_ranked.sort_values(['userId', 'rankingValue'], ascending=[True, False])
    top_ten_ranked = top_ten_ranked.groupby('userId').head(10)






#print(df)
#=========================


#drop_table(UsersData)
#print(df.index.name)

#df.to_sql('usersData', engine, if_exists='replace', index=False)

#dd['cluster'].to_sql(name='usersTable', con=engine.connect() ,chunksize=100, if_exists='replace', dtype='int',)

#print(users_df)
#
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



#****** NOTES ********

#SQL statenments:
#1. how to get latest cafe rankings with user's cluster
""" 
Select tbl2.userId, tbl2.cafeId, tbl2.rankingValue, ud.cluster 
from (
Select tbl.userId, tbl.cafeId, tbl.rankingValue
from (SELECT *, row_number() OVER (PARTITION BY userId, cafeId ORDER BY STR_TO_DATE(rankingTimeStamp, '%Y-%m-%d %H:%i:%s.%f') DESC) r FROM rankings WHERE categoryId = 1) tbl 
WHERE r = 1 ORDER BY userId
) tbl2 left join usersData ud on tbl2.userId = ud.userId;
 """

#2. how to get combined data from latest cafe rankings with user's cluster grouped with average in rankingvalue
""" 
Select distinct tbl2.cafeId,  ud.cluster, avg(tbl2.rankingValue) over ( partition by cluster, cafeid) 
from (
Select tbl.userId, tbl.cafeId, tbl.rankingValue
from (SELECT *, row_number() OVER (PARTITION BY userId, cafeId ORDER BY STR_TO_DATE(rankingTimeStamp, '%Y-%m-%d %H:%i:%s.%f') DESC) r FROM rankings WHERE categoryId = 1) tbl 
WHERE r = 1 ORDER BY userId
) tbl2 left join usersData ud on tbl2.userId = ud.userId;
 """

