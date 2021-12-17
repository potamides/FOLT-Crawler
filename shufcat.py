#!/usr/bin/env python
from crawl import read_tweets, write_tweets
from random import shuffle
from sys import argv

class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

input_, output = argv[1:-1], argv[-1]

if __name__ == "__main__":
    tweets = list()
    for file in input_:
        tweets.extend(read_tweets(file))
    shuffle(tweets)
    write_tweets([AttrDict(tweet) for tweet in tweets], output)
