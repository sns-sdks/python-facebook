# coding=utf-8

from __future__ import unicode_literals, print_function

import unittest
import pyfacebook

import responses

DEFAULT_GRAPH_URL = "https://graph.facebook.com/"
DEFAULT_GRAPH_VERSION = 'v3.2'


class InsApiTest(unittest.TestCase):
    @responses.activate
    def setUp(self):
        self.instagram_business_id = 'test'
        self.test_username = 'username'
        responses.add(
            method=responses.GET,
            url=DEFAULT_GRAPH_URL + DEFAULT_GRAPH_VERSION + '/oauth/access_token',
            json={'access_token': 'testToken'}
        )

        self.api = pyfacebook.InstagramApi(
            app_id='test',
            app_secret='test',
            short_token='test',
            version='3.2',
            timeout=1,
            interval_between_request=1,
            sleep_on_rate_limit=True,
            instagram_business_id=self.instagram_business_id
        )

    @responses.activate
    def testGetUser(self):
        responses.add(
            method=responses.GET,
            url=DEFAULT_GRAPH_URL + DEFAULT_GRAPH_VERSION + '/' + self.instagram_business_id,
            json={
                u'business_discovery': {
                    'biography': 'biography',
                    'followers_count': 3748942,
                    'follows_count': 65,
                    'id': '1234567891011',
                    'ig_id': 123456789,
                    'media_count': 370,
                    'name': 'name',
                    'profile_picture_url': 'profile_picture_url',
                    'username': 'username',
                    'website': 'https://www.example.com/username/'
                },
                'id': self.instagram_business_id
            }
        )

        self_info = self.api.get_user_info()
        self.assertEqual('profile_picture_url', self_info.profile_picture_url)

        user_info = self.api.get_user_info(username=self.test_username)
        self.assertEqual('biography', user_info.biography)

        user_info_json = self.api.get_user_info(username=self.test_username, return_json=True)
        self.assertEqual('1234567891011', user_info_json['business_discovery']['id'])

    @responses.activate
    def testGetMedia(self):
        media_id = '12345678910'
        responses.add(
            method=responses.GET,
            url=DEFAULT_GRAPH_URL + DEFAULT_GRAPH_VERSION + '/' + media_id,
            json={
                'caption': 'Snowing.',
                'comments_count': 1,
                'id': media_id,
                'ig_id': '123456789',
                'is_comment_enabled': True,
                'like_count': 4,
                'media_type': 'IMAGE',
                'media_url': 'media_url',
                'owner': {'id': self.instagram_business_id},
                'permalink': 'permalink',
                'shortcode': 'BuGD8NmF4KI',
                'timestamp': '2019-02-20T07:10:15+0000',
                'username': 'username'
            }
        )

        media_info = self.api.get_media_info(media_id=media_id)
        self.assertEqual(media_id, media_info.id)

        media_info_json = self.api.get_media_info(media_id=media_id, return_json=True)
        self.assertEqual(media_id, media_info_json['id'])
