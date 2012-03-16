import os
import dnslog
import settings
import logging
import yapsy.IPlugin
import collections
import util
import model

class IPAnalysis(yapsy.IPlugin.IPlugin):
    OUTPUTPATH = os.path.join(settings.APP_OUTPUT_DIR, "ip")

    def activate(self):
        pass

    def analysis(self, entries):
        partial_result = self.do_analysis(entries)
        self.save_partial_result(partial_result)

    def collect(self):
        whole_result = self.do_collect()
        self.save_whole_result(whole_result)
        logging.info( "ip analysis finished successfully")

    def do_analysis(self, entries):
        partial_result = collections.Counter()
        round_minutes_by_5 = util.round_minutes_by(5)

        for entry in entries:
            date, ip, domain = entry[dnslog.DATE], entry[dnslog.SOURCE_IP], entry[dnslog.DOMAIN]
            rounded_date = round_minutes_by_5(date).strftime(dnslog.formats[0])
            partial_result[rounded_date+ "#" + ip] += 1
        return partial_result

    @util.ensure_directory(OUTPUTPATH)
    def save_partial_result(self, partial_result):
        m = model.IPCacheModel(partial_result)
        m.save()

    @util.ensure_directory(OUTPUTPATH)
    def do_collect(self):
        m = model.IPCacheModel()
        whole_result = m.load_all()
        return whole_result

    def save_whole_result(self, whole_result):
        batch = []
        for key, count in whole_result.items():
            date, ip = key.split("#")
            batch.append(({"ip":ip, "date": date}, {"count" : count}))
        m = model.IPModel(batch)
        m.save()
    @util.ensure_directory(OUTPUTPATH)
    def deactivate(self):
        pass
