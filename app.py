import json
import logging
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from helper.twitter_helper import create_api
from helper.firebase_helper import getFirestoreDB

# creating the flask app
app = Flask(__name__)
# creating an API object

logger = logging.getLogger()


@app.route('/search/<username>', methods=['GET'])
def search_users(username):
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
    print(requestData)
    
    try:
        twitterApi.get_user(requestData["handle"])
        documentPath = 'tHandles/'+requestData["handle"]
        db = getFirestoreDB()
        db.document(documentPath).set({})
        return jsonify({"data": "success"}), 200
    except Exception as e:
        print(e)
        return jsonify({"data": "Some error occured"}), 500


if __name__ == "__main__":
    app.run(debug=True)