import json
import unittest

import responses
import pyfacebook


class ApiMentionTest(unittest.TestCase):
    BASE_PATH = "testdata/instagram/apidata/mentions/"
    BASE_URL = "https://graph.facebook.com/{}/".format(pyfacebook.Api.VALID_API_VERSIONS[-1])

    with open(BASE_PATH + "tagged_user_medias_p1.json", "rb") as f:
        TAGGED_USER_MEDIAS_P1 = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "tagged_user_medias_p2.json", "rb") as f:
        TAGGED_USER_MEDIAS_P2 = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "mention_user_comment.json", "rb") as f:
        MENTION_USER_COMMENT = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "mention_user_media.json", "rb") as f:
        MENTION_USER_MEDIA = json.loads(f.read().decode("utf-8"))

    def setUp(self):
        self.instagram_business_id = "17841406338772941"
        self.api = pyfacebook.IgProApi(
            app_id="123456", app_secret="secret",
            long_term_token="token"
        )

    def testGetTaggedUserMedias(self):
        # test get all medias

        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL + self.instagram_business_id + "/tags", json=self.TAGGED_USER_MEDIAS_P1)
            m.add("GET", self.BASE_URL + self.instagram_business_id + "/tags", json=self.TAGGED_USER_MEDIAS_P2)

            res = self.api.get_tagged_user_medias(
                user_id=self.instagram_business_id,
                count=None,
                limit=3,
            )
            self.assertEqual(len(res), 5)

        # test count
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL + self.instagram_business_id + "/tags", json=self.TAGGED_USER_MEDIAS_P1)
            m.add("GET", self.BASE_URL + self.instagram_business_id + "/tags", json=self.TAGGED_USER_MEDIAS_P2)

            res = self.api.get_tagged_user_medias(
                user_id=self.instagram_business_id,
                count=4,
                limit=3,
                access_token="token",
                return_json=True
            )
            self.assertEqual(len(res), 4)

    def testGetMentionedCommentInfo(self):
        comment_id = "17892250648466172"
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL + self.instagram_business_id, json=self.MENTION_USER_COMMENT)

            comment = self.api.get_mentioned_comment_info(
                user_id=self.instagram_business_id,
                comment_id=comment_id,
            )
            self.assertEqual(comment.id, comment_id)
            self.assertEqual(comment.media.id, "17846368219941692")

            comment_json = self.api.get_mentioned_comment_info(
                user_id=self.instagram_business_id,
                comment_id=comment_id,
                access_token="token",
                return_json=True
            )
            self.assertEqual(comment_json["id"], comment_id)
            self.assertEqual(comment_json["media"]["id"], "17846368219941692")

    def testGetMentionedMediaInfo(self):
        media_id = "18027939643230671"

        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL + self.instagram_business_id, json=self.MENTION_USER_MEDIA)

            media = self.api.get_mentioned_media_info(
                user_id=self.instagram_business_id,
                media_id=media_id,
            )
            self.assertEqual(media.id, media_id)
            self.assertEqual(len(media.comments), 1)
            self.assertEqual(len(media.children), 2)

            media_json = self.api.get_mentioned_media_info(
                user_id=self.instagram_business_id,
                media_id=media_id,
                access_token="token",
                return_json=True,
            )
            self.assertEqual(media_json["id"], media_id)
            self.assertEqual(len(media_json["comments"]), 1)
            self.assertEqual(len(media_json["children"]["data"]), 2)
