import os
import cPickle
import logging
import uuid

import util
import model
import settings

from yapsy.IPlugin import IPlugin
from dnslog import DATE, DOMAIN, RESOLVE_DETAIL, is_silent, in_whitelist, \
                   formats

OUTPUTPATH = os.path.join(settings.APP_OUTPUT_DIR, "leadingin")

class LeadingInAnalysis(IPlugin):

    def load_domain_cache(self, path):
        if not os.path.exists(path):
            return set()
        return cPickle.load(open(path))

    def activate(self):
        self.domain_cache_path = os.path.join(OUTPUTPATH, "domaincache.pickle")
        self.domain_cache = self.load_domain_cache(self.domain_cache_path)

    def analysis(self, entries):
        uncached_domain, changed_domain = \
                self.do_analysis(self.domain_cache, entries)
        self.save_partial_result(uncached_domain, changed_domain)

    def collect(self):
        uncached_domain, changed_domain = self.do_collect()
        self.save_whole_result(uncached_domain, changed_domain)
        logging.info("CM leading-in-domain analysis finished successfully")

    def do_analysis(self, domain_cache, entries):
        round_minutes_by_5 = util.round_minutes_by(5)
        uncached_domain = set()
        changed_domain = dict()
        for entry in entries:
            date, domain, resolve_detail = \
                    entry[DATE], entry[DOMAIN], entry[RESOLVE_DETAIL]
            if in_whitelist(resolve_detail) and domain not in domain_cache:
                uncached_domain.add(domain)
            if is_silent(resolve_detail) and domain in domain_cache:
                rounded_date = round_minutes_by_5(date).strftime(formats[0])
                changed_domain[domain] = rounded_date
        return uncached_domain, changed_domain

    @util.ensure_directory(OUTPUTPATH)
    def save_partial_result(self, uncached_domain, changed_domain):
        for data, suffix in zip([ uncached_domain,   changed_domain],
                                ["uncached_domain", "changed_domain"]):
            filename = "%s-%s.pickle" % (uuid.uuid4().hex, suffix)
            fullpath = os.path.join(OUTPUTPATH, filename)
            cPickle.dump(data, open(fullpath, "w"), cPickle.HIGHEST_PROTOCOL)

    @util.ensure_directory(OUTPUTPATH)
    def do_collect(self):
        uncached_domain = reduce(lambda x, y: x | y, 
                                 map(util.load_and_delete,
                                     filter(lambda name: name.endswith("uncached_domain.pickle"),
                                            util.listdir(OUTPUTPATH))),
                                 set())
        changed_domain = reduce(lambda x, y: x.update(y) or x,
                                map(util.load_and_delete,
                                    filter(lambda name: name.endswith("changed_domain.pickle"),
                                           util.listdir(OUTPUTPATH))),
                                dict())
        return uncached_domain, changed_domain

    @util.ensure_directory(OUTPUTPATH)
    def save_whole_result(self, uncached_domain, changed_domain):
        self.domain_cache = self.domain_cache | uncached_domain
        cPickle.dump(self.domain_cache, open(self.domain_cache_path, "w"), 
                     cPickle.HIGHEST_PROTOCOL)

        batch = [{"domain": domain, "date": date} \
                 for domain, date in changed_domain.items()]
        m = model.LeadingInDomainModel(batch)
        m.save()
    def deactivate(self):
        pass
