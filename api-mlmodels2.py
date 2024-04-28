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
import numpy as np
import tensorflow_recommenders as tfrs

import tensorflow as tf


pd.set_option('future.no_silent_downcasting', True)
os.environ['LOKY_MAX_CPU_COUNT'] = '0' #exclude wornings

#=========================================================================================================================================================================

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

#==========================================================================================================================================================================

def get_users_rankings_dataframe(): #dataframne with userId, age, postcode, gender, cafeId, ranking

    engine = create_engine("mysql+mysqlconnector://sample:sample@localhost:33060/coffee-mate")

    try:
        #select ранкингов с пользовательскии данными age, postcode, gender
        query  = 'Select tbl.cafeId, tbl.userId, tbl.rankingValue, ut.age, ut.postcode, ut.gender from '
        query += '(SELECT *, row_number() OVER (PARTITION BY userId, cafeId ORDER BY STR_TO_DATE(rankingTimeStamp, "%Y-%m-%d %H:%i:%s.%f") DESC) r FROM rankings WHERE categoryId = 1 ) tbl '
        query +=  'LEFT JOIN usersTable ut on ut.userId = tbl.userId '
        query +=  'WHERE r = 1 ORDER BY userId'

        rankings_df = pd.read_sql(query,engine).fillna(0)
        print(rankings_df)


        #select cafe features
        query  = 'select cafeId, servesCoffee, takeout, goodForChildren, goodForGroups, delivery from cafes'
        cafe_features_df = pd.read_sql(query,engine, index_col='cafeId').fillna(0)
        cafe_features_df = cafe_features_df.map(lambda x: f"{1 if x == 'TRUE' else 0}")
        cafe_features_df['features'] =  cafe_features_df.to_numpy().tolist()
        cafe_features_df = cafe_features_df.reset_index()
        rankings_df = pd.merge(rankings_df, cafe_features_df[['cafeId', 'features']], on='cafeId')

        #select and pivot users features
        query  = "Select tbl.userId, tbl.questionId, tbl.questionValue from (SELECT *, row_number() OVER (PARTITION BY userId, questionId ORDER BY STR_TO_DATE(responseTimeStamp, '%Y-%m-%d %H:%i:%s.%f') DESC) r FROM responses) tbl where r = 1 ORDER BY userId"
        users_features_df = pd.read_sql(query,engine).fillna(0)
        users_features_df['questionId'] = users_features_df['questionId'].apply(lambda x: f"questionId{x}")
        pivoted_users_features_df = users_features_df.pivot(index = 'userId' , columns = 'questionId', values='questionValue')
        
        rankings_df = pd.merge(rankings_df, pivoted_users_features_df, on='userId')
        print(rankings_df)
    
        rankings_df = rankings_df.astype('string')

        return rankings_df
    except Exception as e:
        print(str(e))

#==========================================================================================================================================================================

def get_users_rankings_dataframe_model(): #dataframne with userId, age, postcode, gender, cafeId, ranking

    engine = create_engine("mysql+mysqlconnector://sample:sample@localhost:33060/coffee-mate")

    try:
        #select ранкингов с пользовательскии данными age, postcode, gender
        query  = 'Select tbl.cafeId as cafeId, tbl.userId as userId, tbl.rankingValue as ranking from (SELECT *, row_number() OVER (PARTITION BY userId, cafeId ORDER BY STR_TO_DATE(rankingTimeStamp, "%Y-%m-%d %H:%i:%s.%f") DESC) r FROM rankings WHERE categoryId = 1 ) tbl WHERE r = 1 ORDER BY userId'

        rankings_df = pd.read_sql(query,engine).fillna(0)
        rankings_df = rankings_df.astype('string')
        return rankings_df
    except Exception as e:
        print(str(e))

#=========================================================================================================================================================================

def get_cluster_rankings_dataframe(): #dataframne with userId, age, postcode, gender, cafeId, ranking

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

#=========================================================================================================================================================================

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

#=========================================================================================================================================================================

def get_cafes_dataframe():

    engine = create_engine("mysql+mysqlconnector://sample:sample@localhost:33060/coffee-mate")

    try:
        #select cafe features
        query  = 'select cafeId, servesCoffee, takeout, goodForChildren, goodForGroups, delivery from cafes'
        cafe_features_df = pd.read_sql(query,engine, index_col='cafeId').fillna(0)
        #cafe_features_df = cafe_features_df.map(lambda x: f"{1 if x == 'TRUE' else 0}")
        #cafe_features_df['features'] =  cafe_features_df.to_numpy().tolist()
        cafe_features_df = cafe_features_df.reset_index()
    
        return cafe_features_df
    except Exception as e:
        print(str(e))

#=========================================================================================================================================================================

class RankingModel(tf.keras.Model):

  def __init__(self):
    super().__init__()
    embedding_dimension = 32

    # Compute embeddings for users.
    self.user_embeddings = tf.keras.Sequential([
      tf.keras.layers.StringLookup(
        vocabulary=unique_user_ids, mask_token=None),
      tf.keras.layers.Embedding(len(unique_user_ids) + 1, embedding_dimension)
    ])

    # Compute embeddings for movies.
    self.movie_embeddings = tf.keras.Sequential([
      tf.keras.layers.StringLookup(
        vocabulary=unique_movie_titles, mask_token=None),
      tf.keras.layers.Embedding(len(unique_movie_titles) + 1, embedding_dimension)
    ])

    # Compute predictions.
    self.ratings = tf.keras.Sequential([
      # Learn multiple dense layers.
      tf.keras.layers.Dense(256, activation="relu"),
      tf.keras.layers.Dense(64, activation="relu"),
      # Make rating predictions in the final layer.
      tf.keras.layers.Dense(1)
  ])

  def call(self, inputs):

    user_id, movie_title = inputs

    user_embedding = self.user_embeddings(user_id)
    movie_embedding = self.movie_embeddings(movie_title)

    return self.ratings(tf.concat([user_embedding, movie_embedding], axis=1))

#=========================================================================================================================================================================


ratings = ratings.map(lambda x: {
    "movie_title": x["movie_title"],
    "user_id": x["user_id"],
    "user_rating": x["user_rating"]
})


























#get_users_rankings_dataframe()



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
#cluster_rankings_dataframe = get_cluster_rankings_dataframe()
#cluster_cafe_matrix = cluster_rankings_dataframe.copy()
#users_cafe_matrix = get_user_rankings_dataframe()
#print(f'cluster_cafe_matrix: {cluster_cafe_matrix}')

# MODELING=============================================================
# make a model on:
# cluster_matrix

from typing import Dict, Text

import numpy as np
import tensorflow as tf
import pandas as pd
import tensorflow_recommenders as tfrs

# Ratings data.
#ds = tf.data.Dataset.from_tensor_slices((dict(get_users_rankings_dataframe())))


# Ratings data.
rankings = tf.data.Dataset.from_tensor_slices((dict(get_users_rankings_dataframe())))
# Features of all the available movies.
cafes = tf.data.Dataset.from_tensor_slices((dict(get_cafes_dataframe())))

# Select the basic features.
rankings = rankings.map(lambda x: {
    "cafeId": x["cafeId"],
    "userId": x["userId"]
})
cafes = cafes.map(lambda x: x["cafeId"])

user_ids_vocabulary = tf.keras.layers.StringLookup(mask_token=None)
user_ids_vocabulary.adapt(rankings.map(lambda x: x["userId"]))

cafe_titles_vocabulary = tf.keras.layers.StringLookup(mask_token=None)
cafe_titles_vocabulary.adapt(cafes)


class CaffeeMateModel(tfrs.Model):
  # We derive from a custom base class to help reduce boilerplate. Under the hood,
  # these are still plain Keras Models.

  def __init__(
      self,
      user_model: tf.keras.Model,
      cafe_model: tf.keras.Model,
      task: tfrs.tasks.Retrieval):
    super().__init__()

    # Set up user and cafe representations.
    self.user_model = user_model
    self.cafe_model = cafe_model

    # Set up a retrieval task.
    self.task = task

  def compute_loss(self, features: Dict[Text, tf.Tensor], training=False) -> tf.Tensor:
    # Define how the loss is computed.

    user_embeddings = self.user_model(features["userId"])
    cafe_embeddings = self.cafe_model(features["cafeId"])

    return self.task(user_embeddings, cafe_embeddings)

# Define user and cafe models.
user_model = tf.keras.Sequential([
    user_ids_vocabulary,
    tf.keras.layers.Embedding(user_ids_vocabulary.vocabulary_size(), 64)
])
cafe_model = tf.keras.Sequential([
    cafe_titles_vocabulary,
    tf.keras.layers.Embedding(cafe_titles_vocabulary.vocabulary_size(), 64)
])

# Define your objectives.
task = tfrs.tasks.Retrieval(metrics=tfrs.metrics.FactorizedTopK(
    cafes.batch(128).map(user_model)
  )
)

# Create a retrieval model.
model = CaffeeMateModel(user_model, cafe_model, task)
model.compile(optimizer=tf.keras.optimizers.Adagrad(0.5))

# Train for 3 epochs.
model.fit(rankings.batch(4096), epochs=3)

# Use brute-force search to set up retrieval using the trained representations.
index = tfrs.layers.factorized_top_k.BruteForce(model.user_model)
index.index_from_dataset(
    cafes.batch(100).map(lambda title: (title, model.cafe_model(title))))

# Get some recommendations.
_, titles = index(np.array(["42"]))
print(f"Top 3 recommendations for user 42: {titles[0, :10]}")