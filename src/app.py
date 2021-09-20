from bson import objectid
from flask import Flask, request, jsonify
from flask import json
from flask.json import jsonify
from flask.wrappers import Response
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.wrappers import response
from bson import json_util
from bson.objectid import ObjectId


app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/pythonmongodb'
mongo = PyMongo(app)

@app.route('/users', methods=['POST'])
def create_user():
    
    # Get data format json
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']

    # Save data in mongodb
    if username and password and email:

        hashed_password = generate_password_hash(password)

        id = mongo.db.user.insert(
            {
                'username': username,
                'password': hashed_password,
                'email': email
            }
        )
        response = {
            'id': str(id),
            'username': username,
            'password': hashed_password,
            'emial': email
        }
        return response
    else:
        return not_found()


    return {'message': 'received'}


# List users
@app.route('/users', methods=['GET'])
def get_users():
    users = mongo.db.user.find()
    response = json_util.dumps(users)
    return Response(response, mimetype='application/json')

# Get one user
@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = mongo.db.user.find_one({
        '_id': ObjectId(id)
    })
    response = json_util.dumps(user)
    return Response(response, mimetype='application/json')


# Delete user
@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    mongo.db.user.delete_one({
        '_id': ObjectId(id)
    })
    response = jsonify({
        'message': 'User ' + id + ' it was deleted' 
    })
    return response

# Update User
@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
        
    # Get data format json
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']

    if username and password and email:
        hashed_password = generate_password_hash(password)
        mongo.db.user.update_one({
            '_id': ObjectId(id['$oid']) if '$oid' in id else ObjectId(id)
            }, 
            {'$set': {
                'username': username, 
                'email': email, 
                'password': hashed_password
                }}
                )
        response = jsonify({'message': 'User' + id + 'Updated Successfuly'})
        response.status_code = 200
        return response

# Error message
@app.errorhandler(404)
def not_found(error=None):
    response = jsonify({
        'message': 'Resouce Not Found: ' + request.url,
        'status': 404
    })
    response.status_code = 404
    return response

if __name__ == "__main__":
    app.run(debug=True)