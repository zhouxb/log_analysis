import cPickle
import collections
import itertools
import os
import pymongo
import uuid
import yapsy.IPlugin

import dnslog
import logging
import settings
import util

class DomainAnalysis(yapsy.IPlugin.IPlugin):
    OUTPUTPATH = os.path.join(settings.APP_DIR, "output/domain")
    def activate(self):
        pass

    @util.ensure_directory(OUTPUTPATH)
    def analysis(self, entries):
        collect = {}
        for period in dnslog.periods:
            collect[period] = collections.Counter()

        round_minutes_by_5 = util.round_minutes_by(5)
        for entry in entries:
                date, ip, domain = entry[dnslog.DATE], entry[dnslog.SOURCE_IP], entry[dnslog.DOMAIN]
                for perid, format in zip(dnslog.periods, dnslog.formats):
                    collect[perid][round_minutes_by_5(date).strftime(format) + "#" + domain] += 1

        cPickle.dump(collect, open(os.path.join(DomainAnalysis.OUTPUTPATH, "%s.pickle" % uuid.uuid4().hex), "w"), 2)

    @util.ensure_directory(OUTPUTPATH)
    def collect(self):
        con = pymongo.Connection(settings.MONGODB_SERVER, settings.MONGODB_SERVER_PORT)
        db = con.domain

        periods = dnslog.periods

        collection = {}
        for period in periods:
            collection[period] = collections.Counter()

        results = map(util.load_and_delete, util.listdir(DomainAnalysis.OUTPUTPATH))

        for result, period in itertools.product(results, periods):
            collection[period].update(result[period])

        for period in periods:
            db[period].ensure_index("domain")
            for key, count in collection[period].items():
                date, domain = key.split("#")
                db[period].update({"domain":domain, "date": date}, {"$inc": {"count" : count}}, upsert=True)

        logging.info( "domain analysis finished successfully")

    def deactivate(self):
        pass
