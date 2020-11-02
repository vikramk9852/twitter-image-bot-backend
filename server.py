import json
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from helper.twitter_helper import create_api
from helper.firebase_helper import getFirebaseAuth
from firebase_admin import firestore
from flask_cors import CORS, cross_origin
import helper.db_helper as db

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
        response.append(
            {
                'name': user._json["name"],
                'screen_name': user._json["screen_name"]
            }
        )
    return jsonify({"data": response}), 200


@app.route('/addUser', methods=['POST'])
def addUser():
    requestData = request.get_json()
    user = requestData['user']
    authToken = request.headers.get('authToken')

    try:
        auth = getFirebaseAuth()
        auth.verify_id_token(authToken)

        db.addUser(user)
        return jsonify({"data": "success"}), 200
    except Exception as e:
        print(e)
        return jsonify({"data": "Invalid auth token, make sure you are logged in"}), 500


@app.route('/getAllUsers', methods=['GET'])
@cross_origin()
def getAllUsers():
    try:
        users = db.getAllUsers()
        return jsonify({"data": users}), 200
    except Exception as e:
        print(e)
        return jsonify({"data": "Some error occured"}), 500


@app.route('/getUserData', methods=['GET'])
@cross_origin()
def getUserData():

    user = request.args.get('user')
    pageNo = request.args.get('pageNo')
    nPerPage = request.args.get('nPerPage')
    orderBy = request.args.get('orderBy')
    try:
        data = db.getUserData(user, pageNo, orderBy, nPerPage)
        return jsonify({"data": data}), 200
    except Exception as e:
        print(e)
        return jsonify({"data": "Some error occured"}), 500


if __name__ == "__main__":
    app.run(port=5000)


# def initServer():
#     app.run(debug=True)
