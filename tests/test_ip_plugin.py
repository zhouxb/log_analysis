import unittest
import settings
import yapsy.PluginManager

class TestAlsertPlugin(unittest.TestCase):
    def setUp(self):
        manager = yapsy.PluginManager.PluginManager(plugin_info_ext="info")
        manager.setPluginPlaces([settings.PLUGINS_PATH])
        manager.collectPlugins()
        self.manager = manager

    def tearDown(self):
        pass

    def test_load_plugin(self):
        plugin = self.manager.getPluginByName("ip")
        self.assertIsNotNone(plugin)
