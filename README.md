# FOLT-Crawler
Twitter crawler for the FOLT 2021 shared task. Reads a file with search terms
seperated by newline and writes 100 tweets per search term into a csv file.
Before this can be used one must register a [Twitter
Application](https://developer.twitter.com/en/portal/projects-and-apps) to
obtain required API secrets.

## Usage
```python
pip install -r requirements.txt
./crawl.py
```
