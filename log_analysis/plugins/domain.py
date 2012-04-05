import collections
import operator
import yapsy.IPlugin

import dnslog
import logging
import util
import model

class DomainAnalysis(yapsy.IPlugin.IPlugin):
    def activate(self):
        selector = operator.itemgetter(dnslog.DATE,   dnslog.SOURCE_IP,
                                       dnslog.DOMAIN, dnslog.RESOLVE_DETAIL)
        self.selector = selector
        self.db_model = model.DomainDBModel
        self.cache_model = model.DomainCacheModel

    def analysis(self, entries):
        partial_result = self.do_analysis(entries)
        self.save_partial_result(partial_result)

    def do_analysis(self, entries):
        rounder = util.round_minutes_by(5)
        partial_result = collections.defaultdict(dict)
        for entry in entries:
            date, ip, domain, resolve_detail = self.selector(entry)

            rounded_date = rounder(date).strftime(dnslog.formats[0])
            namelist = dnslog.get_namelist(resolve_detail)

            key = "%s#%s" % (rounded_date, domain)
            record = partial_result[key]
            record["domain"] = domain
            record["date" ] = rounded_date
            record["namelist"] = namelist
            record["count"] = record.get("count", 0) + 1
        return partial_result

    def save_partial_result(self, partial_result):
        self.cache_model(partial_result).save()

    def collect(self):
        whole_result = self.do_collect()
        self.save_whole_result(whole_result)
        logging.info( "domain analysis finished successfully")

    def do_collect(self):
        return self.cache_model().load_all()

    def save_whole_result(self, whole_result):
        batch = whole_result.values()
        self.db_model(self.select_top_n(batch, 150)).save()

    def select_top_n(self, batch, n):
        topdomain = []
        for code in ["w", "B", "G", "-"]:
            domains = sorted([item for item in batch if item["namelist"] == code], 
                                 key=lambda item: item["count"], 
                                 reverse=True)[:n]
            topdomain += domains
        return topdomain

    def deactivate(self):
        pass
