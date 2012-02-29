import unittest
import plugins.domain

class TestDomainPlugin(unittest.TestCase):
    def test_domain_plugin(self):
        domain_plugin = plugins.domain.DomainAnalysis()
