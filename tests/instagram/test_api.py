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
    # BASE_PATH = '../../testdata/instagram/'

    with open(BASE_PATH + 'business_user.json', 'rb') as f:
        BUSINESS_USER_INFO = json.loads(f.read().decode('utf-8'))
    with open(BASE_PATH + 'business_user_media.json', 'rb') as f:
        BUSINESS_USER_MEDIA = json.loads(f.read().decode('utf-8'))
    with open(BASE_PATH + 'business_user_media_2.json', 'rb') as f:
        BUSINESS_USER_MEDIA_2 = json.loads(f.read().decode('utf-8'))
    with open(BASE_PATH + 'owner_user_info.json', 'rb') as f:
        OWNER_USER_INFO = json.loads(f.read().decode('utf-8'))
    with open(BASE_PATH + 'owner_user_info_with_media.json', 'rb') as f:
        OWNER_USER_INFO_WITH_MEDIA = json.loads(f.read().decode('utf-8'))
    with open(BASE_PATH + 'owner_medias.json', 'rb') as f:
        OWNER_MEDIAS = json.loads(f.read().decode('utf-8'))
    with open(BASE_PATH + 'owner_medias_2.json', 'rb') as f:
        OWNER_MEDIAS_2 = json.loads(f.read().decode('utf-8'))
    with open(BASE_PATH + 'owner_media_info.json', 'rb') as f:
        OWNER_MEDIA_INFO = json.loads(f.read().decode('utf-8'))
    with open(BASE_PATH + 'owner_media_comments.json', 'rb') as f:
        OWNER_MEDIA_COMMENTS = json.loads(f.read().decode('utf-8'))
    with open(BASE_PATH + 'owner_media_comments_2.json', 'rb') as f:
        OWNER_MEDIA_COMMENTS_2 = json.loads(f.read().decode('utf-8'))
    with open(BASE_PATH + 'owner_media_comment_info.json', 'rb') as f:
        OWNER_MEDIA_COMMENT_INFO = json.loads(f.read().decode('utf-8'))
    with open(BASE_PATH + 'owner_replies.json', 'rb') as f:
        OWNER_REPLIES = json.loads(f.read().decode('utf-8'))
    with open(BASE_PATH + 'owner_replies_2.json', 'rb') as f:
        OWNER_REPLIES_2 = json.loads(f.read().decode('utf-8'))
    with open(BASE_PATH + 'owner_reply_info.json', 'rb') as f:
        OWNER_REPLY_INFO = json.loads(f.read().decode('utf-8'))

    def setUp(self):
        self.prefix_url = self.DEFAULT_GRAPH_URL + self.DEFAULT_GRAPH_VERSION
        self.api = pyfacebook.InstagramApi(
            long_term_token='token',
            instagram_business_id='17841406338772941'
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

    @responses.activate
    def testGetUserInfo(self):
        with responses.RequestsMock() as m:
            m.add(
                'GET', url=self.prefix_url + '/' + self.api.instagram_business_id,
                json=self.OWNER_USER_INFO
            )
            m.add(
                'GET', url=self.prefix_url + '/' + self.api.instagram_business_id,
                json=self.OWNER_USER_INFO_WITH_MEDIA
            )
            user_info = self.api.get_user_info()
            self.assertEqual(user_info.id, '17841406338772941')
            user_info_with_media = self.api.get_user_info(
                user_id='17841406338772941', include_media=True,
                access_token='user_access_token', return_json=True
            )
            self.assertEqual(user_info_with_media['id'], '17841406338772941')
            self.assertEqual(len(user_info_with_media['media']['data']), 8)

    @responses.activate
    def testGetMedias(self):
        with responses.RequestsMock() as m:
            m.add(
                'GET', url=self.prefix_url + '/' + self.api.instagram_business_id + '/media',
                json=self.OWNER_MEDIAS
            )
            m.add(
                'GET', url=self.prefix_url + '/' + self.api.instagram_business_id + '/media',
                json=self.OWNER_MEDIAS_2
            )

            medias = self.api.get_medias(
                user_id='17841406338772941', include_comment=True, access_token='token',
                since_time='2019-1-1', until_time='2019-10-24')
            self.assertEqual(len(medias), 3)

            medias = self.api.get_medias(count=1, return_json=True)
            self.assertEqual(len(medias), 1)

            with self.assertRaises(pyfacebook.PyFacebookError):
                self.api.get_medias('17841406338772941', since_time='2019')
                self.api.discovery_user_medias('17841406338772941', until_time='2019')

    @responses.activate
    def testGetMediaInfo(self):
        media_id = '18075344632131157'
        with responses.RequestsMock() as m:
            m.add(
                'GET', url=self.prefix_url + '/' + media_id,
                json=self.OWNER_MEDIA_INFO
            )

            media_info = self.api.get_media_info(
                media_id=media_id, access_token='token',
                include_comment=True
            )
            self.assertEqual(media_info.id, media_id)

            media_info_json = self.api.get_media_info(media_id=media_id, return_json=True)
            self.assertEqual(media_info_json['comments_count'], 1)

    @responses.activate
    def testGetComments(self):
        media_id = '17955956875141196'
        with responses.RequestsMock() as m:
            m.add(
                'GET', url=self.prefix_url + '/' + media_id + '/comments',
                json=self.OWNER_MEDIA_COMMENTS
            )
            m.add(
                'GET', url=self.prefix_url + '/' + media_id + '/comments',
                json=self.OWNER_MEDIA_COMMENTS_2
            )

            comments = self.api.get_comments(
                media_id=media_id, access_token='token',
                include_replies=True, limit=3
            )
            self.assertEqual(len(comments), 5)
            comments_json = self.api.get_comments(media_id=media_id, count=1, return_json=True)
            self.assertEqual(len(comments_json), 1)

    @responses.activate
    def testGetCommentInfo(self):
        comment_id = '17984127178281340'

        with responses.RequestsMock() as m:
            m.add(
                'GET', url=self.prefix_url + '/' + comment_id,
                json=self.OWNER_MEDIA_COMMENT_INFO
            )

            comment_info = self.api.get_comment_info(
                comment_id=comment_id, access_token='token',
                include_replies=True,
            )
            self.assertEqual(comment_info.id, comment_id)

            comment_info_json = self.api.get_comment_info(comment_id=comment_id, return_json=True)
            self.assertEqual(comment_info_json['like_count'], 0)
            self.assertEqual(len(comment_info_json['replies']['data']), 3)

    @responses.activate
    def testGetReplies(self):
        comment_id = '17984127178281340'
        with responses.RequestsMock() as m:
            m.add(
                'GET', url=self.prefix_url + '/' + comment_id + '/replies',
                json=self.OWNER_REPLIES
            )
            m.add(
                'GET', url=self.prefix_url + '/' + comment_id + '/replies',
                json=self.OWNER_REPLIES_2
            )

            replies = self.api.get_replies(
                comment_id=comment_id, access_token='token', limit=2
            )
            self.assertEqual(len(replies), 3)
            replies_json = self.api.get_replies(comment_id=comment_id, count=1, return_json=True)
            self.assertEqual(len(replies_json), 1)

    @responses.activate
    def testGetReplyInfo(self):
        reply_id = '18025866040229880'
        with responses.RequestsMock() as m:
            m.add(
                'GET', url=self.prefix_url + '/' + reply_id,
                json=self.OWNER_REPLY_INFO
            )
            reply_info = self.api.get_reply_info(
                reply_id=reply_id, access_token='token'
            )
            self.assertEqual(reply_info.id, reply_id)
            reply_info_json = self.api.get_reply_info(reply_id=reply_id, return_json=True)
            self.assertEqual(reply_info_json['like_count'], 0)
