# -*- coding: utf-8 -*-
import unittest
import mail


@unittest.skip("skip sending email test")
class TestMail(unittest.TestCase):
    def test_send_html_email(self):
        content = '''
        <html>
        <head></head>
        <body>
        <h1>你好</h1>
        <b> hello world </b>
        </body>
        </html>
        '''
        mail.send_html_mail("DNS 日志告警", content)
