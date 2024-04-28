import json
import time
from flask import Flask, request, jsonify, render_template
from flask_swagger_ui import get_swaggerui_blueprint
import mysql.connector
from datetime import datetime

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

    dbConnection = mysql.connector.connect(
        host="api-db",
        port="3306",
        user="sample",
        password="sample",
        database="coffee-mate"
        )

    cursor = dbConnection.cursor()
    
    try:
        select_stmt = ('SELECT cafeId, predicitonValue FROM predictions WHERE userId = %(userId)s '
                       f'ORDER BY predicitonValue DESC LIMIT {int(request.args['size'])} OFFSET {int(request.args['start'])}')
        cursor.execute(select_stmt, {'userId': id})
        results = cursor.fetchall()
        pred_list = [{'cafe': result[0], 'ranking': result[1]} for result in results]
        pred_dictionary = {"recommendations": pred_list}
        cursor.close()
        dbConnection.close()
        return jsonify(pred_dictionary), 200
    except Exception as err:
        cursor.close()
        dbConnection.close()
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
            cursor.execute(insert_stmt, {'userId': id, 'questionId': response['questionId'], 'questionValue': response['questionValue'], 'responseTimeStamp': datetime.now()})
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
            cursor.execute(insert_stmt, {'userId': id, 'cafeId': cafeid, 'categoryId': ranking['categoryId'], 'rankingValue': ranking['rankingValue'], 'responseTimeStamp': datetime.now()})
        dbConnection.commit()
        cursor.close()
        dbConnection.close()
        return 'Created', 201
    except Exception as err:
        dbConnection.rollback()
        cursor.close()
        dbConnection.close()
        return f'Error: {err}', 500

#Run swagger 
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)
#Run flask
app.run(debug=True)