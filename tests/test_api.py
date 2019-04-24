# coding=utf-8

from __future__ import unicode_literals, print_function

import unittest
import pyfacebook

import responses

DEFAULT_GRAPH_URL = "https://graph.facebook.com/"
DEFAULT_GRAPH_VERSION = 'v3.2'


class ApiCallTest(unittest.TestCase):
    @responses.activate
    def setUp(self):
        responses.add(
            method=responses.GET,
            url=DEFAULT_GRAPH_URL + DEFAULT_GRAPH_VERSION + '/oauth/access_token',
            json={'access_token': 'testToken'}
        )

        self.api = pyfacebook.Api(
            app_id='test',
            app_secret='test',
            short_token='test',
            version='3.2',
            timeout=1,
            interval_between_request=1,
            sleep_on_rate_limit=True
        )

    @responses.activate
    def testGetPageInfo(self):
        page_id = '123456789'
        responses.add(
            method=responses.GET,
            url=DEFAULT_GRAPH_URL + DEFAULT_GRAPH_VERSION + '/' + page_id,
            json={
                'about': 'about',
                'category': 'category',
                'category_list': [{
                    'id': 'category_id',
                    'name': 'category_name'
                }],
                'checkins': 1,
                'cover': {
                    'cover_id': 'cover_cover_id',
                    'id': 'cover_id',
                    'offset_x': 50,
                    'offset_y': 50,
                    'source': 'cover_source'
                },
                'description': 'description',
                'description_html': 'description_html',
                'engagement': {
                    'count': 49788740,
                    'social_sentence': '49M people like this.'},
                'fan_count': 49788740,
                'global_brand_page_name': 'global_brand_page_name',
                'id': '123456789',
                'link': 'link',
                'name': 'name',
                'username': 'username',
                'verification_status': u'blue_verified',
                'website': 'website'
            }
        )
        page_info = self.api.get_page_info(page_id=page_id)
        self.assertEqual('about', page_info.about)
        self.assertEqual(49788740, page_info.engagement['count'])

    @responses.activate
    def testGetPostInfo(self):
        post_id = '123456789_123456789'
        responses.add(
            method=responses.GET,
            url=DEFAULT_GRAPH_URL + DEFAULT_GRAPH_VERSION + '/' + post_id,
            json={
                'angry': {'data': [], 'summary': {'total_count': 1}},
                'attachments': {
                    'data': [{
                        'media': {
                            'image': {
                                'height': 274,
                                'src': 'image_src',
                                'width': 720
                            }
                        },
                        'target': {
                            'id': '114219621960016',
                            'url': 'url'
                        },
                        'title': u"'s cover photo",
                        'type': 'cover_photo',
                        'url': 'url'
                    }]
                },
                'comments': {
                    'data': [],
                    'summary': {
                        'can_comment': True,
                        'order': 'ranked',
                        'total_count': 111
                    }
                },
                'created_time': '2019-04-09T05:56:49+0000',
                'full_picture': 'full_picture',
                'haha': {'data': [], 'summary': {'total_count': 9}},
                'icon': 'https://www.facebook.com/images/icons/photo.gif',
                'id': post_id,
                'like': {'data': [], 'summary': {'total_count': 1717}},
                'link': 'link',
                'love': {'data': [], 'summary': {'total_count': 154}},
                'name': u"'s cover photo",
                'permalink_url': 'permalink_url',
                'picture': 'picture',
                'reactions': {
                    'data': [],
                    'summary': {'total_count': 1948, 'viewer_reaction': 'NONE'}
                },
                'sad': {'data': [], 'summary': {'total_count': 3}},
                'shares': {'count': 41},
                'status_type': 'added_photos',
                'thankful': {'data': [], 'summary': {'total_count': 0}},
                'type': 'photo',
                'updated_time': '2019-04-19T08:39:59+0000',
                'wow': {'data': [], 'summary': {'total_count': 64}}

            }
        )

        post_info = self.api.get_post_info(post_id=post_id)

        self.assertEqual(post_id, post_info.id)
        self.assertEqual(1717, post_info.like)
