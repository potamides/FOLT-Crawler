#!/usr/bin/env python
import tweepy
import os
import csv

hashtagfile = "hashtags.txt"
tweetsfile = "tweets.csv"
consumer_key = os.getenv("CONSUMER_KEY") or input("Twitter API key: ")
consumer_secret = os.getenv("CONSUMER_SECRET") or input("Twitter API secret: ")

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

def read_hashtags(filename):
    hashtags = list()
    with open(filename, "rb") as f:
        for line in f:
            hashtags.append(line.strip().decode())
    return hashtags

def crawl_tweets(hashtags):
    tweets, instances = list(), set()

    for hashtag in hashtags:
        for tweet in api.search_tweets(q=hashtag, lang="en", count=100, tweet_mode="extended"):
            try:
                if tweet.retweeted_status.full_text not in instances:
                    tweets.append((tweet.created_at, tweet.retweeted_status.full_text))
                    instances.add(tweet.retweeted_status.full_text)
            except AttributeError:  # Not a Retweet
                if tweet.full_text not in instances:
                    tweets.append((tweet.created_at, tweet.full_text))
                    instances.add(tweet.full_text)
    with open(tweetsfile, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        for date, text in tweets:
            csvwriter.writerow([date, text])
    return tweets

hashtags = read_hashtags(hashtagfile)
tweets = crawl_tweets(hashtags)
