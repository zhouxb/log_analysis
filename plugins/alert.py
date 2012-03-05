import dnslog
import mail
from yapsy.IPlugin import IPlugin
from multiprocessing import Process

class DummynAnalysis(IPlugin):
    def activate(self):
        pass
    def analysis(self, entries, logger):
        for entry in entries:
            date, ip, domain = entry[dnslog.DATE], entry[dnslog.SOURCE_IP], entry[dnslog.DOMAIN]
    def collect(self, logger):
        logger.info( "alert analysis finished successfully")
        mail_proc = Process(target=mail.send_email, args=("test", ))
        mail_proc.start()
    def deactivate(self):
        pass
