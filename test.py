import json
import time
from flask import Flask, request, jsonify, render_template
from flask_swagger_ui import get_swaggerui_blueprint
import mysql.connector
from datetime import datetime
import tensorflow as tf
import pickle
from  sqlalchemy import create_engine
import pandas as pd
from pandas import DataFrame


id = '00a13788-c564-4527-9b97-3921728a1459'


#load kmenas model
kmeans_path = './models/kmeans.pkl' 
kmeans_loaded = pickle.load(open('./models/kmeans.pkl', 'rb'))

'models/kmeans.pkl'

#load group model
model_group_path = './models/model_group'
model_group_loaded = tf.saved_model.load(model_group_path)

#load user model
model_user_path = './models/model_user'
model_user_loaded = tf.saved_model.load(model_user_path)

engine = create_engine("mysql+mysqlconnector://sample:sample@localhost:33060/coffee-mate")


query = "SELECT userId, age, postcode, gender FROM usersTable WHERE userId = %(userId)s"
users_df = pd.read_sql(query,engine, index_col='userId', params={'userId': id}).fillna(0)
postcodes = users_df['postcode'].unique()
postcodes_map = { postcode:index for index, postcode in enumerate(postcodes)}
users_df['postcodeId'] = users_df['postcode'].map(postcodes_map)

#get just last question by timestamp
query = "SELECT tbl.userId, tbl.questionId, tbl.questionValue FROM (SELECT *, ROW_NUMBER() OVER (PARTITION BY userId, questionId ORDER BY STR_TO_DATE(responseTimeStamp, '%Y-%m-%d %H:%i:%s.%f') DESC) r FROM responses) tbl WHERE r = 1 AND userId = %(userId)s"
questions_df = pd.read_sql(query,engine, params={'userId': id}).fillna(0)

pivoted_questions_df = questions_df.pivot(index = 'userId' , columns = 'questionId', values='questionValue')
users_df = users_df.join(pivoted_questions_df).fillna(0)

#change dtype of selected columns
columns_names = users_df.loc[:, users_df.columns != 'postcode'].columns.values.tolist()
types = { str(column): 'int32' for column in columns_names}
users_df = users_df[columns_names].astype(types)

#predict usergroup from kmeans model
results = kmeans_loaded.predict(users_df) 
group_scores, group_cafe_ids = model_group_loaded([str(results[0])])
user_scores, user_cafe_ids = model_user_loaded([str(id)])

group_data = {'cafe': group_cafe_ids[0][:].numpy(), 'ranking_group':  group_scores[0][:].numpy()}
group_df = pd.DataFrame.from_dict(group_data)

user_data = {'cafe': user_cafe_ids[0][:].numpy(), 'ranking_user':  user_scores[0][:].numpy()}
user_df = pd.DataFrame.from_dict(user_data)

final_df = pd.DataFrame.merge(group_df, user_df, how='outer', on='cafe').fillna(0)
final_df['ranking'] = ( final_df['ranking_user'] + final_df['ranking_group'] ) / 2
final_df = final_df.sort_values(by='ranking', ascending=False)
final_df['cafe'] = final_df['cafe'].astype('string')
final_df = final_df[['cafe', 'ranking']]
pred_dictionary = {"recommendations": final_df.to_dict('records')}




print(pred_dictionary)


print(json.dumps(pred_dictionary))


{'recommendations': 
 [{'cafe': b'ChIJWz01d80ZE2sR8KZjVcPXEf8', 'ranking': 0.17160630226135254}, 
  {'cafe': b'ChIJi0TsfQQZE2sRfux3aa5nfEo', 'ranking': 0.16705107688903809}, 
  {'cafe': b'ChIJm8PBO2wNE2sRHNq3j8zN_2s', 'ranking': 0.15944017469882965},
  {'cafe': b'ChIJ8xbSZ7kfE2sRcJ45qFwgQr0', 'ranking': 0.15917719900608063}
  ]}