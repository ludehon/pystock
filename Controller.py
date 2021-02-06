import View
# import Model
from words import wordFreq, TopViz

class Controller:
    def __init__(self):
        pass
    
    def vizu():
        pass
    
    def scrap_all():
        pass
    
    # transform raw txt files to dict files, addWords() remove useless words and keeps compay first name
    # startDate, endDate : str (YYYY-MM-DD)
    def save_wf_from_raw(startDate, endDate):
        dates = pd.date_range(start=startDate, end=endDate).tolist()
        subs = shared.subs
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