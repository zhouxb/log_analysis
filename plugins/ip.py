from yapsy.IPlugin import IPlugin

class IPAnalysis(IPlugin):
    def activate(self):
        pass
        #self.pattern = "ibm"
    def apply(self, entries):
        for entry in entries:
            date, ip, domain = entry
    def deactivate(self):
        pass
