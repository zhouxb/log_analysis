from yapsy.IPlugin import IPlugin

class DummynAnalysis(IPlugin):
    def activate(self):
        pass
    def apply(self, entries):
        for entry in entries:
            date, ip, domain = entry
    def deactivate(self):
        pass
