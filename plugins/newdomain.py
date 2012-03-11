import os
import cPickle
import dnslog
import util
import settings
import uuid
import logging
import pymongo
from yapsy.IPlugin import IPlugin

class NewDomainAnalysis(IPlugin):
    OUTPUTPATH = os.path.join(settings.APP_DIR, "output/newdomain")

    def load_domain_cache(self, path):
        if not os.path.exists(path):
            return set()
        return cPickle.load(open(path))

    @util.ensure_directory(OUTPUTPATH)
    def activate(self):
        domain_cache_path = os.path.join(NewDomainAnalysis.OUTPUTPATH, "domaincache.pickle")
        self.domain_cache = self.load_domain_cache(domain_cache_path)

    @util.ensure_directory(OUTPUTPATH)
    def analysis(self, entries):
        round_minutes_by_5 = util.round_minutes_by(5)
        candidate_domains = {entry[dnslog.DOMAIN] : round_minutes_by_5(entry[dnslog.DATE]).strftime(dnslog.formats[0]) for entry in entries}
        cPickle.dump(candidate_domains, open(os.path.join(NewDomainAnalysis.OUTPUTPATH, "%s.pickle" % uuid.uuid4().hex), "w"), cPickle.HIGHEST_PROTOCOL)

    @util.ensure_directory(OUTPUTPATH)
    def collect(self):
        con = pymongo.Connection(settings.MONGODB_SERVER, settings.MONGODB_SERVER_PORT)
        db = con.newdomain

        results = map(util.load_and_delete, filter(lambda f: not f.endswith("domaincache.pickle"), util.listdir(NewDomainAnalysis.OUTPUTPATH)))

        # a little trick in the labmda expression
        candicates = reduce(lambda x, y: x.update(y) or x, results, {})
        new_domains = set(candicates.keys()) - self.domain_cache

        batch_data = [{"domain": domain, "date": candicates[domain]} for domain in new_domains]

        if batch_data:
            db.newdomain.ensure_index("domain", deprecated_unique = True)
            db.newdomain.insert(batch_data, continue_on_error=True)
            cPickle.dump(new_domains | self.domain_cache , open(os.path.join(NewDomainAnalysis.OUTPUTPATH, "domaincache.pickle"), "w"), cPickle.HIGHEST_PROTOCOL)

        logging.info("newdomain analysis finished successfully")

    def deactivate(self):
        pass
