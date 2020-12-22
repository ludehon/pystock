import re
import glob
from datetime import datetime, timezone

DATA_FOLDER = "wf4/"
RESSOURCES_FOLTER = "ressources/"
RAW_FOLDER = "raw_data/"
POST_SEPARATOR = "_END_OF_POST_PYSTOCK_"

subs = ["stocks", "investing", "wallstreetbets"]

# get date from fileName
def get_date(filename):
    date_pattern = re.compile("g_(.+)\.")
    match = date_pattern.search(filename)
    if not match:
        return None
    date = match.group(1)
    date = datetime.strptime(date, '%Y-%m-%d')
    return date

def getFirstAndLastDate(pattern):
    files = glob.glob(pattern)
    dates = (get_date(file) for file in files)
    dates = set((d for d in dates if d is not None))
    first_date = str(min(dates)).split(" ")[0]
    last_date = str(max(dates)).split(" ")[0]
    return first_date, last_date