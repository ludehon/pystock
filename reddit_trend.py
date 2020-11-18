import time
import praw
import json
import pandas as pd
from words import wordFreq
from datetime import datetime, timezone

def date_generator(month, year="2020"):
    li = []
    for i in range(31):
        li.append(year + "-" + month + "-" + str(i + 1).zfill(2))
    return li


def get_wf_from_sub(subs, limit, nowDate=None):
    print("date : " + nowDate)
    if nowDate == None:
        nowDate = str(
            datetime.fromtimestamp(
                datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()
            )
        ).split(" ")[0]

    wf = wordFreq()
    # wf.clean_csv("amex.csv")
    credentials = json.load(open("credentials.json"))
    reddit = praw.Reddit(
        client_id=credentials["client_id"],
        client_secret=credentials["client_secret"],
        username=credentials["username"],
        password=credentials["password"],
        user_agent=credentials["user_agent"],
    )

    for sub in subs:
        print("  processing " + sub)
        subreddit = reddit.subreddit(sub)
        new_sub = subreddit.new(limit=limit)
        i = 1
        for submission in new_sub:
            if (i * 0.1) % 10 == 0:  # todo : fix
                print(i * 0.1, "%")
            i += 1
            postDate = str(datetime.fromtimestamp(submission.created_utc))
            if nowDate in postDate:
                li = submission.title + " " + submission.selftext
                wf.addWords(li)
    return wf


# save word occurence from raw files to dict files
# startDate, endDate : str (YYYY-MM-DD)
def save_wf_from_raw(startDate, endDate):
    dates = pd.date_range(start=startDate, end=endDate).tolist()
    subs = ["stocks", "investing", "wallstreetbets"]
    for date in dates:
        date = str(date).split(" ")[0]
        wf = wordFreq()
        for sub in subs:
            with open("raw_data/" + sub + "_" + date + ".txt") as f:
                content = f.read()
                posts = content.split("_END_OF_POST_PYSTOCK_")
                for post in posts:
                    wf.addWords(post)
        wf.saveToFile(date)


if __name__ == "__main__":
    # mode 1 : scrap data from reddit and save it
    # mode 2 : display word occurence over time
    # mode 3 : scrap data from raw data
    mode = 2
    if mode == 1:
        dates = date_generator("10")
        dates = ["2020-11-15"]
        subs = ["stocks", "investing", "wallstreetbets"]

        for date in dates:
            wf = get_wf_from_sub(
                subs, 100, date
            )  # 1000 posts = 1 month back in time, 1000 max
            wf.saveToFile(date)
    elif mode == 2:
        wf = wordFreq()
        toExclude = []
        toLookAt = []
        wf.displayTimeSerie(10, toExclude, toLookAt)
    elif mode == 3:
        save_wf_from_raw("2020-11-13", "2020-11-18")
