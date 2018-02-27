from flask import Flask, jsonify
import json
from flask import request

app = Flask(__name__)

dict1 = {}
index1 = 1
@app.route("/")
def hello():
    return "Hello World!"

@app.route('/users', methods=['POST'])
def add_user():
    global index1
    name = request.form["name"]
    dict1[index1] = name
    index1 = index1 + 1
    return (json.dumps([{'id': key, 'name': value} for key, value in dict1.items()]), 201)
    #return jsonify(dict1)


@app.route('/users/<id>', methods=['GET'])
def show_user(id=None):
    for key, value in dict1.items():
        if (int(key)==int(id)):
            return (json.dumps({'id': key, 'name': value}), 200)
    return "NULL"

@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id=None):
    for key, value in dict1.items():
        if (int(key)==int(id)):
            del dict1[key]
            return ('', 204)
    return ('', 204)