import json
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from helper.twitter_helper import create_api
from helper.firebase_helper import getFirestoreDB, getFirebaseAuth
from firebase_admin import firestore
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/search/<username>', methods=['GET'])
@cross_origin()
def search_users(username):
    authToken = request.headers.get('authToken')
    auth = getFirebaseAuth()
    try:
        auth.verify_id_token(authToken)
    except Exception as e:
        return jsonify({"data": "Invalid auth token, make sure you are logged in"}), 500
    twitterApi = create_api()
    searchResults = twitterApi.search_users(username)
    response = []

    for user in searchResults:
        response.append({'name': user._json["name"],
                         'screen_name': user._json["screen_name"]
                         })
    return jsonify({"data": response}), 200


@app.route('/add', methods=['POST'])
def add_to_db():
    twitterApi = create_api()
    requestData = request.get_json()
    authToken = request.headers.get('authToken')
    
    try:
        auth = getFirebaseAuth()
        auth.verify_id_token(authToken)

        documentPath = 'tHandles/'+requestData["handle"]
        db = getFirestoreDB()
        db.document(documentPath).set({})
        return jsonify({"data": "success"}), 200
    except Exception as e:
        print(e)
        return jsonify({"data": "Invalid auth token, make sure you are logged in"}), 500


@app.route('/get', methods=['GET'])
def get_from_db():

    dataPath = request.args.get('dataPath')
    orderBy = request.args.get('orderBy')
    startAfter = request.args.get('startAfter')
    limit = request.args.get('limit')
    authToken = request.headers.get('authToken')
    
    try:
        auth = getFirebaseAuth()
        # auth.verify_id_token(authToken)

        db = getFirestoreDB()
        query = db.collection(u'{dataPath}')
        # if orderBy != None:
        #     query = query.order_by(orderBy, direction=firestore.Query.DESCENDING)
        # if startAfter != None:
        #     query = query.start_after(startAfter)
        # if limit != None:
        #     query = query.limit(int(limit))

        data = query.stream()
        for doc in data:
            print(f'{doc.id} => {doc.to_dict()}')
        return jsonify({"data": "success"}), 200
    except Exception as e:
        print(e)
        return jsonify({"data": "Invalid auth token, make sure you are logged in"}), 500
        
# if __name__ == "__main__":
#     app.run(port=5000)

def initServer():
    app.run(host='0.0.0.0', port=5000)