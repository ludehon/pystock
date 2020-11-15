import string
import collections
import pandas
import json
import os
import glob
from nltk.corpus import stopwords
from datetime import datetime, timezone
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

DATA_FOLDER = "wf2/"
RESSOURCES_FOLTER = "ressources/"

def clean_string(content):
    content = content.translate(str.maketrans("", "", string.punctuation))
    return content


# rate = {0, 1}, data = list
def lowPassFilter(data, rate):
    tmp_data = data[0]
    filter_data = []
    filter_data.append(tmp_data)
    for i in range(1, len(data)):
        tmp_data = tmp_data * rate + data[i] * (1.0 - rate)
        filter_data.append(tmp_data)
    return filter_data


def smoothDF(df):
    # nans = np.where(np.empty_like(df.values), np.nan, np.nan)
    # data = np.hstack([nans, df.values]).reshape(-1, df.shape[1])
    # df = pd.DataFrame(data, columns=df.columns)
    # df = df.interpolate(method='spline', order=1)
    for col in df:
        li = df[col].to_list()
        li = lowPassFilter(li, 0.8)
        df[col] = li
    return df


class wordFreq:
    def __init__(self):
        self.count = dict()
        self.nameMap = dict()
        self.filter = set()
        with open(RESSOURCES_FOLTER + "top_en.txt") as f:
            lines = f.read().splitlines()
        self.stopWords = set(stopwords.words("english")).union(set(lines))
        self.loadFilter(RESSOURCES_FOLTER + "cleaned_nasdaq.csv")
        self.loadFilter(RESSOURCES_FOLTER + "cleaned_nyse.csv")
        self.loadFilter(RESSOURCES_FOLTER + "cleaned_amex.csv")

    def loadFilter(self, filterFile):
        df = pandas.read_csv(filterFile)
        df["First_name"] = df.Name.str.split().str[0]

        ticker_map = df[["Symbol", "First_name"]].set_index("Symbol").T.to_dict('list')
        first_name_map = df[["Name", "First_name"]].set_index("Name").T.to_dict('list')
        self.nameMap = {**ticker_map, **first_name_map}

        self.filter = self.filter.union(
            set(df["First_name"].str.lower().tolist())
        )


    # return set of words from content
    # remove punctuation
    # replace ticker and full company name by the first name
    # lower case
    # keep only company names
    # content : str
    def processContent(self, content):
        content = clean_string(content)
        for key, value in self.nameMap.items():
            content = content.replace(key, value[0])
        content = content.lower().split()
        content = self.filterWords(content)
        return set(content)

    # content : str
    def addWords(self, content):
        words = self.processContent(content)
        for word in words:
            if word in self.count:
                self.count[word] += 1
            else:
                self.count[word] = 1

    # keep words in li that belong to self.filter and remove those that are in self.stopWords
    # li  : list[str]
    def filterWords(self, li):
        li = [x for x in li if x in self.filter]
        li = [x for x in li if x not in self.stopWords]
        return li

    def getCount(self):
        return self.count

    # return list with top words from json files
    # size : int
    def loadTop(self, size):
        stats = collections.Counter()
        files = glob.glob(DATA_FOLDER + "*json")
        files.sort(key=os.path.getmtime)
        for file in files:
            freq = json.load(open(file))
            stats += collections.Counter(freq)
        df = pd.DataFrame.from_dict(stats, orient="index").reset_index()
        df = df.rename(columns={"index": "word", 0: "count"})
        df = df.sort_values("count", ascending=False)
        df = df.head(size)
        top = df["word"].tolist()
        return top

    # refturn dataframe with word occurence from json files for every date
    # tops : list[str]
    def loadStats(self, tops):
        freqs = []
        dates = []
        files = glob.glob(DATA_FOLDER + "*json")
        files.sort(key=os.path.getmtime)
        for file in files:
            date = file.split("/")[1].split("_")[0]
            dates.append(date)
            freq = json.load(open(file))
            freq = {
                top: freq[top] for top in tops if top in freq.keys()
            }  # filter freq dictionary only with top word
            freqs.append(freq)
        df = pd.DataFrame(freqs, index=[dates]).fillna(0)
        df = df.groupby(df.index).sum()
        return df

    # display word occurence by day (n=size)
    # size : int, toExclude : list[str]
    def displayTimeSerie(self, size, toExclude=[]):
        top = self.loadTop(size)
        df = self.loadStats(top)
        df = df.drop(toExclude, axis=1)
        df = smoothDF(df)
        ax = df.plot.line()
        ax.set_title("Word trend by day " + str(size) + "/")
        ax.set_ylabel("occurence")
        plt.show()

    # remove unecessary columns and words
    # fileName : str
    def clean_csv(self, fileName):
        stops = ["inc", "corp", "corporation", "ltd", "etf", "nasdaq", "dow"]
        data = pandas.read_csv(fileName)
        data["Name"] = data["Name"].apply(
            lambda x: x.strip().lower() if x else None
        )  # lower
        data["Name"] = data["Name"].str.replace("[^\w\s]", "")  # remove punctuation
        f = lambda x: " ".join(w for w in x.split() if not w in stops)
        data["Name"] = data["Name"].apply(f)  # remove companies stop words
        data = data[["Symbol", "Name"]]
        newName = "cleaned_" + fileName
        data.to_csv(newName)

    # save word occurence to file
    # date : str
    def saveToFile(self, date=None):
        if date == None:
            date = str(datetime.utcnow()).split(" ")[0]
        json.dump(self.count, open("wf2/" + date + "_word_frequency" + ".json", "w"))

    def loadFromFile(self, date):
        self.count = json.load(open(date + "_word_frequency.json"))


class test_wordFreq:
    def __init__(self):
        self.wf = wordFreq()

    def test_count(self):
        content = "\n\nTEST :\nthese are english words apple aapl  TESLA, micron mu: "
        print(content)
        self.wf.addWords(content)
        print(self.wf.getCount())
        # should be {'apple': 1, 'micron': 1, 'tesla': 1}


if __name__ == "__main__":
    tester = test_wordFreq()
    tester.test_count()
