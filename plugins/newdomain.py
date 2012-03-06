import os
import cPickle
import dnslog
import util
import settings
import util
import log
import pymongo
from yapsy.IPlugin import IPlugin

class NewDomainAnalysis(IPlugin):
    OUTPUTPATH = os.path.join(settings.APP_DIR, "output/newdomain")

    def load_old_domains_cache(self, path):
        if os.path.exists(path):
            return cPickle.load(open(path))
        else:
            return {}

    @util.ensure_directory(OUTPUTPATH)
    def activate(self):
        old_domain_cache_path = os.path.join(NewDomainAnalysis.OUTPUTPATH, "olddomain.pickle")
        self.old_domain_cache = self.load_old_domains_cache(old_domain_cache_path)

    @util.ensure_directory(OUTPUTPATH)
    def analysis(self, entries):
        round_minutes_by_5 = util.round_minutes_by(5)
        new_domains = {}
        for entry in entries:
            date, ip, domain = entry[dnslog.DATE], entry[dnslog.SOURCE_IP], entry[dnslog.DOMAIN]
            if domain not in self.old_domain_cache:
                new_domains[domain] = round_minutes_by_5(date).strftime(dnslog.formats[0]) 
        cPickle.dump(new_domains, open(os.path.join(NewDomainAnalysis.OUTPUTPATH, str(os.getpid()) + ".pickle"), "w"), 2)

    @util.ensure_directory(OUTPUTPATH)
    def collect(self):
        con = pymongo.Connection(settings.MONGODB_SERVER, settings.MONGODB_SERVER_PORT)
        db = con.newdomain

        results = map(util.load_and_delete, filter(lambda f: not f.endswith("olddomain.pickle"), util.listdir(NewDomainAnalysis.OUTPUTPATH)))
        new_domains = self.combine_same_domain(results)

        batch_data = [{"domain": domain, "date": date} for domain, date in new_domains.items()]

        if batch_data:
            db.newdomain.ensure_index("domain", deprecated_unique = True)
            db.newdomain.insert(batch_data, continue_on_error=True)
            new_domains.update(self.old_domain_cache)
            cPickle.dump(new_domains, open(os.path.join(NewDomainAnalysis.OUTPUTPATH, "olddomain.pickle"), "w"), 2)

        logger = log.get_global_logger()
        logger.info("newdomain analysis finished successfully")

    def combine_same_domain(self, results):
        all_domain = {}
        for result in results:
            for domain, date in result.items():
                if not all_domain.get(domain):
                    all_domain[domain] = date
        return all_domain
    def deactivate(self):
        pass
