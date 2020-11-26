import time
import praw
import json
import time
import glob
import re
import pandas as pd
from os import listdir
from words import wordFreq
from datetime import datetime, timezone
from reddit_trend import save_wf_from_raw

import shared

RAW_FOLDER = shared.RAW_FOLDER
POST_SEPARATOR = shared.POST_SEPARATOR

subs = ["stocks", "investing", "wallstreetbets"]
date_pattern = re.compile("g_(.+)\.")

def saveToFile(name, content):
    print("saved")
    text_file = open(RAW_FOLDER + name + ".txt", "w")
    text_file.write(content)
    text_file.close()

def scrapDate(sub, date):
    print("scrapping date : " + str(date) + " in sub : " + sub)
    credentials = json.load(open("credentials.json"))
    reddit = praw.Reddit(
        client_id=credentials["client_id"],
        client_secret=credentials["client_secret"],
        username=credentials["username"],
        password=credentials["password"],
        user_agent=credentials["user_agent"],
    )
    print("  processing " + sub)
    subreddit = reddit.subreddit(sub)
    new_sub = subreddit.new(limit=1000)
    dayContent = ""

    for submission in new_sub:
        postDate = str(datetime.fromtimestamp(submission.created_utc)).split(" ")[0]
        if (postDate == date):
            postContent = submission.title + " " + submission.selftext + POST_SEPARATOR
            dayContent = dayContent + " " + postContent

    saveToFile(sub + "_" + date, dayContent)

# scrap data from every posts possible (1000 max)
def scrappAll(sub):
    credentials = json.load(open("credentials.json"))
    reddit = praw.Reddit(
        client_id=credentials["client_id"],
        client_secret=credentials["client_secret"],
        username=credentials["username"],
        password=credentials["password"],
        user_agent=credentials["user_agent"],
    )
    print("  processing " + sub)
    subreddit = reddit.subreddit(sub)
    new_sub = subreddit.new(limit=500)

    i = 0
    dayContent = ""
    currentPostDate = None  # first date, fix : x = list(new_sub)[0]

    for submission in new_sub:
        postDate = str(datetime.fromtimestamp(submission.created_utc)).split(" ")[0]
        if (i == 0):
            currentPostDate = postDate
        print(i)
        postContent = submission.title + " " + submission.selftext + POST_SEPARATOR

        if (postDate != currentPostDate):
            saveToFile(sub + "_" + currentPostDate, dayContent)
            currentPostDate = postDate
            dayContent = postContent
        else:
            dayContent = dayContent + " " + postContent
            
        time.sleep(0.05)
        i += 1
    saveToFile(sub + "_" + currentPostDate, dayContent)


# either scrap all days or 1 date only
def scrap(sub, date=None):
    if date:
        scrapDate(sub, date)
    else:
        scrappAll(sub)

# get date from fileName
def get_date(filename):
    match = date_pattern.search(filename)
    if not match:
        return None
    date = match.group(1)
    date = datetime.strptime(date, '%Y-%m-%d')
    return date

# scrap data from unprocessed days in /raw, and save the stats into json in /wf
def scrapMissing():
    files = glob.glob("raw_data/investing*.txt")
    dates = (get_date(file) for file in files)
    dates = (d for d in dates if d is not None)
    last_date = max(dates)
    today = datetime.today()
    dates = pd.date_range(start=last_date, end=today).tolist()
    dates = dates[1:]  # unprocessed dates
    if (len(dates) == 0):
        return
    start = dates[0]
    end = dates[-1]
    for date in dates:
        date = str(date).split(" ")[0]
        for sub in subs:
            scrapDate(sub, date)
    save_wf_from_raw(start, end)
    

if __name__ == "__main__":
    # for sub in subs:
    #     scrap(sub, "2020-11-21")
    scrapMissing()

