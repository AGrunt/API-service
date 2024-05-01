import os
from typing import Dict, Text
import numpy as np
import tensorflow as tf
import tensorflow_recommenders as tfrs
from sqlalchemy import create_engine
import pandas as pd

pd.set_option('future.no_silent_downcasting', True)
os.environ['LOKY_MAX_CPU_COUNT'] = '0' #exclude warnings

def get_ratings_dataframe():

    engine = create_engine("mysql+mysqlconnector://sample:sample@localhost:33060/coffee-mate")

    try:
        query = 'SELECT tbl.cafeId AS cafe_id, tbl.userId AS user_id, tbl.rankingValue AS rating from (SELECT *, row_number() OVER (PARTITION BY userId, cafeId ORDER BY STR_TO_DATE(rankingTimeStamp, "%Y-%m-%d %H:%i:%s.%f") DESC) r FROM rankings WHERE categoryId = 1) tbl WHERE r = 1'
        rankings_df = pd.read_sql(query, engine, dtype={'user_id': 'string', 'cafe_id': 'string', 'rating': 'float32'})
        return rankings_df
    except Exception as e:
        print(str(e))

def get_cafes_dataframe():

    engine = create_engine("mysql+mysqlconnector://sample:sample@localhost:33060/coffee-mate")

    try:
        query = 'SELECT DISTINCT tbl.cafeId AS cafe_id from (SELECT *, row_number() OVER (PARTITION BY userId, cafeId ORDER BY STR_TO_DATE(rankingTimeStamp, "%Y-%m-%d %H:%i:%s.%f") DESC) r FROM rankings WHERE categoryId = 1) tbl WHERE r = 1'
        rankings_df = pd.read_sql(query, engine, dtype={'cafe_id': 'string'})
        return rankings_df
    except Exception as e:
        print(str(e))

ratings_df = get_ratings_dataframe()
cafes_df = get_cafes_dataframe()

ratings = tf.data.Dataset.from_tensor_slices((dict(ratings_df)))
cafes = tf.data.Dataset.from_tensor_slices((dict(cafes_df)))

ratings = ratings.map(lambda x: {
    "cafe_id": x["cafe_id"],
    "user_id": x["user_id"],
})
cafes = cafes.map(lambda x: x["cafe_id"])

tf.random.set_seed(42)
shuffled = ratings.shuffle(20000, seed=42, reshuffle_each_iteration=False)

train = shuffled.take(int(len(ratings)*0.8))
test = shuffled.skip(int(len(ratings)*0.8)).take(int(len(ratings) - len(ratings)*0.8))

cafe_ids = cafes.batch(1_000)
user_ids = ratings.batch(1_000_000).map(lambda x: x["user_id"])

unique_cafe_ids = np.unique(np.concatenate(list(cafe_ids)))
unique_user_ids = np.unique(np.concatenate(list(user_ids)))

embedding_dimension = 32

user_model = tf.keras.Sequential([
  tf.keras.layers.StringLookup(
      vocabulary=unique_user_ids, mask_token=None),
  # We add an additional embedding to account for unknown tokens.
  tf.keras.layers.Embedding(len(unique_user_ids) + 1, embedding_dimension)
])

cafe_model = tf.keras.Sequential([
  tf.keras.layers.StringLookup(
      vocabulary=unique_cafe_ids, mask_token=None),
  tf.keras.layers.Embedding(len(unique_cafe_ids) + 1, embedding_dimension)
])

metrics = tfrs.metrics.FactorizedTopK(
  candidates=cafes.batch(128).map(cafe_model)
)

task = tfrs.tasks.Retrieval(
  metrics=metrics
)

class CoffeeMateModel(tfrs.Model):

  def __init__(self, user_model, cafe_model):
    super().__init__()
    self.cafe_model: tf.keras.Model = cafe_model
    self.user_model: tf.keras.Model = user_model
    self.task: tf.keras.layers.Layer = task

  def compute_loss(self, features: Dict[Text, tf.Tensor], training=False) -> tf.Tensor:
    # We pick out the user features and pass them into the user model.
    user_embeddings = self.user_model(features["user_id"])
    # And pick out the movie features and pass them into the movie model,
    # getting embeddings back.
    positive_cafe_embeddings = self.cafe_model(features["cafe_id"])

    # The task computes the loss and the metrics.
    return self.task(user_embeddings, positive_cafe_embeddings)

model = CoffeeMateModel(user_model, cafe_model)
model.compile(optimizer=tf.keras.optimizers.Adagrad(learning_rate=0.1))

cached_train = train.shuffle(20000).batch(8192).cache()
cached_test = test.batch(4096).cache()

model.fit(cached_train, epochs=20)

model.evaluate(cached_test, return_dict=True)

# Create a model that takes in raw query features, and
index = tfrs.layers.factorized_top_k.BruteForce(model.user_model, k=25)
# recommends movies out of the entire movies dataset.
index.index_from_dataset(
  tf.data.Dataset.zip((cafes.batch(100), cafes.batch(100).map(model.cafe_model)))
)

# Get recommendations.
_, ids = index(tf.constant(["001c430d-5e6b-453c-b735-8ae3a4721a37"]))

# Save model.  
path = './models/model_user'
tf.saved_model.save(index, path)