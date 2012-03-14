import unittest
import settings
import dnslog
import yapsy.PluginManager

chunk =  \
'''
11-09-01 10:21:25,041 INFO : queries: - |127.0.0.1|www.google.com|default|\
58.68.239.29;|default;|A|success|+|---w--- qr aa rd ra |202|
11-09-01 10:21:25,041 INFO : queries: - |127.0.0.1|www.baidu.cn|default|\
58.68.239.14;|default;|A|success|+|---w--- qr aa rd ra |203|
11-09-01 10:21:25,041 INFO : queries: - |127.0.0.1|www.twitter.com|default|\
58.68.239.14;|default;|A|success|+|---w--- qr aa rd ra |204|
11-09-01 10:21:25,042 INFO : queries: - |127.0.0.1|www.google.com|default|\
58.68.239.29;|default;|A|success|+|---w--- qr aa rd ra |205|
11-09-01 10:21:25,042 INFO : queries: - |127.0.0.1|www.sina.com|default|\
58.68.239.29;|default;|A|success|+|------- qr aa rd ra |205|
'''


class TestLeadingInAnalysis(unittest.TestCase):
    def setUp(self):
        manager = yapsy.PluginManager.PluginManager(plugin_info_ext="info")
        manager.setPluginPlaces([settings.PLUGINS_PATH])
        manager.collectPlugins()
        plugin = manager.getPluginByName("Leading In Analysis").plugin_object
        self.plugin = plugin

    def tearDown(self):
        pass

    def test_load_plugin(self):
        self.assertIsNotNone(self.plugin)

    def test_do_analysis_with_empty_cache(self):
        plugin = self.plugin
        entries = dnslog.parse_chunk(chunk.splitlines())

        uncached_domain, changed_domain = plugin.do_analysis(set(), entries)
        self.assertEqual(uncached_domain, set(["www.google.com",
                                               "www.baidu.cn", 
                                               "www.twitter.com"]))
        self.assertEqual(changed_domain, dict())

    def test_do_analysis_with_none_empty_cache(self):
        plugin = self.plugin
        entries = dnslog.parse_chunk(chunk.splitlines())
        domain_cache = set(["www.google.com",
                            "www.baidu.cn", 
                            "www.twitter.com"])
        uncached_domain, changed_domain = plugin.do_analysis(domain_cache,
                                                             entries)
        self.assertEqual(uncached_domain, set())
        self.assertEqual(changed_domain, dict())

        domain_cache = set(["www.sina.com",
                            "www.baidu.cn", 
                            "www.twitter.com"])
        uncached_domain, changed_domain = plugin.do_analysis(domain_cache,
                                                             entries)
        self.assertEqual(uncached_domain, set(["www.google.com"]))
        self.assertEqual(changed_domain, {"www.sina.com": "201109011020"})
