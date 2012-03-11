import os
import cPickle
import dnslog
import settings
import logging
import uuid
import yapsy.IPlugin
import collections
import util
import pymongo

class IPAnalysis(yapsy.IPlugin.IPlugin):
    OUTPUTPATH = os.path.join(settings.APP_DIR, "output/ip")

    def activate(self):
        pass

    @util.ensure_directory(OUTPUTPATH)
    def analysis(self, entries):
		collect = {}
		for perid in dnslog.periods:
			collect[perid] = collections.defaultdict(int)

		round_minutes_by_5 = util.round_minutes_by(5)
		for entry in entries:
			date, ip, domain = entry[dnslog.DATE], entry[dnslog.SOURCE_IP], entry[dnslog.DOMAIN]
			for perid, format in zip(dnslog.periods, dnslog.formats):
				collect[perid][round_minutes_by_5(date).strftime(format) + "#" + ip] += 1

		cPickle.dump(collect, open(os.path.join(IPAnalysis.OUTPUTPATH,  "%s.pickle" % uuid.uuid4().hex), "w"), 2) 

    def collect(self):
        con = pymongo.Connection(settings.MONGODB_SERVER, settings.MONGODB_SERVER_PORT)
        db = con.ip

        periods = dnslog.periods

        collection = collections.defaultdict(int)
        for period in periods:
            collection[period] = {}

        results = map(util.load_and_delete,  util.listdir(IPAnalysis.OUTPUTPATH))

        for result in results:
            for period in periods:
                util.upsert(collection[period], result[period])

        for period in periods:
            db[period].ensure_index("ip")
            for key, count in collection[period].items():
                date, ip = key.split("#")
                db[period].update({"ip":ip, "date": date}, {"$inc": {"count" : count}}, upsert=True)

        logging.info( "ip analysis finished successfully")

    @util.ensure_directory(OUTPUTPATH)
    def deactivate(self):
        pass
