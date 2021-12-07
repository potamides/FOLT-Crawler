# FOLT-Crawler
Twitter crawler for the FOLT 2021 shared task.

## Usage
First, install required packages.
```python
pip install -r requirements.txt
```
If you want to mine tweets run `crawl.py`. Check the first few lines of the
file for settings. Functionality for excluding tweets can be toggled with the
boolean variables `read_exclude` and `write_exclude`.
```python
./crawl.py
```
To check the integrity of a csv files with tweets use `check.py`. Files that
should be checked should be specified as command line arguments.
```python
./check.py <file1.csv> <file2.csv>
```
If you want to shuffle a file with tweets and optionally concatenate multiple
files, you can use `shufcat.py`. The last file specified as a command line
argument is used as the output file. All files before that are used as input.
The contents of these files are read, then concatenated, and finally shuffled.
```python
./shufcat.py <input1.csv> <input2.csv> [...] <inputN.csv> <output.csv>
```
For grading the submission of a student for task 4 of the Shared Task, use
`grade.py`. It requires the `gold.csv` file with the 30 gold labeled tweets (as
rows `id,date,country,lang,content,label`), the shuffled `shuffled.csv` file
with the 60 unlabeled tweets (as rows `id,date,country,lang,content`), and the
`predictions.txt` file which should simply contain one prediction of the
student per line. The exact filenames should be supplied as command line
arguments. When run Cohen's Kappa is printed to stdout.
```python
./grade.py <gold.csv> <shuffled.csv> <predictions.txt>
```
