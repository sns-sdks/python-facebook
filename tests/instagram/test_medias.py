import json
import unittest
import pyfacebook


class MediaTest(unittest.TestCase):
    SIMPLE_OWNER_DATA = """{"caption": "Snowing.", "comments_count": 1, "id": "17861821972334188", "ig_id": "1983290017809138312", "is_comment_enabled": true, "like_count": 1, "media_type": "IMAGE", "media_url": "https://scontent.xx.fbcdn.net/v/t51.2885-15/50529291_298375090811167_6500976935770745294_n.jpg?_nc_cat=111&_nc_ht=scontent.xx&oh=aad092e19abb40932de0847bf0c60a74&oe=5CECBE1C", "owner": {"id": "17841406338772941"}, "permalink": "https://www.instagram.com/p/BuGD8NmF4KI/", "shortcode": "BuGD8NmF4KI", "timestamp": "2019-02-20T07:10:15+0000", "username": "ikroskun"}"""
    SIMPLE_PUBLIC_DATA = """{"caption": "Jay Chou in the house I mean, on the streets haha #streetstyle #ootd #bronx #adapt", "children": {"data": [{"id": "18018677311102004", "media_type": "IMAGE", "media_url": "https://scontent.xx.fbcdn.net/v/t51.2885-15/50908538_541383089707125_574808454302592798_n.jpg?_nc_cat=100&_nc_ht=scontent.xx&oh=33baf522e760847c098304ba26d2dd5b&oe=5CDAB60C", "permalink": "https://www.instagram.com/p/Bt6SyE7n00A/", "timestamp": "2019-02-15T17:29:03+0000"}, {"id": "17870453980312780", "media_type": "IMAGE", "media_url": "https://scontent.xx.fbcdn.net/v/t51.2885-15/52759760_252976635625098_7191782999214954453_n.jpg?_nc_cat=105&_nc_ht=scontent.xx&oh=9c625e054dd980efcb514251df4a15c1&oe=5CE98A6D", "permalink": "https://www.instagram.com/p/Bt6SyE7HdgG/", "timestamp": "2019-02-15T17:29:03+0000"}, {"id": "18033931885009831", "media_type": "IMAGE", "media_url": "https://scontent.xx.fbcdn.net/v/t51.2885-15/51139354_2056620461095674_4689084328987720377_n.jpg?_nc_cat=102&_nc_ht=scontent.xx&oh=ab4a4c66be17f034c00feec9e75e5d5f&oe=5D2297A4", "permalink": "https://www.instagram.com/p/Bt6SyE6HiNH/", "timestamp": "2019-02-15T17:29:03+0000"}]}, "comments_count": 1211, "id": "18000503476161727", "like_count": 112631, "media_type": "CAROUSEL_ALBUM", "media_url": "https://scontent.xx.fbcdn.net/v/t51.2885-15/50908538_541383089707125_574808454302592798_n.jpg?_nc_cat=100&_nc_ht=scontent.xx&oh=33baf522e760847c098304ba26d2dd5b&oe=5CDAB60C", "permalink": "https://www.instagram.com/p/Bt6SyHmnGyn/", "timestamp": "2019-02-15T17:29:04+0000", "username": "jaychou"}"""

    def _load_owner_data(self):
        return pyfacebook.InstagramMedia(
            caption="Snowing.",
            comments_count=1,
            id='17861821972334188',
            ig_id='1983290017809138312',
            is_comment_enabled=True,
            like_count=1,
            media_type='IMAGE',
            media_url='https://scontent.xx.fbcdn.net/v/t51.2885-15/50529291_298375090811167_6500976935770745294_n.jpg?_nc_cat=111&_nc_ht=scontent.xx&oh=aad092e19abb40932de0847bf0c60a74&oe=5CECBE1C',
            owner={'id': '17841406338772941'},
            permalink='https://www.instagram.com/p/BuGD8NmF4KI/',
            shortcode='BuGD8NmF4KI',
            timestamp='2019-02-20T07:10:15+0000',
            username='ikroskun'
        )

    def _load_public_data(self):
        return pyfacebook.InstagramMedia(
            caption='Jay Chou in the house I mean, on the streets haha #streetstyle #ootd #bronx #adapt',
            children={'data': [
                {'id': '18018677311102004',
                 'media_type': 'IMAGE',
                 'media_url': 'https://scontent.xx.fbcdn.net/v/t51.2885-15/50908538_541383089707125_574808454302592798_n.jpg?_nc_cat=100&_nc_ht=scontent.xx&oh=33baf522e760847c098304ba26d2dd5b&oe=5CDAB60C',
                 'permalink': 'https://www.instagram.com/p/Bt6SyE7n00A/',
                 'timestamp': '2019-02-15T17:29:03+0000'},
                {'id': '17870453980312780',
                 'media_type': 'IMAGE',
                 'media_url': 'https://scontent.xx.fbcdn.net/v/t51.2885-15/52759760_252976635625098_7191782999214954453_n.jpg?_nc_cat=105&_nc_ht=scontent.xx&oh=9c625e054dd980efcb514251df4a15c1&oe=5CE98A6D',
                 'permalink': 'https://www.instagram.com/p/Bt6SyE7HdgG/',
                 'timestamp': '2019-02-15T17:29:03+0000'},
                {'id': '18033931885009831',
                 'media_type': 'IMAGE',
                 'media_url': 'https://scontent.xx.fbcdn.net/v/t51.2885-15/51139354_2056620461095674_4689084328987720377_n.jpg?_nc_cat=102&_nc_ht=scontent.xx&oh=ab4a4c66be17f034c00feec9e75e5d5f&oe=5D2297A4',
                 'permalink': 'https://www.instagram.com/p/Bt6SyE6HiNH/',
                 'timestamp': '2019-02-15T17:29:03+0000'}
            ]},
            comments_count=1211,
            id='18000503476161727',
            like_count=112631,
            media_type='CAROUSEL_ALBUM',
            media_url='https://scontent.xx.fbcdn.net/v/t51.2885-15/50908538_541383089707125_574808454302592798_n.jpg?_nc_cat=100&_nc_ht=scontent.xx&oh=33baf522e760847c098304ba26d2dd5b&oe=5CDAB60C',
            permalink='https://www.instagram.com/p/Bt6SyHmnGyn/',
            timestamp='2019-02-15T17:29:04+0000',
            username='jaychou',
        )

    def testBuildMediaModel(self):
        owner_media = pyfacebook.InstagramMedia.new_from_json_dict(json.loads(self.SIMPLE_OWNER_DATA))
        self.assertEqual({'id': '17841406338772941'}, owner_media.owner)
        public_media = pyfacebook.InstagramMedia.new_from_json_dict(json.loads(self.SIMPLE_PUBLIC_DATA))
        self.assertEqual('18000503476161727', public_media.id)

    def testAsDict(self):
        owner_media = self._load_owner_data()
        owner_data = owner_media.as_dict()
        self.assertEqual('17861821972334188', owner_data['id'])
        self.assertEqual(1, owner_data['like_count'])
        public_media = self._load_public_data()
        public_data = public_media.as_dict()
        self.assertEqual(1211, public_data['comments_count'])

    def testAsJsonString(self):
        self.assertEqual(self.SIMPLE_OWNER_DATA, self._load_owner_data().as_json_string())
        self.assertEqual(self.SIMPLE_PUBLIC_DATA, self._load_public_data().as_json_string())
