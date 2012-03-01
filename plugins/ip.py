from yapsy.IPlugin import IPlugin
from collections import defaultdict
from util import round_minutes_by
import os
import cPickle
import dnslog

class IPAnalysis(IPlugin):
    def activate(self):
        pass
    def apply(self, entries):
        collect = {}
        for perid in dnslog.periods:
            collect[perid] = defaultdict(int)

        round_minutes_by_5 = round_minutes_by(5)
        for entry in entries:
            date, ip, domain = entry
            for perid, format in zip(dnslog.periods, dnslog.formats):
                collect[perid][round_minutes_by_5(date).strftime(format) + "#" + ip] += 1

        cPickle.dump(collect, open(os.path.join("output", "ip",  str(os.getpid()) + ".pickle"), "w"), 2)
    def collect(self):
        print "ip collect"

    def deactivate(self):
        pass
