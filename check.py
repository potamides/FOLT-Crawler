#!/usr/bin/env python
from crawl import languages, read_tweets
from dateutil.parser import parse
from sys import argv

def is_date(string, fuzzy=False):
    try:
        parse(string, fuzzy=fuzzy)
        return True
    except ValueError:
        return False

for file in argv[1:]:
    print(f"Checking file {file}...")
    for idx, row in enumerate(read_tweets(file)):
        try:
            assert row["id"].isnumeric()
            assert is_date(row["date"])
            assert row["lang"] in languages
            assert row["label"].isnumeric() if "label" in row.keys() else True
            assert type(row["country"]) == type(row["content"]) == str
        except Exception as e:
            print(idx, row)
            raise e
