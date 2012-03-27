# -*- coding: utf-8 -*-
import collections
import jinja2
import multiprocessing
import os
import operator

import dnslog
import logging
import mail
import settings
import util
import model
import yapsy.IPlugin

class AlertAnalysis(yapsy.IPlugin.IPlugin):
    OUTPUTPATH = os.path.join(settings.APP_OUTPUT_DIR, "alert")

    def activate(self):
        selector = operator.itemgetter(dnslog.DATE,  
                                       dnslog.DOMAIN,  
                                       dnslog.RESOLVED_IP,
                                       dnslog.RESOLVE_STATE,
                                       dnslog.RESOLVE_DETAIL)
        self.selector = selector
        self.top100 = self.get_top100()
        self.cc_ips = self.get_cc_ip()
        self.cache_model = model.AlertCacheModel

    def get_top100(self):
        m = model.Top100DomainnModel()
        domains = set(m.get())
        return domains

    def get_cc_ip(self):
        m = model.IPSegmentsModel()
        ips = set(m.get())
        return ips

    @util.ensure_directory(OUTPUTPATH)
    def analysis(self, entries):
        partial_result = self.do_analysis(entries)
        self.save_partial_result(partial_result)

    def do_analysis(self, entries):
        top100 = self.top100
        cc_ips = self.cc_ips
        round_by_5 = util.round_minutes_by(5)
        partial_result = collections.defaultdict(collections.Counter)

        for entry in entries:
            date,  domain, resolved_ips, resolve_state, resolve_detail = \
                                                    self.selector(entry)
            if domain not in top100 or resolve_state != "success":
                continue
            outer_ips = [ip for ip in resolved_ips if util.ip_to_int(ip) not in cc_ips]
            if not outer_ips:
                continue
            rounded_date = round_by_5(date).strftime(dnslog.formats[0]) 
            for resolved_ip in resolved_ips:
                partial_result["%s#%s" % (rounded_date, domain)][resolved_ip] += 1
        return partial_result

    def save_partial_result(self, partial_result):
        self.cache_model(partial_result).save()

    def collect(self):
        whole_result = self.do_collect()
        self.save_whole_result(whole_result)
        logging.info("alert analysis finished successfully")

    def do_collect(self):
        m = model.AlertCacheModel()
        whole_result = m.load_all()
        return whole_result

    def save_whole_result(self, whole_result):
        print whole_result
        #batch = []
        #alerts = []
        #for key, count in whole_result.items():
            #date, domain, resolve_state, resolve_detail = key.split("#")
            #batch.append(({"domain":domain, "date": date, 
                           #"resolve_state": resolve_state, "resolve_detail":
                           #resolve_detail}, {"count" : count}))
            #alerts.append(dict(date=date, domain=domain,
                               #resolve_state=resolve_state,
                               #resolve_detail=resolve_detail, count=count))

        #m = model.AlertModel(batch)
        #m.save()

        #self.alert(alerts)

    def alert(self, stastics):
        tpl = open(os.path.join(settings.TEMPLATE_DIR,
                                "alert_email.tpl")).read().decode("utf-8")
        msg = jinja2.Template(tpl).render(alerts=stastics)
        email_proc = multiprocessing.Process(target=mail.send_html_mail,
                                             args=(u"TOP100 域名解析告警", msg))
        email_proc.start()

    def deactivate(self):
        pass
