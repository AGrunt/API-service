import json
from flask import Flask, request, jsonify, render_template
from flask_swagger_ui import get_swaggerui_blueprint

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
#cursor = mydb.cursor()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/users/<id>', methods=['GET'])
def get_users(id):
    match id:
        case '':
            return f"Success", 200
        case '01061add-1302-4846-bb8e-b8e0ffe7ac84':
            return jsonify({'postcode': '2552', 'gender': 1, 'age': 22}), 200
        case '25c26f74-d0eb-408b-8f97-26429032c832':
            return jsonify({'postcode': '2500', 'gender': 0, 'age': 0}), 200
        case '273cf928-a41f-43c6-9dac-c13385b2a29e':
            return jsonify({'postcode': '2518', 'gender': 1, 'age': 32}), 200
    return f"Not found", 404

@app.route('/users/<id>', methods=['PUT'])
def put_users(id):
    match id:
        case '':
            return f'Success', 200
        case '01061add-1302-4846-bb8e-b8e0ffe7ac84':
            return f"Conflict", 409
        case '25c26f74-d0eb-408b-8f97-26429032c832':
            return f"Conflict", 409
        case '273cf928-a41f-43c6-9dac-c13385b2a29e':
            return f"Conflict", 409
    return f"Created", 201

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

#Run swagger 
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)
#Run flask
app.run(debug=True)