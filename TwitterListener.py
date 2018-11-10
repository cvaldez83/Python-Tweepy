# YouTube Video: https://www.youtube.com/watch?v=WX0MDddgpA4
# Github: https://github.com/vprusso/youtube_tutorials/tree/master/twitter_python/part_3_analyzing_tweet_data

from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import time
import numpy as np
import pandas as pd
import json

from keys import keys
import script


# # # TWITTER CLIENT # # # #
class TwitterClient():
    def __init__(self, twitter_user=None): #default to none, which will default to my own account
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)
        self.twitter_user = twitter_user
        
    def get_twitter_client_api(self):
        return self.twitter_client

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets
    
    def get_friend_list(self,num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends): #.friends & .items are API calls
            friend_list.append(friend)
        return friend_list
    
    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets): #.home_timeline & .items are API calls
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets


# # # TWITTER AUTHENTICATER # # #
class TwitterAuthenticator():
    def authenticate_twitter_app(self):
        auth = OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
        auth.set_access_token(keys['access_token'], keys['access_token_secret'])
        return auth

# # # TWITTER STREAMER # # # #
class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    """
    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()

    def stream_tweets(self, fetched_tweets_filename, follow_list):
        # This handles Twitter authetification and the connection to Twitter Streaming API
        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_authenticator.authenticate_twitter_app()
        stream = Stream(auth, listener)

        # This line filter Twitter Streams to capture data by the keywords: 
        stream.filter(follow=follow_list)
        # stream.filter(track=hash_tag_list)

# # # ON_DATA ACTIONS # # #
class TweetReader():
    print('starting class TweetReader')
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def get_username(self):
        print('def get_username')
        with open(fetched_tweets_filename,"r") as read_file:
            data = json.load(read_file)
        print('type isssss: ' + str(type(data)))
        username = '@'+str(data["user"]["screen_name"])
        # print(username)
        return username
        # d=json.loads(data)
        # d = self.d
        # self.username = '@'+str(d["user"]["screen_name"])
        # print('self.username: ' + self.username)
        # return self.username

    # def get_text(self):
    #     # d=json.loads(data)
    #     d = self.d
    #     self.text = d["text"]
    #     print('self.text: ' + self.text)
    #     return self.text

        # print('printing all data: ' + data)
        # print('data type is: ' + str(type(data))+ 'converting to dictionary')
        # #convert json data to dictionary d
        # d=json.loads(data)
        # print('~~~~~~~~~~~~~~~~~')
        # print('printing all json data: '+ str(d))
        # print('received tweet text: ' + str(d["text"]))
        # print('received tweet screen name: ' + str(d["user"]["screen_name"]))


# # # TWITTER STREAM LISTENER # # #
class TwitterListener(StreamListener):
    """
    This is a basic listener that just prints received tweets to TwitterListener.
    """
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename
    
    def on_data(self,data):
        try:
        #NTS: raw data type is a string
            print('tweet received: '+ time.time())
            with open(self.fetched_tweets_filename, 'w') as tf:
                tf.write(data)

            # print('tweet_info.get_username: ' + str(tweet_info.get_username))
            # script.CallCharlie()
            return True

        except BaseException as e:
            print("Error on_data %s" % str(e))
        return True
    
    def on_error(self,status):
        if status == 420:
            # Returning False on_data method to in case rate limit occurs
            return False
        print(status)
        
class TweetAnalyzer():
    """
    Functionality for analyzing and categorizing content from tweets
    """
    def tweets_to_data_frame(self, tweets):

        #obtain list of text from tweets
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['tweets'])
        
        #obtain list of IDs from tweets and use 'id' as column header
        df['id'] = np.array([tweet.id for tweet in tweets])
        #similarly, create list of other attributes
        df['len'] = np.array([len(tweet.text) for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['source'] = np.array([tweet.source for tweet in tweets])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])
        return df

# # # 
# class CallCharlie():
#     def __init__(self):
#         print('calling charlie!')

if __name__ == '__main__':

    # # # inputs # # #
    fetched_tweets_filename = "tweets.json"
    follow_list = ['1059557863775850496'] #treats4charlie user id
    
    # # # create TwitterStreamer() object (((WORKS)))
    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(fetched_tweets_filename, follow_list)

    # # # # read tweet from tweets.json
    # tweet_reader = TweetReader(fetched_tweets_filename)
    # username = tweet_reader.get_username()
    # print(username)


    # with open("json.json","r") as read_file:
    #     print(type(read_file))
    #     data = json.load(read_file)
        
    

    # tweet_info = TweetInfo(data)

    # #send response tweet
    # message = 'hellooooo auto response from python!'
    # cliente = TwitterClient()
    # cliente.twitter_client.update_status(username + ' ' + message)


    
