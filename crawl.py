#!/usr/bin/env python
from os import makedirs
from os.path import join
from csv import DictWriter
from utils import ParallelMerge
from snscrape.modules.twitter import TwitterSearchScraper

hashtagfile = "hashtags.txt"
outputdir = "mined-tweets"
languages = ["en", "fr", "de", "ar"]
dates = ["2020-03-01", "2021-09-01"]
region = "Europe"
count = 1000

def read_hashtags(filename):
    hashtags = list()
    with open(filename, "rb") as f:
        for line in f:
            hashtags.append(line.strip().decode())
    return hashtags

def write_tweets(tweets, filename):
    with open(filename, "w", newline='', encoding='utf-8') as csv_file:
        fieldnames = ["id", "date", "country", "lang", "content"]
        writer = DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for tweet in tweets:
            try:
                country = tweet.place.country
            except AttributeError:
                country = "None"
            writer.writerow(dict(zip(fieldnames, [tweet.id, tweet.date, country, tweet.lang, tweet.content])))

def crawl_tweets(hashtags, since=None, until=None):
    assert since is not None or until is not None
    makedirs(outputdir, exist_ok=True)

    since = f"since:{since}" if since else None
    until = f"until:{until}" if until else None
    langs = f"({' OR '.join(f'lang:{lang}' for lang in languages)})"
    near = f"near:{region}"
    filter_retweets = "exclude:nativeretweets exclude:retweets"

    filename = join(outputdir, "-".join(filter(None, [since, until])).replace(":", "-") + ".csv")
    scrapers, tweets, unique_contents = list(), list(), set()

    for hashtag in hashtags:
        scrapers.append(TwitterSearchScraper(query=" ".join(filter(None, [hashtag, since, until, langs, near, filter_retweets]))))

    try:
        with ParallelMerge(*[scraper.get_items() for scraper in scrapers]) as items:
            for tweet in items:
                if tweet.content not in unique_contents:
                    tweets.append(tweet)
                    unique_contents.add(tweet.content)
                    print(f"{len(tweets)} tweets mined in current run!" , end='\r')
                    if len(tweets) >= count:
                        break
    except KeyboardInterrupt:
        pass
    print()
    write_tweets(tweets, filename)
    return tweets

if __name__ == "__main__":
    hashtags = read_hashtags(hashtagfile)
    print("Pre-pandemic tweets:", len(crawl_tweets(hashtags, until=dates[0])))
    print("Pandemic tweets:", len(crawl_tweets(hashtags, since=dates[0], until=dates[1])))
