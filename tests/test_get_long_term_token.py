# coding=utf-8

import pyfacebook
import unittest


class ApiTest(unittest.TestCase):
    def setUp(self):
        self.api = pyfacebook.Api(
            app_id='test',
            app_secret='test',
            short_token='test',
        )

    def testApiSetUp(self):
        self.assertRaises(
            pyfacebook.PyFacebookError,
            lambda: pyfacebook.Api(app_id='test')
        )

    def testApiInfo(self):
        data = self.api.get_token_info()
        print(data)
        self.assertEqual(type(data), pyfacebook.AccessToken)
