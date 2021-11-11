#!/usr/bin/env python
from os import makedirs
from os.path import join
from csv import DictWriter
from math import ceil
from snscrape.modules.twitter import TwitterSearchScraper

hashtagfile = "hashtags.txt"
outputdir = "mined-tweets"
languages = ["en", "fr", "de", "ar"]
dates = ["2020-03-01", "2021-09-01"]
count = 1000

def read_hashtags(filename):
    hashtags = list()
    with open(filename, "rb") as f:
        for line in f:
            hashtags.append(line.strip().decode())
    return hashtags

def write_tweets(tweets, filename):
    with open(filename, "w", newline='') as csv_file:
        fieldnames = ["id", "date", "lang", "content"]
        writer = DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for tweet in tweets:
            writer.writerow(dict(zip(fieldnames, [tweet.id, tweet.date, tweet.lang, tweet.content])))

def crawl_tweets(hashtags, since=None, until=None):
    assert since is not None or until is not None
    makedirs(outputdir, exist_ok=True)

    since = f"since:{since}" if since else None
    until = f"until:{until}" if until else None
    langs = f"({' OR '.join(f'lang:{lang}' for lang in languages)})"
    filter_retweets = "exclude:nativeretweets exclude:retweets"

    filename = join(outputdir, "-".join(filter(None, [since, until])) + ".csv")
    tweets, unique_contents = list(), set()
    for hashtag in hashtags:
        mined = 0
        scraper = TwitterSearchScraper(query=" ".join(filter(None, [hashtag, since, until, langs, filter_retweets])))
        for tweet in scraper.get_items():
            if tweet.content not in unique_contents:
                mined += 1
                tweets.append(tweet)
                unique_contents.add(tweet.content)
                print(f"{len(tweets)} tweets mined in current run!" , end='\r')
                if mined >= ceil(count/len(hashtags)):
                    break
    print()
    write_tweets(tweets, filename)
    return tweets

hashtags = read_hashtags(hashtagfile)
print("Pre Covid-19 tweets:", len(crawl_tweets(hashtags, until=dates[0])))
print("Covid-19 tweets:", len(crawl_tweets(hashtags, since=dates[0], until=dates[1])))
