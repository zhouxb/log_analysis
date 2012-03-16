import collections
import yapsy.IPlugin

import dnslog
import logging
import util
import model

class DomainAnalysis(yapsy.IPlugin.IPlugin):
    def activate(self):
        pass

    def analysis(self, entries):
        partial_result = self.do_analysis(entries)
        self.save_partial_result(partial_result)

    def do_analysis(self, entries):
        partial_result = collections.Counter()

        round_minutes_by_5 = util.round_minutes_by(5)
        for entry in entries:
            date, ip, domain = entry[dnslog.DATE], entry[dnslog.SOURCE_IP], \
                                                   entry[dnslog.DOMAIN]
            rounded_date = round_minutes_by_5(date).strftime(dnslog.formats[0])
            partial_result[rounded_date+ "#" + domain] += 1
        return partial_result


    def save_partial_result(self, partial_result):
        m = model.DomainCacheModel(partial_result)
        m.save()

    def collect(self):
        whole_result = self.do_collect()
        self.save_whole_result(whole_result)
        logging.info( "domain analysis finished successfully")

    def do_collect(self):
        m = model.DomainCacheModel()
        return m.load_all()

    def save_whole_result(self, whole_result):
        data = []
        for key, count in whole_result.items():
            date, domain = key.split("#")
            data.append(({"domain": domain, "date":date}, {"count": count}))
        m = model.DomainModel(data)
        m.save()
    def deactivate(self):
        pass
