import datetime
import os
def round_num_by(n):
    def inner(a):
        return (a / n) * n
    return inner

def round_minutes_by(n):
    round_num_by_n = round_num_by(n)
    def inner(date):
        return datetime.datetime(date.year, date.month, date.day, date.hour, round_num_by_n(date.minute))
    return inner

def ensure_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def upsert(dict1, dict2):
    for key, value in dict2.items():
        if dict1.get(key):
            dict1[key] += dict2[key]
        else:
            dict1[key] = dict2[key]

