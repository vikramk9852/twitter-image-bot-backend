import tweepy
import threading
import os
import json
import time
import dateutil.parser
import urllib.request
import logging

from helper.firebase_helper import getFirestoreDB
from helper.twitter_helper import create_api

logger = logging.getLogger()

class TwitterHandleWatcher(threading.Thread):

    def __init__(self, pause):
        super(TwitterHandleWatcher, self).__init__()
        self._pause = pause
        self._stopping = False
        self.twitter_api = create_api()
        self.cloudstore_db = getFirestoreDB()

    def getHandles(self):
        return self.cloudstore_db.collection(u'tHandles').stream()

    def run(self):
        while not self._stopping:
            tHandles = self.getHandles()
            for handleInfo in tHandles:
                user = handleInfo.id
                firebase_url_prefix = 'tHandles/'+user
                metainfo = self.cloudstore_db.document(
                    f'{firebase_url_prefix}').get().to_dict()
                if metainfo != None and "latestTweetId" in metainfo:
                    latestTweetId = metainfo['latestTweetId']
                    tweets = self.twitter_api.user_timeline(
                        id=user, count=200, since_id=int(latestTweetId), tweet_mode="extended", trim_user=True)
                else:
                    logger.info(f"{user}")
                    latestTweetId = 0
                    tweets = self.twitter_api.user_timeline(id=user, count=200, tweet_mode="extended", trim_user=True)

                length = 0
                created_at = ""
                tweets.reverse()
                tweets_len = len(tweets)
                logger.info(f"{tweets_len} Tweets to write for tHandle {user}")
                db_batch = self.cloudstore_db.batch()

                for tweet in tweets:
                    length += 1
                    tweet = tweet._json
                    tweet_id = tweet['id_str']

                    if 'media' not in tweet['entities']:
                        continue
                    logger.info(
                        f"{length}, writing ({firebase_url_prefix}/images/{tweet_id})")

                    tweet_media_info = tweet['extended_entities']['media']
                    media_urls = []

                    for media in tweet_media_info:
                        media_urls.append(media['media_url_https'])
                        
                    if len(media_urls) == 0:
                        continue
                    created_at = dateutil.parser.parse(
                        tweet['created_at']).timestamp()

                    doc_ref = self.cloudstore_db.document(
                        f'{firebase_url_prefix}/images/{tweet_id}')
                    db_batch.set(doc_ref, {
                        "tweet_id": tweet_id,
                        "tweet_media_url": media_urls,
                        "created_at": created_at,
                        "tweet_url": "https://twitter.com/"+user+"/status/"+tweet_id,
                        "tweet_text": tweet['full_text'],
                        "firebase_media_url": ""
                    })
                    latestTweetId = max(int(latestTweetId), tweet['id'])

                logger.info(f"latestTweetId {latestTweetId}")

                if len(tweets) > 0 and latestTweetId != 0:
                    metainfo_ref = self.cloudstore_db.document(
                        f'{firebase_url_prefix}')
                    if metainfo != None:
                        db_batch.update(
                            metainfo_ref, {u'latestTweetId': str(latestTweetId)})
                    else:
                        db_batch.set(metainfo_ref, {
                                     u'latestTweetId': str(latestTweetId)})
                    db_batch.commit()

            logger.info("done")
            time.sleep(self._pause)

    def stop(self):
        self._stopping = True
