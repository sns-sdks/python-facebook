import json
import unittest

import pyfacebook.models as models


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
    with open(BASE_PATH + "ig_insight.json", "rb") as f:
        IG_INSIGHT = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "ig_story.json", "rb") as f:
        IG_STORY = json.loads(f.read().decode("utf-8"))

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

    def testInsight(self):
        m = models.IgProInsight.new_from_json_dict(self.IG_INSIGHT)

        self.assertEqual(m.name, "impressions")
        self.assertEqual(m.id, "instagram_business_account_id/insights/impressions/day")
        self.assertEqual(len(m.values), 2)
        self.assertEqual(m.values[0].value, 32)

    def testStory(self):
        m = models.IgProStory.new_from_json_dict(self.IG_STORY)

        self.assertEqual(m.id, "17908009870517752")
        self.assertEqual(m.owner.id, "17841406338772941")
