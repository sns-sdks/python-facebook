import json
import unittest

import pyfacebook.model as models


class IgProModelTest(unittest.TestCase):
    BASE_PATH = "testdata/instagram/models/"

    with open(BASE_PATH + 'ig_user.json', 'rb') as f:
        IG_USER = json.loads(f.read().decode('utf-8'))
    with open(BASE_PATH + 'ig_media.json', 'rb') as f:
        IG_MEDIA = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + 'ig_comment.json', 'rb') as f:
        IG_COMMENT = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + 'ig_reply.json', 'rb') as f:
        IG_REPLY = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + 'ig_hashtag.json', 'rb') as f:
        IG_HASHTAG = json.loads(f.read().decode("utf-8"))

    def testUser(self):
        m = models.IgProUser.new_from_json_dict(self.IG_USER)

        self.assertEqual(m.id, "17841406338772941")

    def testMedia(self):
        m = models.IgProMedia.new_from_json_dict(self.IG_MEDIA)

        self.assertEqual(m.comments_count, 6)
        self.assertEqual(len(m.children), 3)
        self.assertEqual(len(m.comments), 3)

    def testComment(self):
        m = models.IgProComment.new_from_json_dict(self.IG_COMMENT)

        self.assertEqual(m.like_count, 0)
        self.assertEqual(m.media.id, "17955956875141196")
        self.assertEqual(len(m.replies), 3)

    def testReply(self):
        m = models.IgProReply.new_from_json_dict(self.IG_REPLY)

        self.assertEqual(m.id, "18107567341036926")
        self.assertEqual(m.user.id, "17841406338772941")

    def testHashtag(self):
        m = models.IgProHashtag.new_from_json_dict(self.IG_HASHTAG)

        self.assertEqual(m.id, "17841593698074073")
