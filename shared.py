import re
import glob
from datetime import datetime, timezone

DATA_FOLDER = "wf5_full_name/"
RESSOURCES_FOLTER = "ressources/"
RAW_FOLDER = "raw_data/"
POST_SEPARATOR = "_END_OF_POST_PYSTOCK_"
DEBUG = True

subs = ["stocks", "investing", "wallstreetbets"]

# get date from fileName
def get_date(filename):
    date_pattern = re.compile("\d{4}\-\d{2}\-\d{2}")
    match = date_pattern.search(filename)
    if not match:
        print("get_date no match")
        return None
    date = match.group(0)
    date = datetime.strptime(date, '%Y-%m-%d')
    return date

def getFirstAndLastDate(pattern):
    files = glob.glob(pattern)
    dates = (get_date(file) for file in files)
    dates = set((d for d in dates if d is not None))
    first_date = str(min(dates)).split(" ")[0]
    last_date = str(max(dates)).split(" ")[0]
    return first_date, last_date

def debug(func):
    def wrapper_debug(*args, **kwargs):
        if (DEBUG):
            print("DEBUG : " + func.__name__)
        func(*args, **kwargs)
    return wrapper_debug