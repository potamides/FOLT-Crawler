#!/usr/bin/env python
from sys import argv
from crawl import read_tweets
from sklearn.metrics import cohen_kappa_score

def read_submission(filename):
    predictions = list()
    with open(filename, "rb") as f:
        for line in f:
            predictions.append(int(line.strip()))
    return predictions

assert len(argv[1:]) == 3, "Only two arguments allowed!"
label_file, submission_file, prediction_file = argv[1], argv[2], argv[3]

id2labels = {tweet['id']:int(tweet['label']) for tweet in read_tweets(label_file)}
id2pred = {tweet['id']:pred for tweet, pred in zip(read_tweets(submission_file), read_submission(prediction_file))}

assert len(id2labels) == len(id2pred), "Amount of annotations differ!"
assert 0 <= min(id2pred.values()) <= max(id2pred.values()) <= 2, "Invalid category"

labels, predictions = list(), list()
for id_, pred in id2pred.items():
    if id_ in id2labels:
        labels.append(id2labels[id_])
        predictions.append(pred)

print(f"Cohen's kappa: {cohen_kappa_score(labels, predictions)}")
