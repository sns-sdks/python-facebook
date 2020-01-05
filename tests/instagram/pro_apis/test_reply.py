import json
import unittest

import responses
import pyfacebook


class ApiRepliesTest(unittest.TestCase):
    BASE_PATH = "testdata/instagram/apidata/replies/"
    BASE_URL = "https://graph.facebook.com/v5.0/"

    with open(BASE_PATH + "replies_default_p1.json", "rb") as f:
        REPLIES_DEFAULT_p1 = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "replies_default_p2.json", "rb") as f:
        REPLIES_DEFAULT_p2 = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "replies_fields_p1.json", "rb") as f:
        REPLIES_FIELDS_p1 = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "replies_fields_p2.json", "rb") as f:
        REPLIES_FIELDS_p2 = json.loads(f.read().decode("utf-8"))

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
