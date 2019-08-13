# coding=utf-8

from __future__ import unicode_literals, print_function

import json
import unittest
import pyfacebook

import responses

DEFAULT_GRAPH_URL = "https://graph.facebook.com/"
DEFAULT_GRAPH_VERSION = pyfacebook.Api.VALID_API_VERSIONS[-1]


class ApiCallTest(unittest.TestCase):
    @responses.activate
    def setUp(self):
        self.base_path = 'testdata/facebook/'

        with open(self.base_path + 'exchange_token.json', 'rb') as f:
            token_data = json.loads(f.read().decode('utf-8'))

        responses.add(
            method=responses.GET,
            url=DEFAULT_GRAPH_URL + DEFAULT_GRAPH_VERSION + '/oauth/access_token',
            json=token_data
        )

        self.api = pyfacebook.Api(
            app_id='test',
            app_secret='test',
            short_token='test',
            version=DEFAULT_GRAPH_VERSION,
            timeout=1,
            interval_between_request=1,
            sleep_on_rate_limit=True
        )

    @responses.activate
    def testGetPageInfo(self):
        page_id = '20531316728'
        with open(self.base_path + 'page_info.json', 'rb') as f:
            page_data = json.loads(f.read().decode('utf-8'))
        responses.add(
            method=responses.GET,
            url=DEFAULT_GRAPH_URL + DEFAULT_GRAPH_VERSION + '/' + page_id,
            json=page_data
        )

        self.assertRaises(
            pyfacebook.PyFacebookError,
            lambda: self.api.get_page_info()
        )

        page_info = self.api.get_page_info(page_id=page_id)
        self.assertEqual(page_info.id, page_id)
        self.assertEqual(page_info.engagement.count, 214429223)

        page_info = self.api.get_page_info(page_id=page_id, return_json=True)
        self.assertEqual(page_info['checkins'], 11)

        page_info_by_name = self.api.get_page_info(username=page_id)
        self.assertEqual(page_info_by_name.name, 'Facebook')

    @responses.activate
    def testGetPostInfo(self):
        post_id = '20531316728_10158658756111729'

        with open(self.base_path + 'post_info.json', 'rb') as f:
            post_data = json.loads(f.read().decode('utf-8'))

        responses.add(
            method=responses.GET,
            url=DEFAULT_GRAPH_URL + DEFAULT_GRAPH_VERSION + '/' + post_id,
            json=post_data
        )

        self.assertRaises(
            pyfacebook.PyFacebookError,
            lambda: self.api.get_post_info()
        )

        post_info = self.api.get_post_info(post_id=post_id)

        self.assertEqual(post_info.id, post_id)
        self.assertEqual(post_info.reactions.total_count, 8225)

        post_info = self.api.get_post_info(post_id=post_id, return_json=True)
        self.assertEqual(post_id, post_info['id'])

    @responses.activate
    def testGetPosts(self):
        page_id = '20531316728'

        with open(self.base_path + 'posts_data.json', 'rb') as f:
            posts_data = json.loads(f.read().decode('utf-8'))
        responses.add(
            method=responses.GET,
            url=DEFAULT_GRAPH_URL + DEFAULT_GRAPH_VERSION + '/' + page_id + '/' + 'posts',
            json=posts_data
        )

        with open(self.base_path + 'posts_data.json', 'rb') as f:
            posts_data_next = json.loads(f.read().decode('utf-8'))
        responses.add(
            method=responses.GET,
            url=DEFAULT_GRAPH_URL + DEFAULT_GRAPH_VERSION + '/' + page_id + '/' + 'posts/next',
            json=posts_data_next
        )

        self.assertRaises(
            pyfacebook.PyFacebookError,
            lambda: self.api.get_posts()
        )

        posts = self.api.get_posts(page_id=page_id, count=4)

        self.assertEqual(len(posts), 4)
        self.assertEqual(posts[0].id, '20531316728_10158658756111729')

        posts = self.api.get_posts(username=page_id, count=8, return_json=True)
        self.assertEqual(len(posts), 8)
        self.assertEqual(posts[0]['id'], '20531316728_10158658756111729')

    @responses.activate
    def testGetComments(self):
        object_id = '123456789'
        responses.add(
            method=responses.GET,
            url=DEFAULT_GRAPH_URL + DEFAULT_GRAPH_VERSION + '/' + object_id + '/' + 'comments',
            json={
                "data": [
                    {
                        "id": "123456789_123456789",
                        "created_time": "2019-04-09T05:57:32+0000",
                        "like_count": 0,
                        "message": "comment1",
                        "permalink_url": "permalink_url",
                        "comment_count": 0
                    },
                    {
                        "id": "123456789_12345678910",
                        "created_time": "2019-04-09T05:58:23+0000",
                        "like_count": 1,
                        "message": "comment2",
                        "permalink_url": "permalink_url",
                        "comment_count": 0
                    },
                    {
                        "id": "123456789_12345678911",
                        "created_time": "2019-04-09T05:58:30+0000",
                        "like_count": 5,
                        "message": "comment3",
                        "permalink_url": "permalink_url",
                        "comment_count": 1
                    },
                ],
                "paging": {
                    "cursors": {
                        "before": "before",
                        "after": "before"
                    },
                    "next": "https://graph.facebook.com/{}/123456789/comments/next".format(DEFAULT_GRAPH_VERSION)
                },
                "summary": {
                    "order": "chronological",
                    "total_count": 108,
                    "can_comment": True
                }
            }
        )

        responses.add(
            method=responses.GET,
            url=DEFAULT_GRAPH_URL + DEFAULT_GRAPH_VERSION + '/' + object_id + '/' + 'comments/next',
            json={
                "data": [
                    {
                        "id": "123456789_123456789",
                        "created_time": "2019-04-09T05:57:32+0000",
                        "like_count": 0,
                        "message": "comment1",
                        "permalink_url": "permalink_url",
                        "comment_count": 0
                    },
                    {
                        "id": "123456789_12345678910",
                        "created_time": "2019-04-09T05:58:23+0000",
                        "like_count": 1,
                        "message": "comment2",
                        "permalink_url": "permalink_url",
                        "comment_count": 0
                    },
                    {
                        "id": "123456789_12345678911",
                        "created_time": "2019-04-09T05:58:30+0000",
                        "like_count": 5,
                        "message": "comment3",
                        "permalink_url": "permalink_url",
                        "comment_count": 1
                    },
                ],
                "paging": {
                    "cursors": {
                        "before": "before",
                        "after": "before"
                    },
                    # "next": "https://graph.facebook.com/v3.2/123456789/comments/next"
                },
                "summary": {
                    "order": "chronological",
                    "total_count": 108,
                    "can_comment": True
                }
            }
        )

        self.assertRaises(
            pyfacebook.PyFacebookError,
            lambda: self.api.get_comments()
        )

        comments, summary = self.api.get_comments(object_id=object_id, summary=True, count=4)

        self.assertEqual(4, len(comments))
        self.assertEqual('chronological', summary.order)

        comments, summary = self.api.get_comments(object_id=object_id, summary=True, count=5, return_json=True)

        self.assertEqual(5, len(comments))
        self.assertEqual(108, summary['total_count'])

    @responses.activate
    def testGetPicture(self):
        page_id = '20531316728'

        with open(self.base_path + 'page_picture.json', 'rb') as f:
            picture_data = json.loads(f.read().decode('utf-8'))
        responses.add(
            method=responses.GET,
            url=DEFAULT_GRAPH_URL + DEFAULT_GRAPH_VERSION + '/' + page_id + '/' + 'picture',
            json=picture_data
        )

        self.assertRaises(
            pyfacebook.PyFacebookError,
            lambda: self.api.get_picture()
        )

        picture_info = self.api.get_picture(page_id=page_id)

        self.assertEqual(picture_info.height, 100)

        picture_info = self.api.get_picture(page_id=page_id, return_json=True)

        self.assertEqual(picture_info['height'], 100)
