import cPickle
import collections
import jinja2
import multiprocessing
import os
import pymongo
import uuid

import dnslog
import logging
import mail
import settings
import util
import yapsy.IPlugin

class AlertAnalysis(yapsy.IPlugin.IPlugin):
    OUTPUTPATH = os.path.join(settings.APP_DIR, "output/alert")

    def activate(self):
        pass

    @util.ensure_directory(OUTPUTPATH)
    def analysis(self, entries):
        counter = collections.Counter()
        round_minutes_by_5 = util.round_minutes_by(5)
        for entry in entries:
            date, ip, domain, resolve_state, resolve_detail = (
                entry[dnslog.DATE], entry[dnslog.SOURCE_IP], entry[dnslog.DOMAIN], entry[dnslog.RESOLVE_STATE], entry[dnslog.RESOLVE_DETAIL])
            if  resolve_state != "success" or "aa" not in resolve_detail:
                counter[round_minutes_by_5(date).strftime("%y-%m-%d %H:%M")+  "#" + domain + "#" + resolve_state + "#" + resolve_detail] += 1
        cPickle.dump(counter, open(os.path.join(AlertAnalysis.OUTPUTPATH, "%s.pickle" % uuid.uuid4().hex), "w"), cPickle.HIGHEST_PROTOCOL)

    @util.ensure_directory(OUTPUTPATH)
    def collect(self):
        results = map(util.load_and_delete, util.listdir(AlertAnalysis.OUTPUTPATH))
        collect = reduce(lambda x, y : x + y, results, collections.Counter())
        con = pymongo.Connection(settings.MONGODB_SERVER, settings.MONGODB_SERVER_PORT)
        db = con.alert
        db.alert.ensure_index("domain")
        alerts = []
        for key, count in collect.items():
            date, domain, resolve_state, resolve_detail = key.split("#")
            db.alert.update({"domain":domain, "date": date, "resolve_state": resolve_state, "resolve_detail": resolve_detail}, {"$inc": {"count" : count}}, upsert=True)
            alerts.append((date, domain, resolve_state, resolve_detail, count))
        sorted(alerts, key=lambda record: record[0])

        msg = jinja2.Template(open(os.path.join(settings.TEMPLATE_DIR, "alert_email.tpl")).read().decode("utf-8")).render(alerts=alerts)
        email_proc = multiprocessing.Process(target=mail.send_email, args=(msg,))
        email_proc.start()

        logging.info("alert analysis finished successfully")
    def deactivate(self):
        pass
