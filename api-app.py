import json
from flask import Flask, request, jsonify, render_template
from flask_swagger_ui import get_swaggerui_blueprint
import mysql.connector
from datetime import datetime

#Creating db connector
dbConnection = mysql.connector.connect(
  host="api-db",
  port="3306",
  user="sample",
  password="sample",
  database="coffee-mate"
  )

# Make a cursor
cursor = dbConnection.cursor()

SWAGGER_URL="/swagger"
API_URL="/static/swagger.json"

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config = {
        'app_name': 'Access API'
    }
)

# Make a cursor
cursor = dbConnection.cursor()

app = Flask(__name__)

#Function for retrieving and checking existence of data in the database. Return true if data found.
def get_data(table, data, check):
    #Expected that data is a dictionarry.  with {columnName:value} format
    conditions_string = ''
    values = ()
    #combine data
    for index, column in enumerate(data.keys()):
        if index < len(data.keys()) - 1:
            conditions_string +=  f'{column} = %s AND '
        else:
            conditions_string +=  f'{column} = %s'
        values += tuple([data[column]])
    #make select stetment
    if check:
        check_stmt = (
            f'SELECT COUNT(*) FROM {table} '
            f'WHERE {conditions_string}'
            )
        cursor.execute(check_stmt, values)
        myresult = cursor.fetchone()
        if int(myresult[0]) > 0:
            return True
    else:
        select_stmt = (
            f'SELECT * FROM {table} '
            f'WHERE {conditions_string}'
            )
        cursor.execute(select_stmt, values)
        result = cursor.fetchall()
        print(result)
        return result
    
def put_data(table, data):
#Expected that data is a dictionarry.  with {columnName:value} format
    columns_string = ''
    values_string = ''
    values = ()
    #combine data
    try: 
        for index, column in enumerate(data.keys()):
            if index < len(data.keys()) - 1:
                columns_string += f'{column}, '
                values_string +=  f'%s, '
            else:
                columns_string += f'{column}'
                values_string +=  f'%s'
            values += tuple([data[column]])
        #make insert stetement
        insert_stmt = (
        f'INSERT INTO {table} ({columns_string}) '
        f'VALUES ({values_string})'
        )
        cursor.execute(insert_stmt, values)
        dbConnection.commit()
    except Exception as err:
        return False, err, 500
    return True

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/users/<id>', methods=['GET'])
def get_users(id):
    # combine data
    table = 'usersTable'
    data = {'userid': str(id)}    
    match id:
        case '':
            return f'Success', 200
    
    if not get_data(table, data, check=True):
        return f"Not found", 404
    result = get_data(table, data, check=False)
    # Creation output dictionary 
    output = {       
        'gender': result[0][1],
        'age': result[0][2],
        'postcode': result[0][4]
        }
    return jsonify(output), 200

@app.route('/users/<id>', methods=['PUT'])
def put_users(id):
    match id:
        case '':
            return f'Success', 200
    #Check if user exists already
    table = 'usersTable'
    data = {'userid': id}
    if get_data(table, data, check=True):
        return f"Conflict", 409
    #Put user's data into database
    #combine data
    data = {
        'userId': str(id),
        'gender': int(request.json['gender']),
        'age': int(request.json['age']),
        'registrationTimeStamp': str(datetime.now()),
        'postcode': str(request.json['postcode'])
        }
    results = put_data('usersTable', data)
    if type(results) is not bool:
        return f'Something went wrong. Data :<{data}>. Results: <{results}>', 500
    return f'Created.', 201

@app.route('/users/<id>/recommendations', methods=['GET'])
def get_users_recommendations(id):
    match id:
        case '':
            return f"Success", 200
        case '01061add-1302-4846-bb8e-b8e0ffe7ac84':
            return jsonify({
                'predictions': 
                [{'cafe': 'ChIJvxY0e1UZE2sRshBd4u2VPNc', 'ranking': 0.98},
                 {'cafe': 'ChIJEeMz8sMZE2sRynqdMW4YF9g', 'ranking': 0.94}, 
                 {'cafe': 'ChIJj8l_uYYUE2sRPddj46-ukO0', 'ranking': 0.82}]}), 200
        case '25c26f74-d0eb-408b-8f97-26429032c832':
            return jsonify({
                'predictions': 
                [{'cafe': 'ChIJvxY0e1UZE2sRshBd4u2VPNc', 'ranking': 0.98},
                 {'cafe': 'ChIJEeMz8sMZE2sRynqdMW4YF9g', 'ranking': 0.94}, 
                 {'cafe': 'ChIJj8l_uYYUE2sRPddj46-ukO0', 'ranking': 0.82}]}), 200
        case '273cf928-a41f-43c6-9dac-c13385b2a29e':
            return jsonify({
                'predictions': 
                [{'cafe': 'ChIJvxY0e1UZE2sRshBd4u2VPNc', 'ranking': 0.98},
                 {'cafe': 'ChIJEeMz8sMZE2sRynqdMW4YF9g', 'ranking': 0.94}, 
                 {'cafe': 'ChIJj8l_uYYUE2sRPddj46-ukO0', 'ranking': 0.82}]}), 200
    return f"Not found", 404
        
@app.route('/users/<id>/responses', methods=['PUT'])
def put_responses(id):
    match id:
        case '':
            return f'Success', 200
        case '01061add-1302-4846-bb8e-b8e0ffe7ac84':
            return f'Created', 201
        case '25c26f74-d0eb-408b-8f97-26429032c832':
            return f'Created', 201        
        case '273cf928-a41f-43c6-9dac-c13385b2a29e':
            return f'Created', 201
    return f'Not found', 404

@app.route('/users/<id>/rankings/<cafeid>', methods=['PUT'])
def put_ranking(id, cafeid):
    #check if user exist and cafeid exist
    #Check userId
    table = 'usersTable'
    data = {'userId': id}
    if not get_data(table, data, check=True):
         return f'<userId>: <{id}>. Not found ', 404
    #Check cafeId
    table = 'cafes'
    data = {'cafeId': cafeid}
    if not get_data(table, data, check=True):
         return f'<cafeid>: <{cafeid}>. Not found', 404
    
    #insert user ranking data intop database
    table = 'rankings'
    data = {
        'userId': id,
        'cafeId': cafeid, 
        'categoryId': request.json['rankings'][0]['categoryId'],
        'rankingValue': request.json['rankings'][0]['rank'],
        'rankingTimeStamp': datetime.now()
        }
    #Generating console output
    results = put_data(table, data)
    if type(results) is not bool:
        return f'Something went wrong. Data :<{data}>. Results: <{results}>', 500
    return f'Created', 201

@app.route('/db_test')
def bd_test():
    #TEst database connection
    select_stmt = (
        f'SHOW TABLES'
        )
    cursor.execute(select_stmt)
    dbs = ''
    for db in cursor.fetchall():
        dbs += f'{db}, '
    
    
    return dbs

#Run swagger 
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)
#Run flask
app.run(debug=True)