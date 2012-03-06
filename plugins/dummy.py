import dnslog
import log
from yapsy.IPlugin import IPlugin

class DummynAnalysis(IPlugin):
    def activate(self):
        pass
    def analysis(self, entries):
        for entry in entries:
            date, ip, domain = entry[dnslog.DATE], entry[dnslog.SOURCE_IP], entry[dnslog.DOMAIN]
    def collect(self):
        logger = log.get_global_logger()
        logger.info("dummy analysis finished successfully")
    def deactivate(self):
        pass
