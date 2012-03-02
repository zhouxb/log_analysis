from yapsy.IPlugin import IPlugin

class DummynAnalysis(IPlugin):
    def activate(self):
        pass
    def analysis(self, entries):
        for entry in entries:
            date, ip, domain = entry
    def collect(self):
        print "dummy analysis finished successfully"
    def deactivate(self):
        pass
