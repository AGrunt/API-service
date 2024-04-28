import os
from typing import Dict, Text

import numpy as np
import tensorflow as tf
import tensorflow_recommenders as tfrs
#==============
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

pd.set_option('future.no_silent_downcasting', True)
os.environ['LOKY_MAX_CPU_COUNT'] = '0' #exclude wornings

def get_user_rankings_dataframe():

    engine = create_engine("mysql+mysqlconnector://sample:sample@localhost:33060/coffee-mate")

    try:
        query = "Select tbl.userId as user_id, tbl.cafeId as movie_title, tbl.rankingValue as user_rating "
        query += "from (SELECT *, row_number() OVER (PARTITION BY userId, cafeId ORDER BY STR_TO_DATE(rankingTimeStamp, '%Y-%m-%d %H:%i:%s.%f') DESC) r FROM rankings WHERE categoryId = 1) tbl "
        query += "WHERE r = 1 ORDER BY userId"
        rankings_df = pd.read_sql(query,engine)
        print(rankings_df)
    
        return rankings_df
    except Exception as e:
        print(str(e))

df = get_user_rankings_dataframe()

dataset_len = len(df)

ratings = tf.data.Dataset.from_tensor_slices((dict(df)))

ratings = ratings.map(lambda x: {
    "movie_title": x["movie_title"],
    "user_id": x["user_id"],
    "user_rating": x["user_rating"]
})



tf.random.set_seed(42)
shuffled = ratings.shuffle(dataset_len, seed=42, reshuffle_each_iteration=False)

train = shuffled.take(round(0.8*dataset_len))
test = shuffled.skip(round(0.8*dataset_len)).take(round(dataset_len-round(0.8*dataset_len)))


movie_titles = ratings.batch(dataset_len).map(lambda x: x["movie_title"])
user_ids = ratings.batch(dataset_len).map(lambda x: x["user_id"])

unique_movie_titles = np.unique(np.concatenate(list(movie_titles)))
unique_user_ids = np.unique(np.concatenate(list(user_ids)))

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
  
task = tfrs.tasks.Ranking(
  loss = tf.keras.losses.MeanSquaredError(),
  metrics=[tf.keras.metrics.RootMeanSquaredError()]
)

RankingModel()((["42"], ["One Flew Over the Cuckoo's Nest (1975)"]))

class CafesModel(tfrs.models.Model):

  def __init__(self):
    super().__init__()
    self.ranking_model: tf.keras.Model = RankingModel()
    self.task: tf.keras.layers.Layer = tfrs.tasks.Ranking(
      loss = tf.keras.losses.MeanSquaredError(),
      metrics=[tf.keras.metrics.RootMeanSquaredError()]
    )

  def call(self, features: Dict[str, tf.Tensor]) -> tf.Tensor:
    return self.ranking_model(
        (features["user_id"], features["movie_title"]))

  def compute_loss(self, features: Dict[Text, tf.Tensor], training=False) -> tf.Tensor:
    labels = features.pop("user_rating")
    
    rating_predictions = self(features)

    # The task computes the loss and the metrics.
    return self.task(labels=labels, predictions=rating_predictions)
  

model = CafesModel()
model.compile(optimizer=tf.keras.optimizers.Adagrad(learning_rate=0.1))

cached_train = train.shuffle(dataset_len).batch(8192).cache()
cached_test = test.batch(4096).cache()

model.fit(cached_train, epochs=3)

model.evaluate(cached_test, return_dict=True)

test_ratings = {}
test_movie_titles = ["ChIJVVVVVZkZE2sRBRiwIBkxFsc", "ChIJofTclHQZE2sRkFvkn3SVYrA", "ChIJdeiUZa8ZE2sRLBJ4s8KNdsw"]
for movie_title in test_movie_titles:
  test_ratings[movie_title] = model({
      "user_id": np.array(["001c430d-5e6b-453c-b735-8ae3a4721a37"]),
      "movie_title": np.array([movie_title])
  })

print("Ratings:")
for title, score in sorted(test_ratings.items(), key=lambda x: x[1], reverse=True):
  print(f"{title}: {score}")


#prepare params of model
path = './models/'
timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
export_model_name = f'{path}model-{timestamp}'

#export model
tf.saved_model.save(model, export_model_name)

#write model params to db
engine = create_engine("mysql+mysqlconnector://sample:sample@localhost:33060/coffee-mate")

try:
    dbConnection = mysql.connector.connect(
        host="localhost",
        port="33060",
        user="sample",
        password="sample",
        database="coffee-mate"
        )

    #dbConnection = mysql.connector.connect(
    #    host="api-db",
    #    port="3306",
    #    user="sample",
    #    password="sample",
    #    database="coffee-mate"
    #    )


    cursor = dbConnection.cursor()

    query = "INSERT INTO models (model_name, modelTimeStamp) VALUES (export_model_name = 'model')"
    rankings_df = pd.read_sql(query,engine)
    
    insert_stmt = 'INSERT INTO models (model_name, modelTimeStamp) VALUES (export_model_name = "%(export_model_name)s", modelTimeStamp = "%(modelTimeStamp)s")'

    cursor.execute(insert_stmt, {'export_model_name':export_model_name, 'modelTimeStamp': timestamp})
    cursor.close()
    dbConnection.close()

except Exception as e:
    cursor.close()
    dbConnection.close()
    print(str(e))

#loaded = tf.saved_model.load("export")

#loaded({"user_id": np.array(["001c430d-5e6b-453c-b735-8ae3a4721a37"]), "movie_title": ["ChIJdeiUZa8ZE2sRLBJ4s8KNdsw"]}).numpy()