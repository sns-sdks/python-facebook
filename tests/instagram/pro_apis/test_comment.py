import json

import unittest
from six import iteritems

import responses
import pyfacebook


class ApiCommentTest(unittest.TestCase):
    BASE_PATH = "testdata/instagram/apidata/comments/"
    BASE_URL = "https://graph.facebook.com/v5.0/"

    with open(BASE_PATH + "comment_default_p1.json", "rb") as f:
        COMMENTS_DEFAULT_p1 = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "comment_default_p2.json", "rb") as f:
        COMMENTS_DEFAULT_p2 = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "comment_fields.json", "rb") as f:
        COMMENTS_FIELDS = json.loads(f.read().decode("utf-8"))

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


