import unittest
import settings
import dnslog
import collections
import yapsy.PluginManager

class TestAlsertPlugin(unittest.TestCase):
    def setUp(self):
        manager = yapsy.PluginManager.PluginManager(plugin_info_ext="info")
        manager.setPluginPlaces([settings.PLUGINS_PATH])
        manager.collectPlugins()
        plugin = manager.getPluginByName("alert")
        self.plugin = plugin

    def tearDown(self):
        pass

    def test_load_plugin(self):
        self.assertIsNotNone(self.plugin)

    def test_get_top100(self):
        pobj = self.plugin.plugin_object
        pobj.activate()
        self.assertTrue(len(pobj.get_top100()) > 0)

    def test_get_cc_ip(self):
        pobj = self.plugin.plugin_object
        pobj.activate()
        self.assertTrue(len(pobj.get_cc_ip()) > 0)

    def test_send_mail(self):
        data = collections.defaultdict(collections.Counter)
        data["2012#www.googole.com"]["192.168.1.1"] = 10
        data["2012#www.googole.com"]["192.168.1.1"] = 10

        pobj = self.plugin.plugin_object
        pobj.activate()
        pobj.save_whole_result(data)

    #def test_do_analysis(self):
        #chunk =  \
#'''
#11-09-01 10:21:25,041 INFO : queries: - |127.0.0.1|www.google.com|default|\
#58.68.239.29;|default;|A|failure|+|---w--- qr aa rd ra |202|
#11-09-01 10:21:25,041 INFO : queries: - |127.0.0.1|www.google.com|default|\
#58.68.239.39;|default;|A|success|+|---w--- qr aa rd ra |202|
#11-09-01 10:21:25,041 INFO : queries: - |127.0.0.1|www.google.com|default|\
#58.68.239.29;|default;|A|success|+|---w--- qr aa rd ra |202|
#11-09-01 10:21:25,041 INFO : queries: - |127.0.0.1|www.baidu.cn|default|\
#58.68.239.14;|default;|A|success|+|---w--- qr aa rd ra |203|
#'''
        #entries = dnslog.parse_chunk(chunk.splitlines())

        #pobj = self.plugin.plugin_object
        #pobj.activate()
        #result = pobj.do_analysis(entries)
        #self.assertEqual(result["201109011020#www.google.com"]["58.68.239.39"], 1)
        #self.assertEqual(result["201109011020#www.google.com"]["58.68.239.29"], 1)
