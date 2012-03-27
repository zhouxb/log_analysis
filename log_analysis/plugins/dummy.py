import logging
from yapsy.IPlugin import IPlugin

class DummynAnalysis(IPlugin):
	def activate(self):
		pass

	def analysis(self, entries):
		for entry in entries:
			pass

	def collect(self):
		logging.info("dummy analysis finished successfully")

	def deactivate(self):
		pass
