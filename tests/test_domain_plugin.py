import unittest
import settings
import yapsy.PluginManager

class TestDomainPlugin(unittest.TestCase):
    def setUp(self):
        manager = yapsy.PluginManager.PluginManager(plugin_info_ext="info")
        manager.setPluginPlaces([settings.PLUGINS_PATH])
        manager.collectPlugins()
        plugin = manager.getPluginByName("domain").plugin_object
        self.plugin = plugin

    def tearDown(self):
        pass

    def test_load_plugin(self):
        self.assertIsNotNone(self.plugin)
