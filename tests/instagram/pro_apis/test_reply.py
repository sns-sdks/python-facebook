import json
import unittest

import responses
from six import iteritems

import pyfacebook


class ApiRepliesTest(unittest.TestCase):
    BASE_PATH = "testdata/instagram/apidata/replies/"
    BASE_URL = "https://graph.facebook.com/{}/".format(pyfacebook.Api.VALID_API_VERSIONS[-1])

    with open(BASE_PATH + "replies_default_p1.json", "rb") as f:
        REPLIES_DEFAULT_p1 = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "replies_default_p2.json", "rb") as f:
        REPLIES_DEFAULT_p2 = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "replies_fields_p1.json", "rb") as f:
        REPLIES_FIELDS_p1 = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "replies_fields_p2.json", "rb") as f:
        REPLIES_FIELDS_p2 = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "reply_single_default.json", "rb") as f:
        REPLY_SINGLE_DEFAULT = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "reply_single_fields.json", "rb") as f:
        REPLY_SINGLE_FIELDS = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "replies_multi_default.json", "rb") as f:
        REPLIES_MULTI_DEFAULT = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "replies_multi_fields.json", "rb") as f:
        REPLIES_MULTI_FIELDS = json.loads(f.read().decode("utf-8"))

    def setUp(self):
        self.api = pyfacebook.IgProApi(
            app_id="123456", app_secret="secret",
            long_term_token="token",
        )

    def testGetRepliesByComment(self):
        comment_id = "17984127178281340"
        # test get all replies
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL + comment_id + "/replies", json=self.REPLIES_DEFAULT_p1)
            m.add("GET", self.BASE_URL + comment_id + "/replies", json=self.REPLIES_DEFAULT_p2)

            res = self.api.get_replies_by_comment(
                comment_id=comment_id,
                count=None,
                limit=2
            )

            self.assertEqual(len(res), 3)
            self.assertEqual(res[0].id, "18107567341036926")

        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL + comment_id + "/replies", json=self.REPLIES_FIELDS_p1)

            res = self.api.get_replies_by_comment(
                comment_id=comment_id,
                fields=["id", "timestamp", "text"],
                count=1,
                limit=2,
                return_json=True
            )

            self.assertEqual(len(res), 1)
            self.assertEqual(res[0]["id"], "18107567341036926")

    def testGetReplyInfo(self):
        reply_id = "18025866040229880"

        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL + reply_id, json=self.REPLY_SINGLE_DEFAULT)
            m.add("GET", self.BASE_URL + reply_id, json=self.REPLY_SINGLE_FIELDS)

            res_default = self.api.get_reply_info(
                reply_id=reply_id
            )
            self.assertEqual(res_default.id, reply_id)

            res_fields = self.api.get_reply_info(
                reply_id=reply_id,
                fields=["id", "timestamp", "text"],
                return_json=True
            )
            self.assertEqual(res_fields["id"], reply_id)

    def testGetRepliesInfo(self):
        reply_ids = ["17850033184810160", "18025866040229880"]

        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=self.REPLIES_MULTI_DEFAULT)
            m.add("GET", self.BASE_URL, json=self.REPLIES_MULTI_FIELDS)

            res_default = self.api.get_replies_info(
                reply_ids=reply_ids
            )
            for _id, data in iteritems(res_default):
                self.assertIn(_id, reply_ids)
                self.assertIn(_id, data.id)

            res_fields = self.api.get_replies_info(
                reply_ids=reply_ids,
                fields=["id", "timestamp", "text"],
                return_json=True
            )
            for _id, data in iteritems(res_fields):
                self.assertIn(_id, reply_ids)
                self.assertIn(_id, data["id"])
