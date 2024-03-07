import json
from flask import Flask, request, jsonify
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

app = Flask(__name__)

@app.route('/users/<id>', methods=['GET'])
def get_users(id):
    return jsonify({'postcode': '2515', 'gender': 0, 'age': 45})

@app.route('/users/<id>', methods=['PUT'])
def put_users(id):
    return f"Success", 200

@app.route('/users/<id>/recommendations', methods=['GET'])
def get_users_recommendations(id):
    return jsonify({'predictions': [{'cafe': 'a6ffc3e9-a33b-4afb-b9c8-aa63bd0e49f3', 'ranking': 0.98}, {'cafe': '6901e116-3bde-44bc-9b67-9b0a7b31e3a5', 'ranking': 0.94}, {'cafe': '7259acf8-90bc-40b5-98cd-73781536dcbe', 'ranking': 0.82}]})

@app.route('/users/<id>/responses', methods=['PUT'])
def put_responses(id):
    return f"Success", 200

@app.route('/users/<id>/<cafeid>/rankings', methods=['PUT'])
def put_ranking(id, cafeid):
    return f"Success", 200

#Run swagger 
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)
#Run flask
app.run(debug=True)