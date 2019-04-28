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
                'verification_status': 'blue_verified',
                'website': 'website'
            }
        )

        self.assertRaises(
            pyfacebook.PyFacebookError,
            lambda: self.api.get_page_info()
        )

        page_info = self.api.get_page_info(page_id=page_id)
        self.assertEqual('about', page_info.about)
        self.assertEqual(49788740, page_info.engagement['count'])

        page_info = self.api.get_page_info(page_id=page_id, return_json=True)
        self.assertEqual('about', page_info['about'])

        page_info_by_name = self.api.get_page_info(username=page_id)
        self.assertEqual('name', page_info_by_name.name)

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

        self.assertRaises(
            pyfacebook.PyFacebookError,
            lambda: self.api.get_post_info()
        )

        post_info = self.api.get_post_info(post_id=post_id)

        self.assertEqual(post_id, post_info.id)
        self.assertEqual(1717, post_info.like)

        post_info = self.api.get_post_info(post_id=post_id, return_json=True)
        self.assertEqual(post_id, post_info['id'])

    @responses.activate
    def testGetPosts(self):
        page_id = '123456789'
        responses.add(
            method=responses.GET,
            url=DEFAULT_GRAPH_URL + DEFAULT_GRAPH_VERSION + '/' + page_id + '/' + 'posts',
            json={
                'data': [
                    {
                        'angry': {'data': [], 'summary': {'total_count': 0}},
                        'attachments': {
                            'data': [{
                                'media': {
                                    'image': {
                                        'height': 405,
                                        'src': 'src',
                                        'width': 720
                                    }
                                },
                                'target': {
                                    'id': '123456789',
                                    'url': 'url'
                                },
                                'title': 'title',
                                'type': 'video_autoplay',
                                'url': 'url'
                            }]
                        },
                        'comments': {
                            'data': [],
                            'summary': {
                                'can_comment': True,
                                'order': 'ranked',
                                'total_count': 21
                            }
                        },
                        'created_time': '2019-04-24T05:00:21+0000',
                        'full_picture': 'full_picture',
                        'haha': {'data': [], 'summary': {'total_count': 1}},
                        'icon': 'https://www.facebook.com/images/icons/video.gif',
                        'id': '123456789_123456789',
                        'like': {'data': [], 'summary': {'total_count': 314}},
                        'link': 'link',
                        'love': {'data': [], 'summary': {'total_count': 38}},
                        'message': 'message',
                        'name': 'name',
                        'permalink_url': 'permalink_url',
                        'picture': 'picture',
                        'reactions': {
                            'data': [],
                            'summary': {'total_count': 362, 'viewer_reaction': 'NONE'}
                        },
                        'sad': {'data': [], 'summary': {'total_count': 0}},
                        'shares': {'count': 7},
                        'status_type': 'added_video',
                        'thankful': {'data': [], 'summary': {'total_count': 0}},
                        'type': 'video',
                        'updated_time': '2019-04-24T11:47:38+0000',
                        'wow': {'data': [], 'summary': {'total_count': 9}}},
                    {
                        'angry': {'data': [], 'summary': {'total_count': 0}},
                        'attachments': {
                            'data': [{
                                'media': {
                                    'image': {
                                        'height': 405,
                                        'src': 'src',
                                        'width': 720
                                    }
                                },
                                'target': {
                                    'id': '123456789',
                                    'url': 'url'
                                },
                                'title': 'title',
                                'type': 'video_autoplay',
                                'url': 'url'
                            }]
                        },
                        'comments': {
                            'data': [],
                            'summary': {
                                'can_comment': True,
                                'order': 'ranked',
                                'total_count': 27
                            }
                        },
                        'created_time': '2019-04-24T00:00:23+0000',
                        'full_picture': 'full_picture',
                        'haha': {'data': [], 'summary': {'total_count': 0}},
                        'icon': 'https://www.facebook.com/images/icons/video.gif',
                        'id': '123456789_12345678910',
                        'like': {'data': [], 'summary': {'total_count': 330}},
                        'link': 'link',
                        'love': {'data': [], 'summary': {'total_count': 44}},
                        'message': 'message',
                        'name': 'name',
                        'permalink_url': 'permalink_url',
                        'picture': 'picture',
                        'reactions': {
                            'data': [],
                            'summary': {'total_count': 386, 'viewer_reaction': 'NONE'}
                        },
                        'sad': {'data': [], 'summary': {'total_count': 0}},
                        'shares': {'count': 18},
                        'status_type': 'added_video',
                        'thankful': {'data': [], 'summary': {'total_count': 0}},
                        'type': 'video',
                        'updated_time': '2019-04-24T12:05:27+0000',
                        'wow': {'data': [], 'summary': {'total_count': 12}}},
                    {
                        'angry': {'data': [], 'summary': {'total_count': 1}},
                        'attachments': {
                            'data': [{
                                'media': {
                                    'image': {
                                        'height': 405,
                                        'src': 'src',
                                        'width': 720
                                    }
                                },
                                'target': {
                                    'id': '123456789',
                                    'url': 'url'
                                },
                                'title': 'url',
                                'type': 'video_autoplay',
                                'url': 'url'
                            }]
                        },
                        'comments': {
                            'data': [],
                            'summary': {
                                'can_comment': True,
                                'order': 'ranked',
                                'total_count': 43
                            }
                        },
                        'created_time': '2019-04-23T05:00:25+0000',
                        'full_picture': 'full_picture',
                        'haha': {'data': [], 'summary': {'total_count': 3}},
                        'icon': 'https://www.facebook.com/images/icons/video.gif',
                        'id': '123456789_12345678911',
                        'like': {'data': [], 'summary': {'total_count': 581}},
                        'link': 'link',
                        'love': {'data': [], 'summary': {'total_count': 66}},
                        'message': 'message',
                        'name': 'name',
                        'permalink_url': 'permalink_url',
                        'picture': 'picture',
                        'reactions': {
                            'data': [],
                            'summary': {'total_count': 677, 'viewer_reaction': 'NONE'}
                        },
                        'sad': {'data': [], 'summary': {'total_count': 1}},
                        'shares': {'count': 27},
                        'status_type': 'added_video',
                        'thankful': {'data': [], 'summary': {'total_count': 0}},
                        'type': 'video',
                        'updated_time': '2019-04-24T11:54:30+0000',
                        'wow': {'data': [], 'summary': {'total_count': 25}}}
                ],
                'paging': {
                    'cursors': {
                        'after': 'after',
                        'before': 'before'
                    },
                    'next': 'https://graph.facebook.com/v3.2/123456789/posts/next'}
            }
        )

        responses.add(
            method=responses.GET,
            url=DEFAULT_GRAPH_URL + DEFAULT_GRAPH_VERSION + '/' + page_id + '/' + 'posts/next?access_token=testToken',
            json={
                'data': [
                    {
                        'angry': {'data': [], 'summary': {'total_count': 0}},
                        'attachments': {
                            'data': [{
                                'media': {
                                    'image': {
                                        'height': 405,
                                        'src': 'src',
                                        'width': 720
                                    }
                                },
                                'target': {
                                    'id': '123456789',
                                    'url': 'url'
                                },
                                'title': 'title',
                                'type': 'video_autoplay',
                                'url': 'url'
                            }]
                        },
                        'comments': {
                            'data': [],
                            'summary': {
                                'can_comment': True,
                                'order': 'ranked',
                                'total_count': 21
                            }
                        },
                        'created_time': '2019-04-24T05:00:21+0000',
                        'full_picture': 'full_picture',
                        'haha': {'data': [], 'summary': {'total_count': 1}},
                        'icon': 'https://www.facebook.com/images/icons/video.gif',
                        'id': '123456789_12345678912',
                        'like': {'data': [], 'summary': {'total_count': 314}},
                        'link': 'link',
                        'love': {'data': [], 'summary': {'total_count': 38}},
                        'message': 'message',
                        'name': 'name',
                        'permalink_url': 'permalink_url',
                        'picture': 'picture',
                        'reactions': {
                            'data': [],
                            'summary': {'total_count': 362, 'viewer_reaction': 'NONE'}
                        },
                        'sad': {'data': [], 'summary': {'total_count': 0}},
                        'shares': {'count': 7},
                        'status_type': 'added_video',
                        'thankful': {'data': [], 'summary': {'total_count': 0}},
                        'type': 'video',
                        'updated_time': '2019-04-24T11:47:38+0000',
                        'wow': {'data': [], 'summary': {'total_count': 9}}},
                    {
                        'angry': {'data': [], 'summary': {'total_count': 0}},
                        'attachments': {
                            'data': [{
                                'media': {
                                    'image': {
                                        'height': 405,
                                        'src': 'src',
                                        'width': 720
                                    }
                                },
                                'target': {
                                    'id': '123456789',
                                    'url': 'url'
                                },
                                'title': 'title',
                                'type': 'video_autoplay',
                                'url': 'url'
                            }]
                        },
                        'comments': {
                            'data': [],
                            'summary': {
                                'can_comment': True,
                                'order': 'ranked',
                                'total_count': 27
                            }
                        },
                        'created_time': '2019-04-24T00:00:23+0000',
                        'full_picture': 'full_picture',
                        'haha': {'data': [], 'summary': {'total_count': 0}},
                        'icon': 'https://www.facebook.com/images/icons/video.gif',
                        'id': '123456789_1234567891013',
                        'like': {'data': [], 'summary': {'total_count': 330}},
                        'link': 'link',
                        'love': {'data': [], 'summary': {'total_count': 44}},
                        'message': 'message',
                        'name': 'name',
                        'permalink_url': 'permalink_url',
                        'picture': 'picture',
                        'reactions': {
                            'data': [],
                            'summary': {'total_count': 386, 'viewer_reaction': 'NONE'}
                        },
                        'sad': {'data': [], 'summary': {'total_count': 0}},
                        'shares': {'count': 18},
                        'status_type': 'added_video',
                        'thankful': {'data': [], 'summary': {'total_count': 0}},
                        'type': 'video',
                        'updated_time': '2019-04-24T12:05:27+0000',
                        'wow': {'data': [], 'summary': {'total_count': 12}}},
                ],
                'paging': {
                    'cursors': {
                        'after': 'after',
                        'before': 'before'
                    },
                    # 'next': 'https://graph.facebook.com/v3.2/123456789/posts/next'
                }
            }
        )

        self.assertRaises(
            pyfacebook.PyFacebookError,
            lambda: self.api.get_posts()
        )

        posts = self.api.get_posts(page_id=page_id, count=4)

        self.assertEqual(4, len(posts))
        self.assertEqual('123456789_123456789', posts[0].id)

        posts = self.api.get_posts(username=page_id, count=5, return_json=True)
        self.assertEqual(5, len(posts))
        self.assertEqual('123456789_123456789', posts[0]['id'])

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
                    "next": "https://graph.facebook.com/v3.2/123456789/comments/next"
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
        page_id = '123456789'

        responses.add(
            method=responses.GET,
            url=DEFAULT_GRAPH_URL + DEFAULT_GRAPH_VERSION + '/' + page_id + '/' + 'picture',
            json={
                'data': {
                    'height': 50,
                    'is_silhouette': False,
                    'url': 'url',
                    'width': 50
                }
            }
        )

        self.assertRaises(
            pyfacebook.PyFacebookError,
            lambda: self.api.get_picture()
        )

        picture_info = self.api.get_picture(page_id=page_id)

        self.assertEqual(50, picture_info.height)

        picture_info = self.api.get_picture(page_id=page_id, return_json=True)

        self.assertEqual(50, picture_info['height'])
