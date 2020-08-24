import json

import unittest
from six import iteritems

import responses
import pyfacebook


class ApiCommentTest(unittest.TestCase):
    BASE_PATH = "testdata/instagram/apidata/comments/"
    BASE_URL = "https://graph.facebook.com/{}/".format(pyfacebook.Api.VALID_API_VERSIONS[-1])

    with open(BASE_PATH + "comment_default_p1.json", "rb") as f:
        COMMENTS_DEFAULT_p1 = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "comment_default_p2.json", "rb") as f:
        COMMENTS_DEFAULT_p2 = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "comment_fields.json", "rb") as f:
        COMMENTS_FIELDS = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "comment_single_default.json", "rb") as f:
        COMMENT_SINGLE_DEFAULT = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "comment_single_fields.json", "rb") as f:
        COMMENT_SINGLE_FIELDS = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "comments_multi_default.json", "rb") as f:
        COMMENTS_MULTI_DEFAULT = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "comments_multi_fields.json", "rb") as f:
        COMMENTS_MULTI_FIELDS = json.loads(f.read().decode("utf-8"))

    def setUp(self):
        self.api = pyfacebook.IgProApi(
            app_id="123456", app_secret="secret",
            long_term_token="token",
        )

    def testGetCommentsByMedia(self):
        media_id = "17955956875141196"
        # test get all comments
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL + media_id + "/comments", json=self.COMMENTS_DEFAULT_p1)
            m.add("GET", self.BASE_URL + media_id + "/comments", json=self.COMMENTS_DEFAULT_p2)

            res = self.api.get_comments_by_media(
                media_id=media_id,
                count=None
            )
            self.assertEqual(len(res), 9)
            self.assertEqual(res[0].replies[0].id, "17850033184810160")

        # test count
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL + media_id + "/comments", json=self.COMMENTS_DEFAULT_p1)
            m.add("GET", self.BASE_URL + media_id + "/comments", json=self.COMMENTS_DEFAULT_p2)

            res = self.api.get_comments_by_media(
                media_id=media_id,
                count=8,
                return_json=True
            )
            self.assertEqual(len(res), 8)
            self.assertEqual(res[6]["replies"]["data"][0]["id"], "18107567341036926")

        # test fields
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL + media_id + "/comments", json=self.COMMENTS_FIELDS)

            res = self.api.get_comments_by_media(
                media_id=media_id,
                fields=["id", "like_count", "timestamp", "text"],
                count=4
            )

            self.assertEqual(len(res), 4)
            self.assertEqual(res[0].id, "17862949873623188")

    def testGetCommentInfo(self):
        comment_id = "17862949873623188"

        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL + comment_id, json=self.COMMENT_SINGLE_DEFAULT)
            m.add("GET", self.BASE_URL + comment_id, json=self.COMMENT_SINGLE_DEFAULT)

            res_default_with_reply = self.api.get_comment_info(
                comment_id=comment_id
            )
            self.assertEqual(res_default_with_reply.id, comment_id)
            self.assertEqual(res_default_with_reply.replies[0].id, "17850033184810160")

            res_fields = self.api.get_comment_info(
                comment_id=comment_id,
                fields=["id", "like_count", "timestamp", "text"],
                include_reply=False,
                return_json=True
            )
            self.assertEqual(res_fields["id"], comment_id)

    def testGetCommentsInfo(self):
        comment_ids = ["17862949873623188", "17844360649889631"]

        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=self.COMMENTS_MULTI_DEFAULT)
            m.add("GET", self.BASE_URL, json=self.COMMENTS_MULTI_FIELDS)

            res_default_with_reply = self.api.get_comments_info(
                comment_ids=comment_ids
            )
            for _id, data in iteritems(res_default_with_reply):
                self.assertIn(_id, comment_ids)
                self.assertIn(_id, data.id)

            res_fields = self.api.get_comments_info(
                comment_ids=comment_ids,
                fields=["id", "like_count", "timestamp", "text"],
                include_reply=False,
                return_json=True,
            )
            for _id, data in iteritems(res_fields):
                self.assertIn(_id, comment_ids)
                self.assertIn(_id, data["id"])
