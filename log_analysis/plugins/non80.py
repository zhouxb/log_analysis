import collections
import operator
import yapsy.IPlugin

import dnslog
import logging
import util
import model

class Non80Analysis(yapsy.IPlugin.IPlugin):
    def activate(self):
        selector = operator.itemgetter(dnslog.DATE, dnslog.DOMAIN, 
                                       dnslog.RECORD_TTYPE)
        self.selector = selector
        self.db_model = model.Non80DBModel
        self.cache_model = model.Non80CacheModel

    def analysis(self, entries):
        partial_result = self.do_analysis(entries)
        self.save_partial_result(partial_result)

    def do_analysis(self, entries):
        rounder = util.round_minutes_by(5)
        partial_result = collections.defaultdict(dict)
        for entry in entries:
            date, domain, record_type = self.selector(entry)

            if record_type not in ["MX", "NS"]:
                continue
            rounded_date = rounder(date).strftime(dnslog.formats[0])

            key = "%s#%s#%s" % (rounded_date, domain, record_type)
            record = partial_result[key]
            record["domain"] = domain
            record["date" ] = rounded_date
            record["type"] = record_type
            record["count"] = record.get("count", 0) + 1
        return partial_result

    def save_partial_result(self, partial_result):
        self.cache_model(partial_result).save()

    def collect(self):
        whole_result = self.do_collect()
        self.save_whole_result(whole_result)
        logging.info( "non 80 port query analysis finished successfully")

    def do_collect(self):
        return self.cache_model().load_all()

    def save_whole_result(self, whole_result):
        batch = whole_result.values()
        self.db_model(batch).save()

    def deactivate(self):
        pass
