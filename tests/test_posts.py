import json
import unittest
import pyfacebook


class PostsTest(unittest.TestCase):
    SIMPLE_DATA = """{"angry": 15, "attachments": {"data": [{"subattachments": {"data": [{"target": {"id": "249705015653756"}, "title": "Read about Sharks", "type": "option"}, {"target": {"id": "1880667495571868"}, "title": "Swim with Sharks", "type": "option"}]}, "target": {"id": "10157619579666729", "url": "https://www.facebook.com/20531316728/posts/10157619579666729/"}, "title": "Would you rather swim with sharks in the Pacific Ocean or read about sharks by the swimming pool?", "type": "visual_poll", "url": "https://www.facebook.com/20531316728/posts/10157619579666729/"}]}, "caption": null, "child_attachments": null, "comments": 1018, "created_time": "2018-08-16T13:00:33+0000", "description": null, "full_picture": null, "haha": 561, "icon": null, "id": "20531316728_10157619579661729", "like": 5492, "link": null, "love": 248, "message": "Would you rather swim with sharks in the Pacific Ocean or read about sharks by the swimming pool?", "name": null, "permalink_url": "https://www.facebook.com/20531316728/posts/10157619579661729/", "picture": null, "reactions": 6404, "sad": 9, "shares": 411, "source": null, "status_type": "mobile_status_update", "thankful": 0, "type": "status", "updated_time": "2019-01-09T18:47:36+0000", "wow": 79}"""

    def _load_simple_post(self):
        return pyfacebook.Post(
            id='20531316728_10157619579661729',
            attachments={'data': [
                {
                    'subattachments': {
                        'data': [
                            {
                                'target': {'id': '249705015653756'},
                                'title': 'Read about Sharks',
                                'type': 'option'
                            },
                            {
                                'target': {'id': '1880667495571868'},
                                'title': 'Swim with Sharks',
                                'type': 'option'
                            }]
                    },
                    'target': {'id': '10157619579666729',
                               'url': 'https://www.facebook.com/20531316728/posts/10157619579666729/'},
                    'title': 'Would you rather swim with sharks in the Pacific Ocean or read about sharks by the swimming pool?',
                    'type': 'visual_poll',
                    'url': 'https://www.facebook.com/20531316728/posts/10157619579666729/'
                }]
            },
            created_time='2018-08-16T13:00:33+0000',
            description=None,
            message='Would you rather swim with sharks in the Pacific Ocean or read about sharks by the swimming pool?',
            permalink_url='https://www.facebook.com/20531316728/posts/10157619579661729/',
            picture=None,
            shares=411,
            type='status',
            status_type='mobile_status_update',
            updated_time='2019-01-09T18:47:36+0000',
            comments=1018,
            reactions=6404,
            like=5492,
            love=248,
            wow=79,
            haha=561,
            sad=9,
            angry=15,
            thankful=0
        )

    def testProperties(self):
        """ test the page model's properties """
        post = pyfacebook.Post()
        post.id = '20531316728_10157619579661729'
        post.created_time = '2018-08-16T13:00:33+0000'
        post.permalink_url = 'https://www.facebook.com/20531316728/posts/10157619579661729/'
        post.type = 'status'

        self.assertEqual('20531316728_10157619579661729', post.id)

        self.assertEqual('2018-08-16T13:00:33+0000', post.created_time)

        self.assertEqual(
            'https://www.facebook.com/20531316728/posts/10157619579661729/',
            post.permalink_url,
        )
        self.assertEqual('status', post.type)

    def testBuildPostMode(self):
        post = pyfacebook.Post.new_from_json_dict(json.loads(self.SIMPLE_DATA))
        self.assertEqual('20531316728_10157619579661729', post.id)

    def testAsDict(self):
        page = self._load_simple_post()
        data = page.as_dict()
        self.assertEqual('20531316728_10157619579661729', data['id'])
        self.assertEqual(6404, data['reactions'])

    def testAsJsonString(self):
        self.assertEqual(self.SIMPLE_DATA, self._load_simple_post().as_json_string())

