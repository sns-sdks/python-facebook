import json
import unittest

import pyfacebook.models as models


class IgBasicModelTest(unittest.TestCase):
    BASE_PATH = "testdata/instagram_basic/models/"

    with open(BASE_PATH + 'user_info.json', 'rb') as f:
        USER_INFO = json.loads(f.read().decode('utf-8'))
    with open(BASE_PATH + 'media_info.json', 'rb') as f:
        MEDIA_INFO = json.loads(f.read().decode("utf-8"))

    def testBasicUser(self):
        m = models.IgBasicUser.new_from_json_dict(self.USER_INFO)

        self.assertEqual(m.account_type, "BUSINESS")
        self.assertEqual(m.media_count, 10)

    def testBasicMedia(self):
        m = models.IgBasicMedia.new_from_json_dict(self.MEDIA_INFO)

        self.assertEqual(m.id, "18027939643230671")
        self.assertEqual(m.media_type, "CAROUSEL_ALBUM")
        self.assertEqual(len(m.children), 2)
        self.assertEqual(m.children[0].id, "17895013408404508")
        self.assertEqual(m.children[0].media_type, "IMAGE")
