import os
import cPickle
import dnslog
import settings

from collections import defaultdict, Counter
from pymongo import Connection
from util import round_minutes_by, ensure_directory
from yapsy.IPlugin import IPlugin
from itertools import product


class DomainAnalysis(IPlugin):
    def activate(self):
        self.outputpath = "output/domain/"
        ensure_directory(self.outputpath)

    def analysis(self, entries, logger):
        collect = {}
        for period in dnslog.periods:
            collect[period] = defaultdict(int)

        round_minutes_by_5 = round_minutes_by(5)
        for entry in entries:
                date, ip, domain = entry[dnslog.DATE], entry[dnslog.SOURCE_IP], entry[dnslog.DOMAIN]
                for perid, format in zip(dnslog.periods, dnslog.formats):
                    collect[perid][round_minutes_by_5(date).strftime(format) + "#" + domain] += 1

        cPickle.dump(collect, open(os.path.join(self.outputpath, str(os.getpid()) + ".pickle"), "w"), 2)

    def collect(self, logger):
        def load_and_delete(f):
            full_path = self.outputpath + f
            result = cPickle.load(open(full_path))
            os.remove(full_path)
            return result
        con = Connection(settings.MONGODB_SERVER, settings.MONGODB_SERVER_PORT)
        db = con.domain

        periods = dnslog.periods

        collection = {}
        for period in periods:
            collection[period] = Counter()

        results = map(load_and_delete, os.listdir(self.outputpath))

        for result, period in product(results, periods):
            collection[period].update(result[period])

        for period in periods:
            db[period].ensure_index("domain")
            for key, count in collection[period].items():
                date, domain = key.split("#")
                db[period].update({"domain":domain, "date": date}, {"$inc": {"count" : count}}, upsert=True)
        logger.info( "domain analysis finished successfully")
    def deactivate(self):
        pass
