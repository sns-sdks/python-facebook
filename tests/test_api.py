# coding=utf-8

from __future__ import unicode_literals, print_function

import json
import unittest
import pyfacebook

import responses

DEFAULT_GRAPH_URL = "https://graph.facebook.com/"
EXCHANGE_ACCESS_TOKEN_URL = pyfacebook.Api.EXCHANGE_ACCESS_TOKEN_URL
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

    def testApiVersion(self):
        with self.assertRaises(pyfacebook.PyFacebookError):
            pyfacebook.Api(long_term_token='token', version='3.0')
        pyfacebook.Api(long_term_token='token', version='77')

    @responses.activate
    def testAuth(self):
        with self.assertRaises(pyfacebook.PyFacebookError):
            self.api.exchange_access_token('')

        with self.assertRaises(pyfacebook.PyFacebookError):
            api = pyfacebook.Api(long_term_token='token')
            api.get_authorization_url()

        url, state = self.api.get_authorization_url()
        self.assertEqual(state, 'PyFacebook')

        with open(self.base_path + 'auth_access_token.json', 'rb') as f:
            auth_access_token = json.loads(f.read().decode('utf-8'))
        responses.add(
            method=responses.POST,
            url=EXCHANGE_ACCESS_TOKEN_URL, json=auth_access_token
        )

        redirect_response = (
            'https://localhost/?code=code&state=PyFacebook'
        )
        access_token_data = self.api.exchange_access_token(redirect_response)
        self.assertEqual(access_token_data.access_token, 'access_token')
        access_token_json = self.api.exchange_access_token(redirect_response, return_json=True)
        self.assertEqual(access_token_json["access_token"], 'access_token')

    @responses.activate
    def testResponse(self):
        page_id = '20531316728'
        responses.add(
            url=DEFAULT_GRAPH_URL + DEFAULT_GRAPH_VERSION + '/' + page_id,
            method=responses.GET, body=''
        )
        responses.add(
            url=DEFAULT_GRAPH_URL + DEFAULT_GRAPH_VERSION + '/' + page_id,
            method=responses.GET, json={'error': 'error'}
        )
        with self.assertRaises(pyfacebook.PyFacebookError):
            self.api.get_page_info(page_id=page_id)
        with self.assertRaises(pyfacebook.PyFacebookError):
            self.api.get_page_info(page_id=page_id)

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

        with self.assertRaises(pyfacebook.PyFacebookError):
            self.api.get_page_info()

        page_info = self.api.get_page_info(page_id=page_id)
        self.assertEqual(page_info.id, page_id)
        self.assertEqual(page_info.engagement.count, 214429223)

        page_info = self.api.get_page_info(page_id=page_id, return_json=True)
        self.assertEqual(page_info['checkins'], 11)

        page_info_by_name = self.api.get_page_info(username=page_id)
        self.assertEqual(page_info_by_name.name, 'Facebook')
        self.assertEqual(page_info_by_name.picture.height, 50)

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

        with self.assertRaises(pyfacebook.PyFacebookError):
            self.api.get_post_info()

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
        responses.add(
            method=responses.GET,
            url=DEFAULT_GRAPH_URL + DEFAULT_GRAPH_VERSION + '/' + page_id + '/' + 'posts',
            json=posts_data
        )

        with open(self.base_path + 'posts_data_next.json', 'rb') as f:
            posts_data_next = json.loads(f.read().decode('utf-8'))
        responses.add(
            method=responses.GET,
            url=DEFAULT_GRAPH_URL + DEFAULT_GRAPH_VERSION + '/' + page_id + '/' + 'posts',
            json=posts_data_next
        )

        with self.assertRaises(pyfacebook.PyFacebookError):
            self.api.get_posts()

        posts = self.api.get_posts(page_id=page_id, count=4)

        self.assertEqual(len(posts), 4)
        self.assertEqual(posts[0].id, '20531316728_10158658756111729')

        posts = self.api.get_posts(username=page_id, count=8, return_json=True)
        self.assertEqual(len(posts), 8)
        self.assertEqual(posts[0]['id'], '20531316728_10158658756111729')

    @responses.activate
    def testGetComments(self):
        object_id = '20531316728_10158658756111729'

        with open(self.base_path + 'comments.json', 'rb') as f:
            comments_data = json.loads(f.read().decode('utf-8'))
        responses.add(
            method=responses.GET,
            url=DEFAULT_GRAPH_URL + DEFAULT_GRAPH_VERSION + '/' + object_id + '/' + 'comments',
            json=comments_data
        )

        with open(self.base_path + 'comments_next.json', 'rb') as f:
            comments_data_next = json.loads(f.read().decode('utf-8'))
        responses.add(
            method=responses.GET,
            url=DEFAULT_GRAPH_URL + DEFAULT_GRAPH_VERSION + '/' + object_id + '/' + 'comments',
            json=comments_data_next
        )

        with self.assertRaises(pyfacebook.PyFacebookError):
            self.api.get_comments()

        comments, summary = self.api.get_comments(object_id=object_id, summary=True, count=4)

        self.assertEqual(len(comments), 4)
        self.assertEqual(summary.order, 'chronological')

        comments, summary = self.api.get_comments(object_id=object_id, summary=True, count=8, return_json=True)

        self.assertEqual(len(comments), 8)
        self.assertEqual(summary['total_count'], 794)

    @responses.activate
    def testGetCommentInfo(self):
        comment_id = '10158658755326729_10158658760011729'

        with open(self.base_path + 'models/comment_info.json', 'rb') as f:
            comment_data = json.loads(f.read().decode('utf-8'))

        responses.add(
            method=responses.GET,
            url=DEFAULT_GRAPH_URL + DEFAULT_GRAPH_VERSION + '/' + comment_id,
            json=comment_data
        )

        with self.assertRaisesRegexp(pyfacebook.PyFacebookError, 'comment'):
            self.api.get_comment_info()

        comment_info = self.api.get_comment_info(comment_id=comment_id)
        self.assertEqual(comment_info.id, comment_id)
        self.assertEqual(comment_info._from, None)

        comment_info = self.api.get_comment_info(comment_id=comment_id, return_json=True)
        self.assertEqual(comment_info['like_count'], 7)

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

        with self.assertRaises(pyfacebook.PyFacebookError):
            self.api.get_picture()

        picture_info = self.api.get_picture(page_id=page_id)

        self.assertEqual(picture_info.height, 100)

        picture_info = self.api.get_picture(page_id=page_id, return_json=True)

        self.assertEqual(picture_info['height'], 100)

    @responses.activate
    def testExchangeToken(self):
        with self.assertRaises(pyfacebook.PyFacebookError):
            self.api.exchange_insights_token(token='token', page_id='')

        page_id = '20531316728'
        with open(self.base_path + 'page_access_token.json', 'rb') as f:
            access_token_data = json.loads(f.read().decode('utf-8'))
        # correct response mock
        responses.add(
            method=responses.GET,
            url=DEFAULT_GRAPH_URL + DEFAULT_GRAPH_VERSION + '/' + page_id,
            json=access_token_data
        )
        # error response mock
        responses.add(
            method=responses.GET,
            url=DEFAULT_GRAPH_URL + DEFAULT_GRAPH_VERSION + '/' + page_id,
            json={}
        )
        access_token = self.api.exchange_insights_token(token='token', page_id=page_id)
        self.assertEqual(access_token, access_token_data['access_token'])

        with self.assertRaises(pyfacebook.PyFacebookError):
            self.api.exchange_insights_token(token='', page_id=page_id)
            self.api.exchange_insights_token(token='token', page_id='')

        access_token = self.api.exchange_insights_token(token='token', page_id=page_id)
        self.assertTrue("the permission or your token" in access_token)

    @responses.activate
    def testGetPublishedPosts(self):
        page_id = '20531316728'
        with open(self.base_path + 'posts_published_data.json', 'rb') as f:
            posts_data = json.loads(f.read().decode('utf-8'))
        responses.add(
            method=responses.GET,
            url=DEFAULT_GRAPH_URL + DEFAULT_GRAPH_VERSION + '/' + page_id + '/' + 'published_posts',
            json=posts_data
        )
        responses.add(
            method=responses.GET,
            url=DEFAULT_GRAPH_URL + DEFAULT_GRAPH_VERSION + '/' + page_id + '/' + 'published_posts',
            json=posts_data
        )

        with open(self.base_path + 'posts_published_data_next.json', 'rb') as f:
            posts_data_next = json.loads(f.read().decode('utf-8'))
        responses.add(
            method=responses.GET,
            url=DEFAULT_GRAPH_URL + DEFAULT_GRAPH_VERSION + '/' + page_id + '/' + 'published_posts',
            json=posts_data_next
        )

        with self.assertRaises(pyfacebook.PyFacebookError):
            self.api.get_published_posts()

        posts = self.api.get_published_posts(page_id=page_id, count=4)
        self.assertEqual(len(posts), 4)
        self.assertEqual(posts[0].id, '20531316728_10158658756111729')

        posts = self.api.get_published_posts(page_id=page_id, count=8, return_json=True)
        self.assertEqual(len(posts), 8)
        self.assertEqual(posts[7]['id'], '20531316728_314949872489189')

    @responses.activate
    def testGetTaggedPosts(self):
        page_id = '20531316728'
        with open(self.base_path + 'posts_tagged_data.json', 'rb') as f:
            posts_data = json.loads(f.read().decode('utf-8'))
        responses.add(
            method=responses.GET,
            url=DEFAULT_GRAPH_URL + DEFAULT_GRAPH_VERSION + '/' + page_id + '/' + 'tagged',
            json=posts_data
        )
        responses.add(
            method=responses.GET,
            url=DEFAULT_GRAPH_URL + DEFAULT_GRAPH_VERSION + '/' + page_id + '/' + 'tagged',
            json=posts_data
        )

        with open(self.base_path + 'posts_tagged_data_next.json', 'rb') as f:
            posts_data_next = json.loads(f.read().decode('utf-8'))
        responses.add(
            method=responses.GET,
            url=DEFAULT_GRAPH_URL + DEFAULT_GRAPH_VERSION + '/' + page_id + '/' + 'tagged',
            json=posts_data_next
        )

        with self.assertRaises(pyfacebook.PyFacebookError):
            self.api.get_tagged_posts()

        posts = self.api.get_tagged_posts(page_id=page_id, count=3)
        self.assertEqual(len(posts), 3)
        self.assertEqual(posts[0].id, '20531316728_10158658756111729')
        self.assertEqual(posts[0].tagged_time, '2019-08-16T11:18:58+0000')

        posts = self.api.get_tagged_posts(page_id=page_id, count=7, return_json=True)
        self.assertEqual(len(posts), 7)
        self.assertEqual(posts[6]['id'], '20531316728_381805782375907')

    @responses.activate
    def testGetFeedPosts(self):
        page_id = '20531316728'
        with open(self.base_path + 'posts_feeds_data.json', 'rb') as f:
            posts_data = json.loads(f.read().decode('utf-8'))
        responses.add(
            method=responses.GET,
            url=DEFAULT_GRAPH_URL + DEFAULT_GRAPH_VERSION + '/' + page_id + '/' + 'feed',
            json=posts_data
        )
        responses.add(
            method=responses.GET,
            url=DEFAULT_GRAPH_URL + DEFAULT_GRAPH_VERSION + '/' + page_id + '/' + 'feed',
            json=posts_data
        )

        with open(self.base_path + 'posts_feeds_data_next.json', 'rb') as f:
            posts_data_next = json.loads(f.read().decode('utf-8'))
        responses.add(
            method=responses.GET,
            url=DEFAULT_GRAPH_URL + DEFAULT_GRAPH_VERSION + '/' + page_id + '/' + 'feed',
            json=posts_data_next
        )

        with self.assertRaises(pyfacebook.PyFacebookError):
            self.api.get_feeds()

        posts = self.api.get_feeds(page_id=page_id, count=2)
        self.assertEqual(len(posts), 2)
        self.assertEqual(posts[0].id, '20531316728_10158658756111729')

        posts = self.api.get_feeds(page_id=page_id, count=6, return_json=True)
        self.assertEqual(len(posts), 6)
        self.assertEqual(posts[5]['id'], '20531316728_10158137001326729')
