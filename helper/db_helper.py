from pymongo import MongoClient, DESCENDING, ASCENDING
# import constants

client = None
DB_NAME = "vikramk9852"
USER_COLLECTION_NAME = "users"
IMAGE_COLLECTION_NAME = "images"
DB_URL = "localhost"


def getDB():
    global client
    try:
        if client == None:
            client = MongoClient(host=DB_URL, port=27017)
        return client[DB_NAME]
    except Exception as e:
        raise e


def createIndex():
    try:
        db = getDB()
        imageCollection = db[USER_COLLECTION_NAME]
        return imageCollection.create_index("user")
    except Exception as e:
        raise e


def addUser(user):
    return insertUserMetaData(user)


def insertUserMetaData(user):
    try:
        db = getDB()
        userCollection = db[USER_COLLECTION_NAME]
        return userCollection.update_one(
            {"_id": user},
            {"$set": {
                "images": []
            }},
            upsert=True
        )
    except Exception as e:
        raise e


def insertTweets(user, tweets, latestTweetId):
    try:
        db = getDB()
        userCollection = db[USER_COLLECTION_NAME]
        imageCollection = db[IMAGE_COLLECTION_NAME]
        insertedImages = imageCollection.insert_many(tweets)
        return userCollection.update_one(
            {"_id": user},
            {
                "$push": {
                    "images": {"$each": insertedImages.inserted_ids}
                },
                "$set": {
                    "latestTweetId": str(latestTweetId)
                }
            }
        )
    except Exception as e:
        raise e


def doesUserExist(user):
    try:
        db = getDB()
        userCollection = db[USER_COLLECTION_NAME]
        return userCollection.find_one({"_id": user}, {"latestTweetId": 1})
    except Exception as e:
        raise e


def getAllUsers():
    try:
        db = getDB()
        userCollection = db[USER_COLLECTION_NAME]
        return [doc['_id'] for doc in userCollection.find({}, {"_id": 1}).sort("_id", ASCENDING)]
    except Exception as e:
        raise e


def getUserData(user, pageNo, orderBy, nPerPage):
    try:
        db = getDB()
        imageCollection = db[IMAGE_COLLECTION_NAME]

        if pageNo != None:
            pageNo = int(pageNo)
        else:
            pageNo = 1

        if nPerPage != None:
            nPerPage = int(nPerPage)
        else:
            nPerPage = 10

        if orderBy == None:
            orderBy = "tweet_id"

        data = imageCollection.find(
            {"user": user}
        ).skip(
            (pageNo-1)*nPerPage
        ).limit(
            nPerPage
        ).sort(
            orderBy, DESCENDING
        )
        return [doc for doc in data]
    except Exception as e:
        raise e
