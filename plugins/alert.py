import os
import cPickle
import dnslog
import mail
import settings
import jinja2
from multiprocessing import Process
from util import round_minutes_by, ensure_directory, upsert
from pymongo import Connection
from yapsy.IPlugin import IPlugin
from collections import defaultdict

class AlertAnalysis(IPlugin):
    OUTPUTPATH = os.path.join(settings.APP_DIR, "output/alert")

    def activate(self):
        pass

    @ensure_directory(OUTPUTPATH)
    def analysis(self, entries, logger):
        collect = defaultdict(int)
        round_minutes_by_5 = round_minutes_by(5)
        for entry in entries:
            date, ip, domain, resolve_state, resolve_detail = (
                entry[dnslog.DATE], entry[dnslog.SOURCE_IP], entry[dnslog.DOMAIN], entry[dnslog.RESOLVE_STATE], entry[dnslog.RESOLVE_DETAIL])
            if  resolve_state != "success" or "aa" not in resolve_detail:
                collect[round_minutes_by_5(date).strftime("%y-%m-%d %H:%M")+  "#" + domain + "#" + resolve_state + "#" + resolve_detail] += 1
        cPickle.dump(collect, open(os.path.join(AlertAnalysis.OUTPUTPATH, str(os.getpid()) + ".pickle"), "w"), 2)

    @ensure_directory(OUTPUTPATH)
    def collect(self, logger):
        def load_and_delete(f):
            full_path = os.path.join(AlertAnalysis.OUTPUTPATH, f)
            result = cPickle.load(open(full_path))
            os.remove(full_path)
            return result
        results = map(load_and_delete, os.listdir(AlertAnalysis.OUTPUTPATH))
        collect = defaultdict(int)
        for result in results:
            upsert(collect, result)
        con = Connection(settings.MONGODB_SERVER, settings.MONGODB_SERVER_PORT)
        db = con.alert
        db["resolve"].ensure_index("domain")
        alerts = []
        for key, count in collect.items():
            date, domain, resolve_state, resolve_detail = key.split("#")
            db["resolve"].update({"domain":domain, "date": date, "resolve_state": resolve_state, "resolve_detail": resolve_detail}, {"$inc": {"count" : count}}, upsert=True)
            alerts.append((date, domain, resolve_state, resolve_detail, count))
        sorted(alerts, key=lambda record: record[0])
        msg = jinja2.Template(open(os.path.join(settings.TEMPLATE_DIR, "alert_email.tpl")).read().decode("utf-8")).render(alerts=alerts)
        email_proc = Process(target=mail.send_email, args=(msg,))
        email_proc.start()
        logger.info("alert analysis finished successfully")
    def deactivate(self):
        pass
