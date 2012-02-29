from yapsy.IPlugin import IPlugin
from collections import defaultdict
from util import round_minutes_by
import os
import cPickle

class DomainAnalysis(IPlugin):
    def activate(self):
        self.db = self.con.domain
        self.db.minutely.remove()
        self.db.hourly.remove()
        self.db.daily.remove()
        self.db.weekly.remove()
        self.db.monthly.remove()
        self.db.yearly.remove()

        self.db.minutely.ensure_index("domain")
        self.db.hourly.ensure_index("domain")
        self.db.daily.ensure_index("domain")
        self.db.weekly.ensure_index("domain")
        self.db.monthly.ensure_index("domain")
        self.db.yearly.ensure_index("domain")

    def apply(self, entries):
        round_minutes_by_5 = round_minutes_by(5)
        minutely_collect = defaultdict(int)
        hourly_collect = defaultdict(int)
        daily_collect = defaultdict(int)
        weekly_collect = defaultdict(int)
        monthly_collect = defaultdict(int)
        yearly_collect = defaultdict(int)
        for entry in entries:
            date, ip, domain = entry
            minutely_collect[round_minutes_by_5(date).strftime("%y-%m-%d %H:%M") + "#" + domain] +=1
            hourly_collect[date.strftime("%y-%m-%d %H") + "#" + domain] += 1
            daily_collect[date.strftime("%y-%m-%d") + "#" + domain] += 1
            weekly_collect[date.strftime("%y-%W") + "#" + domain] += 1
            monthly_collect[date.strftime("%y-%m") + "#" + domain] += 1
            yearly_collect[date.strftime("%y") + "#" + domain] += 1

        collect = {
            "minutely" : minutely_collect,
            "hourly" : hourly_collect,
            "daily"  : daily_collect,
            "weekly" : weekly_collect,
            "monthly": monthly_collect,
            "yearly" : yearly_collect
        }
        cPickle.dump(collect, open("output/" + str(os.getpid()) + ".pickle", "w"), 2)

            #self.db.minutely.update({"domain":domain, "date": date.strftime("%y-%m-%d %H:%M")}, {"$inc": {"count" : 1}}, upsert=True)
            #self.db.hourly.update({"domain":domain, "date": date.strftime("%y-%m-%d %H")}, {"$inc": {"count" : 1}}, upsert=True)
            #self.db.daily.update({"domain":domain, "date": date.strftime("%y-%m-%d")}, {"$inc": {"count" : 1}}, upsert=True)
            #self.db.weekly.update({"domain":domain, "date": date.strftime("%y-%W")}, {"$inc": {"count" : 1}}, upsert=True)
            #self.db.monthly.update({"domain":domain, "date": date.strftime("%y-%m")}, {"$inc": {"count" : 1}}, upsert=True)
            #self.db.yearly.update({"domain":domain, "date": date.strftime("%y")}, {"$inc": {"count" : 1}}, upsert=True)

    def deactivate(self):
        pass
