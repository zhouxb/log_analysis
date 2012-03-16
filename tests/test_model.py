import model
import unittest
import pymongo
import settings
import collections

con = pymongo.Connection(settings.MONGODB_SERVER, settings.MONGODB_SERVER_PORT)

class TestTestModel(unittest.TestCase):
    def setUp(self):
        coll = con[model.TestModel.database][model.TestModel.collection]
        coll.drop()
        self.coll = coll
    def tearDown(self):
        pass
    def test_save(self):
        self.assertEqual(self.coll.find().count(), 0)
        m1 = model.TestModel([{"domain": "www.google.com", "date": "20121011"}])
        m1.save()
        m1.save()
        self.assertEqual(self.coll.find().count(), 1)
        m2 = model.TestModel([{"domain": "www.google.com", "date": "20121011"}])
        m2.save()
        m2.save()
        self.assertEqual(self.coll.find().count(), 2)

class TestLeadingInModel(unittest.TestCase):
    def setUp(self):
        database = model.LeadingInDomainModel.database
        collection = model.LeadingInDomainModel.collection
        coll = con[database][collection]
        coll.drop()
        self.coll = coll
    def tearDown(self):
        pass
    def test_save(self):
        self.assertEqual(self.coll.find().count(), 0)
        m1 = model.LeadingInDomainModel([{"domain": "www.google.com", "date": "20121011"}])
        m1.save()
        m1.save()
        self.assertEqual(self.coll.find().count(), 1)
        m2 = model.LeadingInDomainModel([{"domain": "www.google.com", "date": "20121011"}])
        m2.save()
        m2.save()
        self.assertEqual(self.coll.find().count(), 1)

class TestDomainModel(unittest.TestCase):
    def setUp(self):
        database = model.DomainModel.database
        collection = model.DomainModel.collection
        coll = con[database][collection]
        coll.drop()
        self.coll = coll
    def test_save(self):
        self.assertEqual(self.coll.find().count(), 0)
        data = [({"domain": "www.google.com", "date": "201103120540"},{ "count": 100})]
        m1 = model.DomainModel(data)
        m1.save()
        m1.save()
        self.assertEqual(self.coll.find().count(), 1)
        m2 = model.DomainModel(data)
        m2.save()
        self.assertEqual(self.coll.find().count(), 1)

class TestIPModel(unittest.TestCase):
    def setUp(self):
        database = model.IPModel.database
        collection = model.IPModel.collection
        coll = con[database][collection]
        coll.drop()
        self.coll = coll
    def test_save(self):
        self.assertEqual(self.coll.find().count(), 0)
        data = [({"ip": "211.87.147.164", "date": "201103120540"},{ "count": 100})]
        m1 = model.IPModel(data)
        m1.save()
        m1.save()
        self.assertEqual(self.coll.find().count(), 1)
        m2 = model.IPModel(data)
        m2.save()
        self.assertEqual(self.coll.find().count(), 1)

class TestDomainCacheModel(unittest.TestCase):
    def test_save_and_load_with_empty_data(self):
        m = model.DomainCacheModel(dict())
        m.save()
        result = m.load_all()
        self.assertEqual(result, dict())
    def test_save_and_load(self):
        data1 = collections.Counter({"www.google.com": 11})
        m1 = model.DomainCacheModel(data1)
        m1.save()
        result1 = m1.load_all()
        self.assertEqual(result1, data1)

        data2 = collections.Counter({"www.google.com": 12})
        m1.save()
        m2 = model.DomainCacheModel(data2)
        m2.save()
        result2 = m1.load_all()
        self.assertEqual(result2, collections.Counter({"www.google.com": 23}))

class TestIPCacheModel(unittest.TestCase):
    def test_save_and_load_with_empty_data(self):
        m = model.DomainCacheModel(dict())
        m.save()
        result = m.load_all()
        self.assertEqual(result, dict())
    def test_save_and_load(self):
        data1 = collections.Counter({"127.0.0.1": 11})
        m1 = model.DomainCacheModel(data1)
        m1.save()
        result1 = m1.load_all()
        self.assertEqual(result1, data1)

        data2 = collections.Counter({"127.0.0.1": 12})
        m1.save()
        m2 = model.DomainCacheModel(data2)
        m2.save()
        result2 = m1.load_all()
        self.assertEqual(result2, collections.Counter({"127.0.0.1": 23}))
