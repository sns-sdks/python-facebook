# coding=utf-8
from __future__ import unicode_literals, print_function

import unittest
import pyfacebook
from requests.exceptions import Timeout

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
        api = pyfacebook.Api(long_term_token='test', timeout=1)
        self.assertRaises(Timeout, lambda: api.get_token_info())

    @responses.activate
    def testApiOnlyShortToken(self):
        responses.add(
            method=responses.GET,
            url=self.base_url + "{}/oauth/access_token".format(self.version),
            json={'access_token': 'testToken'}
        )

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

        api = pyfacebook.Api(
            app_id='test',
            app_secret='test',
            short_token='test'
        )
        self.assertEqual(api.token, "testToken")

        info = api.get_token_info()
        self.assertEqual(type(info), pyfacebook.AccessToken)

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

    @responses.activate
    def testApiParams(self):
        responses.add(
            method=responses.GET,
            url=self.base_url + "{}/oauth/access_token".format(self.version),
            json={'access_token': 'testToken'}
        )
        self.assertRaises(
            pyfacebook.PyFacebookError,
            lambda: pyfacebook.Api(
                app_id='test',
                app_secret='test',
                short_token='test',
                interval_between_request=0,
            )
        )

        self.assertRaises(
            pyfacebook.PyFacebookError,
            lambda: pyfacebook.Api(
                app_id='test',
                app_secret='test',
                short_token='test',
                version='3.3',
            )
        )
