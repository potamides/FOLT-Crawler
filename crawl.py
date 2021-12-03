#!/usr/bin/env python
from os import makedirs
from os.path import join, isfile
from csv import DictWriter, DictReader
from utils import ParallelMerge
from snscrape.modules.twitter import TwitterSearchScraper

hashtagfile = "hashtags.txt"
excludefile = "exclude.txt"
read_exclude, write_exclude = True, True
outputdir = "mined-tweets"
languages = ["en", "fr", "de", "ar"]
dates = ["2020-03-01", "2021-09-01"]
region = "Europe"
count = 30

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
                try:
                    country = tweet.country
                except AttributeError:
                    country = "None"
            writer.writerow(dict(zip(fieldnames, [tweet.id, tweet.date, country, tweet.lang, tweet.content])))

def read_tweets(filename):
    with open(filename, newline='', encoding='utf-8') as csvfile:
        return list(DictReader(csvfile))

def read_excludefile(filename):
    ids = list()
    if isfile(filename):
        with open(filename, "rb") as f:
            for line in f:
                ids.append(int(line))
    return ids

def append_exclude(filename, ids):
        with open(filename, "a+b") as f:
            for id_ in ids:
                f.write(f"{id_}\n".encode())

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
    exclude_ids = read_excludefile(excludefile) if read_exclude else list()

    for hashtag in hashtags:
        scrapers.append(TwitterSearchScraper(query=" ".join(filter(None, [hashtag, since, until, langs, near, filter_retweets]))))

    try:
        with ParallelMerge(*[scraper.get_items() for scraper in scrapers]) as items:
            for tweet in items:
                if tweet.id not in exclude_ids and tweet.content not in unique_contents:
                    tweets.append(tweet)
                    unique_contents.add(tweet.content)
                    print(f"{len(tweets)} tweets mined in current run!" , end='\r')
                    if len(tweets) >= count:
                        break
    except KeyboardInterrupt:
        pass
    print()
    write_tweets(tweets, filename)
    if write_exclude:
        append_exclude(excludefile, [tweet.id for tweet in tweets])

    return tweets

if __name__ == "__main__":
    hashtags = read_hashtags(hashtagfile)
    #print("Pre-pandemic tweets:", len(crawl_tweets(hashtags, until=dates[0])))
    print("Pandemic tweets:", len(crawl_tweets(hashtags, since=dates[0], until=dates[1])))
