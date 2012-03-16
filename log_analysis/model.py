import settings
import pymongo
import util
import uuid
import os
import collections
import cPickle

class BasicbModel(object):
    con               = pymongo.Connection(settings.MONGODB_SERVER,
                            settings.MONGODB_SERVER_PORT)

    database          = None
    collection        = None
    indexes           = None
    uniqueindex       = None
    upsert_method     = None
    continue_on_error = False
    upsert            = True

    def __init__(self, data = None):
        self.data = data
        self.saved = False

    def save(self):
        if self.saved:
            return
        if not all([self.database, self.collection, self.data, 
                    self.save_method]):
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
    def _insert(self, coll):
        coll.insert(self.data, continue_on_error = self.continue_on_error)
        self.saved = True
    def _update(self, coll):
        for query, inc in self.data:
            coll.update(query, {self.upsert_method: inc}, upsert=self.upsert)

class DomainModel(BasicbModel):
    database      = "domain"
    collection    = "minutely"
    indexes       = [("date", -1), ("domain", 1)]
    unique_index  = None
    save_method   = "update"
    upsert_method = "$inc"

class IPModel(BasicbModel):
    database      = "ip"
    collection    = "minutely"
    indexes       = [("date", -1), ("ip", 1)]
    unique_index  = None
    save_method   = "update"
    upsert_method = "$inc"

class LeadingInDomainModel(BasicbModel):
    database     = "leadingindomain"
    collection   = "minutely"
    indexes      = [("date", -1), ("domain", 1)]
    unique_index = "domain"
    save_method  = "insert"
    continue_on_error = True

class TestModel(BasicbModel):
    database     = "test"
    collection   = "minutely"
    indexes      = [("date", -1), ("domain", 1)]
    unique_index = None
    save_method  = "insert"

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
        results = [util.load_and_delete(name) for name in util.listdir(self.path)
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
    default = collections.Counter()
    combine_method = lambda self, x, y: x.update(y) or x

class IPCacheModel(PickleModel):
    path = os.path.join(settings.APP_OUTPUT_DIR, "ip")
    suffix = "ip.pickle"
    default = collections.Counter()
    combine_method = lambda self, x, y: x.update(y) or x
