import os
from datetime import datetime
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo

application = Flask(__name__)

application.config["MONGO_URI"] = 'mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ['MONGODB_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + ':27017/' + os.environ['MONGODB_DATABASE']

mongo = PyMongo(application)
db = mongo.db

def get_hit_count():
    doc = list(db.count.find())
    iters = 0
    for row in doc:
        iters = iters + 1
        last_count = int(row['count']) + 1
        db.count.update_one({ '_id': row['_id'] }, { "$set":{
            'count': int(row['count']) + 1 , 
            'datetime': datetime.now(), 
            'client_info': request.headers.get('User-Agent') }})
        return last_count
    if (iters == 0):
        db.count.insert_one({ 
            'count': 1 , 
            'datetime': datetime.now(), 
            'client_info': request.headers.get('User-Agent')})
        return 1

@application.route('/')
def hello():
    count = get_hit_count()
    return 'Hello World! I have been seen {} times.\n'.format(count)

if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5000)
    application.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)