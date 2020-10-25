import os
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


def initFirestoreDB():

    dirname = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(dirname, '../config.json')) as f:
        config_cloudstore = json.load(f)

    cred = credentials.Certificate(config_cloudstore)
    firebase_admin.initialize_app(cred)
    return firestore.client()

def getFirestoreDB():
    if firebase_admin._apps:
        return firestore.client()
    return initFirestoreDB()
