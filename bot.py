import tweepy
import threading
import os
import json
import time
import dateutil.parser
import urllib.request
import logging
import helper.db_helper as db
from helper.twitter_helper import create_api

logger = logging.getLogger()


class TwitterWatcher(threading.Thread):

    def __init__(self, pause):
        super(TwitterWatcher, self).__init__()
        self._pause = pause
        self._stopping = False
        self.twitter_api = create_api()

    def run(self):
        while not self._stopping:
            users = db.getAllUsers()
            for userInfo in users:
                user = userInfo['_id']

                userExists = db.doesUserExist(user)
                if userExists != None:
                    latestTweetId = userExists['latestTweetId']
                    tweets = self.twitter_api.user_timeline(
                        id=user, count=200, since_id=int(latestTweetId), tweet_mode="extended", trim_user=True)
                else:
                    db.insertUserMetaData(user)
                    latestTweetId = 0
                    tweets = self.twitter_api.user_timeline(
                        id=user, count=200, tweet_mode="extended", trim_user=True)

                length = 0
                created_at = ""
                tweets.reverse()
                tweets_len = len(tweets)
                logger.info(f"{tweets_len} Tweets to write for user {user}")
                tweetObjs = []

                for tweet in tweets:
                    length += 1
                    tweet = tweet._json
                    tweet_id = tweet['id_str']

                    if 'media' not in tweet['entities']:
                        continue
                    logger.info(
                        f"{length}, writing ({user}/images/{tweet_id})")

                    tweet_media_info = tweet['extended_entities']['media']
                    media_urls = []

                    for media in tweet_media_info:
                        media_urls.append(media['media_url_https'])

                    if len(media_urls) == 0:
                        continue
                    created_at = dateutil.parser.parse(
                        tweet['created_at']).timestamp()

                    tweetObjs.append({
                        "_id": tweet_id,
                        "tweet_id": tweet_id,
                        "tweet_media_url": media_urls,
                        "created_at": created_at,
                        "tweet_url": "https://twitter.com/"+user+"/status/"+tweet_id,
                        "tweet_text": tweet['full_text'],
                        "user": user
                    })
                    latestTweetId = max(int(latestTweetId), tweet['id'])

                logger.info(f"latestTweetId {latestTweetId} for user {user}")

                if len(tweets) > 0 and latestTweetId != 0:
                    db.insertTweets(user, tweetObjs, latestTweetId)

            logger.info("done")
            time.sleep(self._pause)

    def stop(self):
        self._stopping = True
