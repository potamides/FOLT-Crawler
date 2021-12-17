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

if __name__ == "__main__":
    for file in argv[1:]:
        print(f"Checking file {file}...")
        has_id, has_label = False, False
        for idx, row in enumerate(read_tweets(file)):
            try:
                if "id" in row.keys():
                    has_id = True
                if "label" in row.keys():
                    has_label = True
                assert row["id"].isnumeric() if "id" in row.keys() else True
                assert is_date(row["date"])
                assert row["lang"] in languages
                assert row["label"].isnumeric() if "label" in row.keys() else True
                assert type(row["country"]) == type(row["content"]) == str
            except Exception as e:
                print(idx, row)
                raise e
        if not has_id:
            print("File has no id column!")
        if not has_label:
            print("File has no label column!")
