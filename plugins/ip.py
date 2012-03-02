import os
import cPickle
import dnslog
from pymongo import Connection
from yapsy.IPlugin import IPlugin
from collections import defaultdict
from util import round_minutes_by, ensure_directory, upsert

class IPAnalysis(IPlugin):
    def activate(self):
        self.outputpath = "output/ip/"
        ensure_directory(self.outputpath)

    def analysis(self, entries):
        collect = {}
        for perid in dnslog.periods:
            collect[perid] = defaultdict(int)

        round_minutes_by_5 = round_minutes_by(5)
        for entry in entries:
            date, ip, domain = entry
            for perid, format in zip(dnslog.periods, dnslog.formats):
                collect[perid][round_minutes_by_5(date).strftime(format) + "#" + ip] += 1

        cPickle.dump(collect, open(os.path.join(self.outputpath +  str(os.getpid()) + ".pickle"), "w"), 2)

    def collect(self):
        def load_and_delete(f):
            full_path = self.outputpath + f
            result = cPickle.load(open(full_path))
            os.remove(full_path)
            return result
        con = Connection("localhost")
        db = con.ip

        periods = dnslog.periods

        collection = defaultdict(int)
        for period in periods:
            collection[period] = {}

        results = map(load_and_delete,  os.listdir(self.outputpath))

        for result in results:
            for period in periods:
                upsert(collection[period], result[period])

        for period in periods:
            db[period].ensure_index("ip")
            for key, count in collection[period].items():
                date, ip = key.split("#")
                db[period].update({"ip":ip, "date": date}, {"$inc": {"count" : count}}, upsert=True)

        print "ip analysis finished successfully"
    def deactivate(self):
        pass
