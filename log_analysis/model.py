import settings
import pymongo
import util
import uuid
import os
import collections
import cPickle
import json
import urllib2
import itertools
import datetime

class DBModel(object):
    con               = pymongo.Connection(settings.MONGODB_SERVER,
                                           settings.MONGODB_SERVER_PORT)

    database          = None
    collection        = None
    indexes           = None
    unique_index      = None
    upsert_method     = None
    continue_on_error = False
    upsert            = True

    def __init__(self, data = None):
        self.data = data
        self.saved = False

    def _insert(self, coll):
        for entry in self.data:
            entry["province"] = settings.PROVINCE
        coll.insert(self.data, continue_on_error = self.continue_on_error)
        self.saved = True

    def _update(self, coll):
        for entry in self.data:
            query = {key: entry[key] for key in self.query_keys}
            query["province"] = settings.PROVINCE
            update = {method : {key: entry[key]} for method, key in self.update_keys}
            coll.update(query, update, upsert=self.upsert)

    def save(self):
        if self.saved:
            return
        if not all([self.database, self.collection, self.data, self.save_method]):
            return
        coll = self.con[self.database][self.collection]
        if self.unique_index:
            coll.ensure_index(self.unique_index, unique = True)
        if self.indexes:
            coll.ensure_index(self.indexes)
        if self.save_method == "insert":
            self._insert(coll)
        elif self.save_method == "update":
            self._update(coll)

class DomainDBModel(DBModel):
    database      = "domain"
    collection    = "minutely"
    indexes       = [("date", -1), ("domain", 1)]
    save_method   = "update"
    query_keys    = ["domain", "date"]
    update_keys   = [("$inc", "count"), ("$set", "namelist")]

class Non80DBModel(DBModel):
    database      = "non80"
    collection    = "minutely"
    indexes       = [("date", -1), ("domain", 1)]
    save_method   = "update"
    query_keys    = ["domain", "date", "type"]
    update_keys   = [("$inc", "count")]

class IPDBModel(DBModel):
    database      = "ip"
    collection    = "minutely"
    indexes       = [("date", -1), ("ip", 1)]
    save_method   = "update"
    query_keys    = ["date", "ip"]
    update_keys   = [("$inc", "count")]

class AlertDBModel(DBModel):
    database      = "alert"
    collection    = "minutely"
    indexes       = [("date", -1), ("domain", 1)]
    unique_index  = None
    save_method   = "update"
    query_keys    = ["date", "domain"]
    def _update(self, coll):
        for entry in self.data:
            query = {key: entry[key] for key in self.query_keys}
            query["province"] = settings.PROVINCE

            ipcount = {}
            for ip, count in entry["ips"].items():
                ipcount["ips.%s" % ip.replace('.', '#')] = count

            update = {"$inc": ipcount}
            coll.update(query, update, upsert=self.upsert)

class LeadingInDomainModel(DBModel):
    database     = "leadingindomain"
    collection   = "minutely"
    indexes      = [("date", -1), ("domain", 1)]
    unique_index = "domain"
    save_method  = "insert"
    continue_on_error = True

class PickleModel(object):
    path           = None
    suffix         = None
    default        = None
    combine_method = None
    def __init__(self, data = None):
        self.data = data

    def load_all(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        results = [util.load_and_delete(name) 
                      for name in util.listdir(self.path) 
                          if name.endswith(self.suffix)]
        if len(results) == 0:
            return self.default
        if len(results) == 1:
            return results[0]
        return reduce(self.combine_method, results)

    def save(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        full_path = os.path.join(self.path, "%s-%s" % (uuid.uuid4(), self.suffix))
        cPickle.dump(self.data, open(full_path, "w"), cPickle.HIGHEST_PROTOCOL)

class DomainCacheModel(PickleModel):
    path = os.path.join(settings.APP_OUTPUT_DIR, "domain")
    suffix = "domain.pickle"
    default = collections.defaultdict(dict)

    def combine_method(self, x, y):
        for key in y.keys():
            if key in x:
                x[key]["count"] += y[key]["count"]
            else:
                x[key] = y[key]
        return x

class Non80CacheModel(PickleModel):
    path = os.path.join(settings.APP_OUTPUT_DIR, "non80")
    suffix = "non80.pickle"
    default = collections.defaultdict(dict)

    def combine_method(self, x, y):
        for key in y.keys():
            if key in x:
                x[key]["count"] += y[key]["count"]
            else:
                x[key] = y[key]
        return x

class IPCacheModel(PickleModel):
    path = os.path.join(settings.APP_OUTPUT_DIR, "ip")
    suffix = "ip.pickle"
    default = collections.Counter()
    combine_method = lambda self, x, y: x + y


class AlertCacheModel(PickleModel):
    path = os.path.join(settings.APP_OUTPUT_DIR, "alert")
    suffix = "alert.pickle"
    default = collections.defaultdict(collections.Counter)
    def combine_method(self, x, y):
        z = collections.defaultdict(collections.Counter)
        for key in set(x.keys()) | set(y.keys()):
            z[key] = x[key] + y[key]
        return z

class RemoteModel:
    path       = None
    suffix     = None
    timeout    = datetime.timedelta(days=1)
    def get(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        cachefiles = sorted(filter(lambda name: name.endswith(self.suffix), 
                            os.listdir(self.path)))

        has_validated_cache = False
        if cachefiles:
            latest_cache = max(cachefiles)
            latest_date = datetime.datetime.strptime(latest_cache.split('-')[0], "%Y%m%d%H")
            if datetime.datetime.today() - latest_date < self.timeout:
                has_validated_cache = True

        if not has_validated_cache:
            today = datetime.datetime.today().strftime("%Y%m%d%H")
            cachefile = os.path.join(self.path, "%s-%s" % (today, self.suffix))
            cache = self.get_from_remote()
            if cache:
                cPickle.dump(cache, open(cachefile, "w"))
                cachefiles = sorted(filter(lambda name: name.endswith(self.suffix), 
                                    os.listdir(self.path)))

        return cPickle.load(open(os.path.join(self.path, max(cachefiles))))

    def get_from_remote(self):
        raise NotImplementedError()

    def get_param(self):
        raise NotImplementedError()

class IPSegmentsModel(RemoteModel):
    path       = os.path.join(settings.APP_OUTPUT_DIR, "alert")
    suffix     = "ipcache.pickle"
    remote_url = "http://rcmsapi.chinacache.com:36000/node/ips"
    def __init__(self):
        pass

    def get_from_remote(self):
        try:
            fp = urllib2.urlopen(self.remote_url)
        except:
            return None
        ips_info = json.load(fp)

        ip_segments = [(item["ipStart"], item["ipEnd"]) for item in ips_info]
        ips = [util.ip_range_to_int(begin, end) for begin, end in ip_segments]
        ips = list(itertools.chain(*ips))
        return ips

class Top100DomainnModel(RemoteModel):
    path       = os.path.join(settings.APP_OUTPUT_DIR, "alert")
    suffix     = "top100domaincache.pickle"

    def get_from_remote(self):
        date = datetime.datetime.today() - datetime.timedelta(days=1)
        yesterday = date.strftime("%Y-%m-%d")
        province_id = settings.PROVINCE_CODE
        url = "http://221.130.162.89:5000/top100domains?customer_id=%s&day=%s" % \
                (province_id, yesterday)

        try:
            content = urllib2.urlopen(url).read()
        except:
            return None
        domains = content.split()
        return domains
