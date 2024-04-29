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


#wait for mysqlService
time.sleep(10)

SWAGGER_URL="/swagger"
API_URL="/static/swagger.json"

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config = {
        'app_name': 'Access API'
    }
)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/users/<id>', methods=['GET'])
def get_users(id):

    if len(id) == 0:
        return f'Invalid arguments', 400

    dbConnection = mysql.connector.connect(
        host="api-db",
        port="3306",
        user="sample",
        password="sample",
        database="coffee-mate"
        )

    cursor = dbConnection.cursor()
    
    try:
        select_stmt = ('SELECT userId, gender, age, postcode FROM usersTable WHERE userId = %(userId)s LIMIT 1')
        cursor.execute(select_stmt, {'userId':id})
        result = cursor.fetchone()
        if result:
            output = {       
                      'gender': result[0][1],
                      'age': result[0][2],
                      'postcode': result[0][4]
                      }
            cursor.close()
            dbConnection.close()
            return jsonify(output), 200
        else:
            cursor.close()
            dbConnection.close()
            return f'<userId>: <{id}>. Not found ', 404             
    except Exception as err:
        cursor.close()
        dbConnection.close()
        return f'Error: {err}', 500

@app.route('/users/<id>', methods=['PUT'])
def put_users(id):
    
    if len(id) == 0:
        return f'Invalid arguments', 400
    
    dbConnection = mysql.connector.connect(
        host="api-db",
        port="3306",
        user="sample",
        password="sample",
        database="coffee-mate"
        )

    cursor = dbConnection.cursor()
    
    try:
        insert_stmt = ('INSERT INTO usersTable (userId, gender, age, postcode) VALUES (%(userId)s, %(gender)s, %(age)s, %(postcode)s)')
        cursor.execute(insert_stmt, {'userId': id, 'gender': request.json['gender'], 'age': request.json['age'], 'postcode': request.json['postcode']})
        dbConnection.commit()
        cursor.close()
        dbConnection.close()
        return 'Created', 201
    except Exception as err:
        dbConnection.rollback()
        cursor.close()
        dbConnection.close()
        return f'Error: {err}', 500

@app.route('/users/<id>/recommendations', methods=['GET'])
def get_users_recommendations(id):
       
    if len(id) == 0:
        return f'Invalid arguments', 400

    try:
        pred_dictionary = recomendations(id, int(request.args['start']), int(request.args['size']))    
        return jsonify(pred_dictionary), 200
    except Exception as err:
        return f'Error: {err}', 500
            
@app.route('/users/<id>/responses', methods=['PUT'])
def put_responses(id):
    
    if len(id) == 0:
        return f'Invalid arguments', 400
    
    dbConnection = mysql.connector.connect(
        host="api-db",
        port="3306",
        user="sample",
        password="sample",
        database="coffee-mate"
        )

    cursor = dbConnection.cursor()
    
    try:
        for response in request.json('responses'):
            insert_stmt = ('INSERT INTO responses (userId, questionId, questionValue, responseTimeStamp) VALUES (%(userId)s, %(questionId)s, %(questionValue)s, %(responseTimeStamp)s)')
            cursor.execute(insert_stmt, {'userId': id, 'questionId': request.json['questionId'], 'questionValue': request.json['questionValue'], 'responseTimeStamp': datetime.now()})
        dbConnection.commit()
        cursor.close()
        dbConnection.close()
        return 'Created', 201
    except Exception as err:
        dbConnection.rollback()
        cursor.close()
        dbConnection.close()
        return f'Error: {err}', 500

@app.route('/users/<id>/rankings/<cafeid>', methods=['PUT'])
def put_ranking(id, cafeid):
    
    if len(id) == 0:
        return f'Invalid arguments', 400
    
    dbConnection = mysql.connector.connect(
        host="api-db",
        port="3306",
        user="sample",
        password="sample",
        database="coffee-mate"
        )

    cursor = dbConnection.cursor()
    
    try:
        for ranking in request.json('rankings'):
            insert_stmt = ('INSERT INTO rankings (userId, cafeId, categoryId, rankingValue, rankingTimeStamp) '
                           'VALUES (%(userId)s, %(cafeId)s, %(categoryId)s, %(rankingValue)s, %(rankingTimeStamp)s)')
            cursor.execute(insert_stmt, {'userId': id, 'cafeId': cafeid, 'categoryId': request.json['categoryId'], 'rankingValue': request.json['rankingValue'], 'responseTimeStamp': datetime.now()})
        dbConnection.commit()
        cursor.close()
        dbConnection.close()
        return 'Created', 201
    except Exception as err:
        dbConnection.rollback()
        cursor.close()
        dbConnection.close()
        return f'Error: {err}', 500

def recomendations(id, start, size):
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

    engine = create_engine("mysql+mysqlconnector://sample:sample@api-db:3306/coffee-mate")

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
    final_df['ranking'] = ( final_df['ranking_user']*0.75 + final_df['ranking_group']*0.25)
    final_df = final_df.sort_values(by='ranking', ascending=False)
    final_df['cafe'] = final_df['cafe'].astype('string')
    final_df = final_df[['cafe', 'ranking']]
    pred_dictionary = {"recommendations": final_df.to_dict('records')[start:start+size]}

    return pred_dictionary

#Run swagger 
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)
#Run flask
app.run(debug=True)