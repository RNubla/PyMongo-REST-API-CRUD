from flask import Flask, request
from flask.json import jsonify
from flask_pymongo import PyMongo, MongoClient
from bson.json_util import dumps, loads
# import json
import pprint

client = MongoClient('localhost', 27017)
db = client.ContactDB
contactCollection = db.Contacts


app = Flask(__name__)


@app.route('/', methods=["POST"])
def add_stuff():
    new_post = [{'name': request.json['name']}]
    # return contactCollection.insert_many(new_post).inserted_ids
    contactCollection.insert_many(new_post).inserted_ids
    return dumps(new_post)


@app.route('/', methods=["GET"])
def get_stuff():
    return (dumps(contactCollection.find(), indent=2))


@app.route('/<name>', methods=['GET'])
def get_one(name):
    _name = contactCollection.find_one({'name': name})
    return dumps(_name)


@app.route('/', methods=["DELETE"])
def remove_one():
    remove_post = {'name': request.json['name']}
    contactCollection.delete_one(remove_post)
    return remove_post


@app.route('/', methods=["PUT"])
def update_one():
    old_query = {'name': request.json['name']}
    new_query = {"$set": {'name': request.json['newname']}}
    contactCollection.update_one(old_query, new_query)
    return new_query


if __name__ == "__main__":
    app.run(debug=True)
