import os
import json
import firebase_admin
from firebase_admin import credentials, firestore, auth


def initFirebase():

    dirname = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(dirname, '../config.json')) as f:
        config_cloudstore = json.load(f)

    cred = credentials.Certificate(config_cloudstore)
    return firebase_admin.initialize_app(cred)

def getFirestoreDB():
    if firebase_admin._apps:
        return firestore.client()
    initFirebase()
    return firestore.client()

def getFirebaseAuth():
    if firebase_admin._apps:
        return auth
    initFirebase()
    return auth