"""
    Tests for instagram api.
"""
from __future__ import unicode_literals, print_function

import json
import unittest

import responses

import pyfacebook


class InstagramApiTest(unittest.TestCase):
    DEFAULT_GRAPH_URL = pyfacebook.InstagramApi.GRAPH_URL
    DEFAULT_GRAPH_VERSION = pyfacebook.InstagramApi.VALID_API_VERSIONS[-1]

    BASE_PATH = 'testdata/instagram/'

    with open(BASE_PATH + 'business_user.json', 'rb') as f:
        BUSINESS_USER_INFO = json.loads(f.read().decode('utf-8'))
    with open(BASE_PATH + 'business_user_media.json', 'rb') as f:
        BUSINESS_USER_MEDIA = json.loads(f.read().decode('utf-8'))
    with open(BASE_PATH + 'business_user_media_2.json', 'rb') as f:
        BUSINESS_USER_MEDIA_2 = json.loads(f.read().decode('utf-8'))

    def setUp(self):
        self.prefix_url = self.DEFAULT_GRAPH_URL + self.DEFAULT_GRAPH_VERSION
        self.api = pyfacebook.InstagramApi(
            long_term_token='token',
            instagram_business_id='test'
        )

    def testApiInit(self):
        with self.assertRaises(pyfacebook.PyFacebookError):
            pyfacebook.InstagramApi(long_term_token='token')

    @responses.activate
    def testDiscoveryUser(self):
        responses.add(
            method=responses.GET, url=self.prefix_url + '/' + self.api.instagram_business_id,
            json=self.BUSINESS_USER_INFO,
        )
        user_info = self.api.discovery_user(username='facebook')
        self.assertEqual(user_info.id, '17841400455970028')

        user_info_json = self.api.discovery_user(username='facebook', include_media=True, return_json=True)
        self.assertEqual(len(user_info_json['media']['data']), 25)

    @responses.activate
    def testDiscoveryMedia(self):
        with responses.RequestsMock() as m:
            m.add(
                'GET', url=self.prefix_url + '/' + self.api.instagram_business_id,
                json=self.BUSINESS_USER_MEDIA
            )
            m.add(
                'GET', url=self.prefix_url + '/' + self.api.instagram_business_id,
                json=self.BUSINESS_USER_MEDIA_2
            )

            medias = self.api.discovery_user_medias(username='facebook', since_time='2019-7-1', until_time='2019-10-1')
            self.assertEqual(len(medias), 4)

            medias = self.api.discovery_user_medias('facebook', count=2, return_json=True)
            self.assertEqual(len(medias), 2)

            with self.assertRaises(pyfacebook.PyFacebookError):
                self.api.discovery_user_medias('facebook', since_time='2019')
                self.api.discovery_user_medias('facebook', until_time='2019')
