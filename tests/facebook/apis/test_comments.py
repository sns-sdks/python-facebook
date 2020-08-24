import json
import unittest

import responses
from six import iteritems

import pyfacebook


class CommentTestApi(unittest.TestCase):
    BASE_PATH = "testdata/facebook/apidata/comments/"
    BASE_URL = "https://graph.facebook.com/{}/".format(pyfacebook.Api.VALID_API_VERSIONS[-1])

    with open(BASE_PATH + "comment_by_parent_p1.json", "rb") as f:
        COMMENTS_PAGED_1 = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "comment_by_parent_p2.json", "rb") as f:
        COMMENTS_PAGED_2 = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "comment_info.json", "rb") as f:
        COMMENT_INFO = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "multi_default_fields.json", "rb") as f:
        MULTI_COMMENT_INFO_1 = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "multi_fields.json", "rb") as f:
        MULTI_COMMENT_INFO_2 = json.loads(f.read().decode("utf-8"))

    def setUp(self):
        self.api = pyfacebook.Api(
            app_id="123456", app_secret="secret",
            long_term_token="token", version="v8.0"
        )

    def testGetCommentByObject(self):
        post_id = "2121008874780932_2498613793687103"
        # test all comments
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL + post_id + "/comments", json=self.COMMENTS_PAGED_1)
            m.add("GET", self.BASE_URL + post_id + "/comments", json=self.COMMENTS_PAGED_2)

            comments, comment_summary = self.api.get_comments_by_object(
                object_id=post_id,
                count=None,
                limit=5
            )

            self.assertEqual(len(comments), 7)
            self.assertEqual(comment_summary.total_count, 7)

        # test count
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL + post_id + "/comments", json=self.COMMENTS_PAGED_1)

            comments, comment_summary = self.api.get_comments_by_object(
                object_id=post_id,
                count=5,
                limit=5,
                return_json=True
            )

            self.assertEqual(len(comments), 5)
            self.assertEqual(comment_summary["total_count"], 7)

    def testGetCommentInfo(self):
        comment_id = "2498598377021978_2498617433686739"
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL + comment_id, json=self.COMMENT_INFO)

            comment = self.api.get_comment_info(
                comment_id=comment_id,
            )
            self.assertEqual(comment.id, comment_id)

            comment_json = self.api.get_comment_info(
                comment_id=comment_id,
                return_json=True
            )
            self.assertEqual(comment_json["id"], comment_id)

    def testGetComments(self):
        ids = ["2498598377021978_2498617433686739", "2498598377021978_2509257692622713"]
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=self.MULTI_COMMENT_INFO_1)

            comment_dict = self.api.get_comments(
                ids=ids
            )
            for _id, data in iteritems(comment_dict):
                self.assertIn(_id, ids)
                self.assertEqual(_id, data.id)

        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=self.MULTI_COMMENT_INFO_2)
            comment_dict = self.api.get_comments(
                ids=ids,
                fields=["id", "message", "created_time", "comment_count"],
                return_json=True
            )
            for _id, data in iteritems(comment_dict):
                self.assertIn(_id, ids)
                self.assertEqual(_id, data["id"])
