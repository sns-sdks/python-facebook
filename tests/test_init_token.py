# coding=utf-8
from __future__ import unicode_literals, print_function

import json
import unittest
import pyfacebook
from requests.exceptions import Timeout, ConnectionError

import responses


class ApiTest(unittest.TestCase):

    def setUp(self):
        self.base_url = "https://graph.facebook.com/"
        self.base_path = 'testdata/facebook/'
        self.version = pyfacebook.Api.VALID_API_VERSIONS[-1]

    def testApiSetUp(self):
        with self.assertRaises((pyfacebook.PyFacebookError, ConnectionError)):
            pyfacebook.Api(app_id='test')

    def testApiNoAuthError(self):
        api = pyfacebook.Api(long_term_token='test', timeout=1)
        with self.assertRaises((pyfacebook.PyFacebookError, Timeout)):
            api.get_token_info()

    @responses.activate
    def testApiOnlyShortToken(self):
        responses.add(
            method=responses.GET,
            url=self.base_url + "{}/oauth/access_token".format(self.version),
            json={'access_token': 'testToken'}
        )
        with open(self.base_path + 'access_token.json', 'rb') as f:
            token_data = json.loads(f.read().decode('utf-8'))
        responses.add(
            method=responses.GET,
            url=self.base_url + '{0}/debug_token'.format(self.version),
            json={'data': token_data}
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
        self.assertEqual(api.version, pyfacebook.Api.VALID_API_VERSIONS[-1])

        with open(self.base_path + 'access_token.json', 'rb') as f:
            token_data = json.loads(f.read().decode('utf-8'))
        responses.add(
            method=responses.GET,
            url=self.base_url + '{0}/debug_token'.format(self.version),
            json={'data': token_data}
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

        with self.assertRaises(pyfacebook.PyFacebookError) as cm:
            pyfacebook.Api(
                app_id='test',
                app_secret='test',
                short_token='test',
                interval_between_request=0,
            )
            self.assertEqual(cm.exception.message, 'Min interval is 1')
            pyfacebook.Api(
                app_id='test',
                app_secret='test',
                short_token='test',
                version='3.0',
            )
