# split the string to only keep the date
def find_date(file):
    date = file.split("\\")[1].split("_")[0]
    return date
