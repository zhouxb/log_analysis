from pymongo import Connection
import puremvc.patterns.proxy

class TempProxy(puremvc.patterns.proxy.Proxy):
    NAME = 'TempProxy'

    def __init__(self):
        super(TempProxy, self).__init__(TempProxy.NAME, [])
        self.connection = Connection('localhost', 27017)

    def change_data(self, v):
        self.data = v

    def get_data(self):
        return self.data

    def test(self):
        #db = self.connection.test_database
        #collection = db.test_collection
        #print collection
        db = self.connection.domain

        domain = db.domain
        domain.save({'id':1, 'name':'test'})
        print domain.find_one({'id':1})
