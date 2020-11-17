import time
import praw
import json
import time
from words import wordFreq
from datetime import datetime, timezone


RAW_FOLDER = "raw_data/"
POST_SEPARATOR = "_END_OF_POST_PYSTOCK_"

def saveToFile(name, content):
    print("saved")
    text_file = open(RAW_FOLDER + name + ".txt", "w")
    text_file.write(content)
    text_file.close()

def scrapDate(sub, date):
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
    new_sub = subreddit.new(limit=1000)

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


def scrap(sub, date=None):
    if date:
        scrapDate(sub, date)
    else:
        scrappAll(sub)

if __name__ == "__main__":
    subs = ["stocks", "investing", "wallstreetbets"]
    for sub in subs:
        scrap(sub, "2020-11-17")

