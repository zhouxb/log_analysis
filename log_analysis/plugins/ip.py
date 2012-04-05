import dnslog
import logging
import yapsy.IPlugin
import collections
import util
import operator
import model

class IPAnalysis(yapsy.IPlugin.IPlugin):

	def activate(self):
		selector = operator.itemgetter(dnslog.DATE,   dnslog.SOURCE_IP)
		self.selector = selector
		self.db_model = model.IPDBModel
		self.cache_model = model.IPCacheModel

	def analysis(self, entries):
		partial_result = self.do_analysis(entries)
		self.save_partial_result(partial_result)


	def do_analysis(self, entries):
		partial_result = collections.Counter()
		rounder = util.round_minutes_by(5)

		for entry in entries:
			date, ip  = self.selector(entry)
			rounded_date = rounder(date).strftime(dnslog.formats[0])
			key = "%s#%s" % (rounded_date, ip)
			partial_result[key] += 1
		return partial_result

	def save_partial_result(self, partial_result):
		self.cache_model(partial_result).save()

	def collect(self):
		whole_result = self.do_collect()
		self.save_whole_result(whole_result)
		logging.info( "ip analysis finished successfully")

	def do_collect(self):
		return self.cache_model().load_all()

	def save_whole_result(self, whole_result):
		batch = []
		for key, count in whole_result.most_common(150):
			date, ip = key.split("#")
			batch.append({"ip":ip, "date": date, "count" : count})
		self.db_model(batch).save()

	def deactivate(self):
		pass
