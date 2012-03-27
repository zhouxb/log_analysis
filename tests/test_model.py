import model
import unittest
import pymongo
import settings
import collections

con = pymongo.Connection(settings.MONGODB_SERVER, settings.MONGODB_SERVER_PORT)

class TestDomaindbModel(unittest.TestCase):
	def test_save(self):
		m = model.DomainDBModel()
		m.data =[{"domain": "www.google.com", "date": "2012", "count": 10, "namelist": "w"}] 
		m.save()

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

class TestIPDBModel(unittest.TestCase):
	def setUp(self):
		database = model.IPDBModel.database
		collection = model.IPDBModel.collection
		coll = con[database][collection]
		coll.drop()
		self.coll = coll
	def test_save(self):
		self.assertEqual(self.coll.find().count(), 0)
		data = [{"ip": "211.87.147.164", "date": "201103120540", "count": 100}]
		m1 = model.IPDBModel(data)
		m1.save()
		m1.save()
		self.assertEqual(self.coll.find().count(), 1)
		m2 = model.IPDBModel(data)
		m2.save()
		self.assertEqual(self.coll.find().count(), 1)

class TestDomainCacheModel(unittest.TestCase):
	def test_save_and_load_with_empty_data(self):
		default = model.DomainCacheModel.default
		m = model.DomainCacheModel(default)
		m.save()
		result = m.load_all()
		self.assertEqual(result, default)
	def test_save_and_load(self):
		data1 = model.DomainCacheModel.default
		data1["20111212#www.google.com"]["count"] = 11
		data1["20111212#www.google.com"]["namelist"] = "w"
		m1 = model.DomainCacheModel([data1])
		m1.save()
		result1 = m1.load_all()
		self.assertEqual(result1, [data1])

		#data2 = collections.Counter({"www.google.com": 12})
		#m1.save()
		#m2 = model.DomainCacheModel(data2)
		#m2.save()
		#result2 = m1.load_all()
		#self.assertEqual(result2, collections.Counter({"www.google.com": 23}))

class TestIPCacheModel(unittest.TestCase):
	def test_save_and_load_with_empty_data(self):
		m = model.IPCacheModel(dict())
		m.save()
		result = m.load_all()
		self.assertEqual(result, dict())
	def test_save_and_load(self):
		data1 = collections.Counter({"127.0.0.1": 11})
		m1 = model.IPCacheModel(data1)
		m1.save()
		result1 = m1.load_all()
		self.assertEqual(result1, data1)

		data2 = collections.Counter({"127.0.0.1": 12})
		m1.save()
		m2 = model.IPCacheModel(data2)
		m2.save()
		result2 = m1.load_all()
		self.assertEqual(result2, collections.Counter({"127.0.0.1": 23}))

class TestIPSegmentModel(unittest.TestCase):
    def test_get(self):
        m = model.IPSegmentsModel()
        ips = m.get()
        self.assertIsNotNone(ips)

    @unittest.skip("skip get ips from remote")
    def test_get_from_remote(self):
        m = model.IPSegmentsModel()
        ips = m.get_from_remote()
        self.assertIsNotNone(ips)

class TestTop100domainModel(unittest.TestCase):
    def test_get(self):
        m = model.Top100DomainnModel()
        domains = m.get()
        self.assertTrue(len(domains))

    @unittest.skip("skip get top100 domain from remote")
    def test_get_from_remote(self):
        m = model.Top100DomainnModel()
        domains = m.get_from_remote()
        self.assertTrue(len(domains) > 0)

