import os
import cPickle
from collections import defaultdict
from pymongo import Connection

def upsert(dict1, dict2):
    for key, value in dict2.items():
        if dict1.get(key):
            dict1[key] += dict2[key]
        else:
            dict1[key] = dict2[key]

def gather_result(path):
    con = Connection("localhost")
    db = con.domain
    periods = [("minutely", "%y-%m-%d %H:%M"), ("hourly", "%y-%m-%d %H"),
               ("daily", "%y-%m-%d"),
               ("weekly","%y-%W"),
               ("monthly","%y-%m"),
               ("yearly", "%y")]

    collection = defaultdict(int)
    for period, format in periods:
        collection[period] = {}

    results = map(lambda f: cPickle.load(open(path + "/" + f)), os.listdir(path))

    for result in results:
        for period, format in periods:
            upsert(collection[period], result[period])

    for period, format in periods:
        for key, count in collection[period].items():
            date, domain = key.split("#")
            db.minutely.update({"domain":domain, "date": date}, {"$inc": {"count" : count}}, upsert=True)

