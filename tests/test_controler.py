import os
import unittest
import controller
import settings
from puremvc.patterns.observer import Notification

tmpdir = os.path.join(settings.APP_DIR, "tmp")

#class TestControler(unittest.TestCase):
    #def setUp(self):
        #filename = "queries.log.CMN-CQ-2-375.20120217223800.gz"
        #self.filename = os.path.join(tmpdir, filename)
        #os.system("touch %s" % self.filename)

    #def test_prepare_command(self):
        #note = Notification("who knows")
        #note.body = self.filename

        #cmd = controller.PreprocessCommand()
        #cmd.facade = "hello"

        #cmd.execute(note)
    #def tearDown(self):
        #pass
