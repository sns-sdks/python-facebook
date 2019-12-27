import json
import unittest

import responses

import pyfacebook


class PostApiTest(unittest.TestCase):
    BASE_PATH = "testdata/facebook/apidata/posts/"
    BASE_URL = "https://graph.facebook.com/v5.0/"
    PAGE_ID = "2121008874780932"

    with open(BASE_PATH + "feeds_default_fields_p1.json", "rb") as f:
        FEED_PAGED_1 = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "feeds_default_fields_p2.json", "rb") as f:
        FEED_PAGED_2 = json.loads(f.read().decode("utf-8"))

    def setUp(self):
        self.api = pyfacebook.Api(
            app_id="12345678",
            app_secret="secret",
            long_term_token="token"
        )

    def testPageFeed(self):
        # test base count
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL + self.PAGE_ID + "/feed", json=self.FEED_PAGED_1)
            m.add("GET", self.BASE_URL + self.PAGE_ID + "/feed", json=self.FEED_PAGED_2)

            posts = self.api.get_page_feeds(
                page_id=self.PAGE_ID,
                count=12,
                access_token="token",
                return_json=True
            )

            self.assertEqual(len(posts), 12)

        # test count is None
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL + self.PAGE_ID + "/feed", json=self.FEED_PAGED_1)
            m.add("GET", self.BASE_URL + self.PAGE_ID + "/feed", json=self.FEED_PAGED_2)

            posts = self.api.get_page_feeds(
                page_id=self.PAGE_ID,
                count=None,
                access_token="token",
            )
            self.assertEqual(len(posts), 15)
