import dnslog
import logging
from yapsy.IPlugin import IPlugin

class DummynAnalysis(IPlugin):
    def activate(self):
        pass
    def analysis(self, entries):
        for entry in entries:
            date, ip, domain = entry[dnslog.DATE], entry[dnslog.SOURCE_IP], entry[dnslog.DOMAIN]
    def collect(self):
        logging.info("dummy analysis finished successfully")
    def deactivate(self):
        pass
