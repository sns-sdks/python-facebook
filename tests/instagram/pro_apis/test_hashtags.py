import json
import unittest

import responses

import pyfacebook


class ApiHashtagTest(unittest.TestCase):
    BASE_PATH = "testdata/instagram/apidata/hashtags/"
    BASE_URL = "https://graph.facebook.com/v5.0/"

    with open(BASE_PATH + "hashtag_search.json", "rb") as f:
        HASHTAG_SEARCH = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "recently_searched_hashtags.json", "rb") as f:
        RECENTLY_HASHTAGS = json.loads(f.read().decode("utf-8"))

    def setUp(self):
        self.instagram_business_id = "123456789"
        self.api = pyfacebook.IgProApi(
            app_id="123456", app_secret="secret",
            long_term_token="token",
            instagram_business_id=self.instagram_business_id
        )

    def testSearchHashtag(self):
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL + "ig_hashtag_search", json=self.HASHTAG_SEARCH)

            hashtags = self.api.search_user_hashtag(
                user_id=self.instagram_business_id,
                q="liukun"
            )
            self.assertEqual(len(hashtags), 1)
            self.assertEqual(hashtags[0].id, "17843421130029320")

            hashtags_json = self.api.search_user_hashtag(
                user_id=self.instagram_business_id,
                q="liukun",
                return_json=True
            )
            self.assertEqual(hashtags_json[0]["id"], "17843421130029320")

    def testGetUserRecentlySearchedHashtags(self):
        with responses.RequestsMock() as m:
            m.add(
                "GET",
                self.BASE_URL + self.instagram_business_id + "/recently_searched_hashtags",
                json=self.RECENTLY_HASHTAGS
            )

            hashtags = self.api.get_user_recently_searched_hashtags(
                user_id=self.instagram_business_id,
                limit=3,
            )

            self.assertEqual(len(hashtags), 3)
            self.assertEqual(hashtags[0].name, "loveyou")

            hashtags_json = self.api.get_user_recently_searched_hashtags(
                user_id=self.instagram_business_id,
                limit=3,
                return_json=True
            )
            self.assertEqual(hashtags_json[1]["name"], "love")
