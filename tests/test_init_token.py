# coding=utf-8
from __future__ import unicode_literals, print_function

import unittest
import pyfacebook

import responses


class ApiTest(unittest.TestCase):

    def setUp(self):
        self.base_url = "https://graph.facebook.com/"
        self.version = "v3.2"

    def testApiSetUp(self):
        self.assertRaises(
            pyfacebook.PyFacebookError,
            lambda: pyfacebook.Api(app_id='test')
        )

    def testApiNoAuthError(self):
        api = pyfacebook.Api(long_term_token='test')
        self.assertRaises(pyfacebook.PyFacebookError, lambda: api.get_token_info())

    @responses.activate
    def testApiOnlyShortToken(self):
        responses.add(
            method=responses.GET,
            url=self.base_url + "{}/oauth/access_token".format(self.version),
            json={'access_token': 'testToken'}
        )
        api = pyfacebook.Api(
            app_id='test',
            app_secret='test',
            short_token='test'
        )
        self.assertEqual(api.token, "testToken")

    @responses.activate
    def testApiOnlyLongTermToken(self):
        api = pyfacebook.Api(
            long_term_token='testToken',
        )
        self.assertEqual(api.token, "testToken")

        responses.add(
            method=responses.GET,
            url=self.base_url + '{0}/debug_token'.format(self.version),
            json={'data': {
                'app_id': 'test',
                'application': 'test',
                'type': 'test',
                'expires_at': 'test',
                'is_valid': 'test',
                'issued_at': 'test',
                'scopes': 'test',
                'user_id': 'test',
            }}
        )
        info = api.get_token_info()
        self.assertEqual(type(info), pyfacebook.AccessToken)
