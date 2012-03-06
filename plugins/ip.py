import os
import cPickle
import dnslog
import settings
import log
from pymongo import Connection
from yapsy.IPlugin import IPlugin
from collections import defaultdict
from util import round_minutes_by, ensure_directory, upsert

class IPAnalysis(IPlugin):
    OUTPUTPATH = os.path.join(settings.APP_DIR, "output/ip")

    @ensure_directory(OUTPUTPATH)
    def activate(self):
        pass

    def analysis(self, entries):
		collect = {}
		for perid in dnslog.periods:
			collect[perid] = defaultdict(int)

		round_minutes_by_5 = round_minutes_by(5)
		for entry in entries:
			date, ip, domain = entry[dnslog.DATE], entry[dnslog.SOURCE_IP], entry[dnslog.DOMAIN]
			for perid, format in zip(dnslog.periods, dnslog.formats):
				collect[perid][round_minutes_by_5(date).strftime(format) + "#" + ip] += 1

		cPickle.dump(collect, open(os.path.join(IPAnalysis.OUTPUTPATH,  str(os.getpid()) + ".pickle"), "w"), 2) 

    def collect(self):
        def load_and_delete(f):
            full_path = os.path.join(IPAnalysis.OUTPUTPATH,  f)
            result = cPickle.load(open(full_path))
            os.remove(full_path)
            return result
        con = Connection(settings.MONGODB_SERVER, settings.MONGODB_SERVER_PORT)
        db = con.ip

        periods = dnslog.periods

        collection = defaultdict(int)
        for period in periods:
            collection[period] = {}

        results = map(load_and_delete,  os.listdir(IPAnalysis.OUTPUTPATH))

        for result in results:
            for period in periods:
                upsert(collection[period], result[period])

        for period in periods:
            db[period].ensure_index("ip")
            for key, count in collection[period].items():
                date, ip = key.split("#")
                db[period].update({"ip":ip, "date": date}, {"$inc": {"count" : count}}, upsert=True)

        logger = log.get_global_logger()
        logger.info( "ip analysis finished successfully")
    @ensure_directory(OUTPUTPATH)
    def deactivate(self):
        pass
