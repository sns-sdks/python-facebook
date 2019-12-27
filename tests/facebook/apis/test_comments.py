import json
import unittest

import responses

import pyfacebook


class CommentTestApi(unittest.TestCase):
    BASE_PATH = "testdata/facebook/apidata/comments/"
    BASE_URL = "https://graph.facebook.com/v5.0/"

    with open(BASE_PATH + "comment_by_parent_p1.json", "rb") as f:
        COMMENTS_PAGED_1 = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "comment_by_parent_p2.json", "rb") as f:
        COMMENTS_PAGED_2 = json.loads(f.read().decode("utf-8"))

    def setUp(self):
        self.api = pyfacebook.Api(
            app_id="123456", app_secret="secret",
            long_term_token="token"
        )

    def testGetCommentByParent(self):
        post_id = "2121008874780932_2498613793687103"
        # test all comments
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL + post_id + "/comments", json=self.COMMENTS_PAGED_1)
            m.add("GET", self.BASE_URL + post_id + "/comments", json=self.COMMENTS_PAGED_2)

            comments, comment_summary = self.api.get_comments_by_parent(
                object_id=post_id,
                count=None,
                limit=5
            )

            self.assertEqual(len(comments), 7)
            self.assertEqual(comment_summary.total_count, 7)

        # test count
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL + post_id + "/comments", json=self.COMMENTS_PAGED_1)

            comments, comment_summary = self.api.get_comments_by_parent(
                object_id=post_id,
                count=5,
                limit=5,
                return_json=True
            )

            self.assertEqual(len(comments), 5)
            self.assertEqual(comment_summary["total_count"], 7)
