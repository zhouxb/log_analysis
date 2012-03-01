import os
import cPickle
import dnslog
from collections import defaultdict
from pymongo import Connection

    #periods = dnslog.periods
    #formats = dnslog.formats

    #con = Connection("localhost")
    #db = con.domain

    #collection = defaultdict(int)
    #for period in periods:
        #collection[period] = {}

    #results = map(lambda f: cPickle.load(open(path + "/" + f)), os.listdir(path))

    #for result in results:
        #for period in periods:
            #upsert(collection[period], result[period])

    #for period, format in zip(periods, formats):
        #db[period].ensure_index("domain")
        #for key, count in collection[period].items():
            #date, domain = key.split("#")
            #db[period].update({"domain":domain, "date": date}, {"$inc": {"count" : count}}, upsert=True)

