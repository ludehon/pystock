# pystock
main in reddit_trend.py, tests in words.py

## Dependencies
- pandas
- numpy
- praw
- nltk

## Trello
https://trello.com/b/M3uJcQ1x/project-pystock

## Example
<img src="https://github.com/ludehon/pystock/blob/main/ressources/inter2_08_4top.png" width="600" />

## Usage
### python reddit_trend.py raw
Parse data from raw files into word frequency dictionaries in "wf" folder.

### python reddit_trend.py vizu
Vizualize the stocks price evolution. Selected stocks are the most discussed from the last 7 days.

### python reddit_trend.py top
Vizualize top discussed stocks in terminal.

### python scrap_all.py
Download data from the last 1000 reddit posts. Store raw files, detect missing dates, and clean raw data to wf folder.

### Unit tests
pytest -q tests.py
