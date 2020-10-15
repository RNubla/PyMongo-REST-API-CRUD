from flask import Flask, request, json
from flask.json import dumps, jsonify
from flask_pymongo import PyMongo

# client = MongoClient('mongodb://localhost:27017/ContactDB')
# db = client.Contact


app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb://localhost:27017/ContactDB'
mongo = PyMongo(app)


@app.route('/')
def hello():
    return 'welcome to flask'


@app.route('/add_contact', methods=['POST'])
def add_contacts():
    name = request.json['name']
    contact = request.json['contact']
    if name and contact:
        id = mongo.db.Contacts.insert(
            {'name': name, 'contact': contact}
        )
        response = jsonify({
            '_id': str(id),
            'name': name,
            'contact': contact
        })
        response.status_code = 201
        return response
    else:
        return not_found()


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'message': 'Resource not found' + request.url,
        'status': 404
    }
    response = jsonify(message)
    response.status_code = 404
    return response


@app.route("/get_all_contact", methods=['GET'])
def get_all_contact():
    try:
        contacts = db.Contacts.find()
        return dumps(contacts)
    except Exception as e:
        return dumps({'error': str(e)})


if __name__ == "__main__":
    app.run(debug=True)
