import json
import unittest

import responses

import pyfacebook


class ApiHashtagTest(unittest.TestCase):
    BASE_PATH = "testdata/instagram/apidata/hashtags/"
    BASE_URL = "https://graph.facebook.com/{}/".format(pyfacebook.Api.VALID_API_VERSIONS[-1])

    with open(BASE_PATH + "hashtag_search.json", "rb") as f:
        HASHTAG_SEARCH = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "recently_searched_hashtags.json", "rb") as f:
        RECENTLY_HASHTAGS = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "hashtag_info.json", "rb") as f:
        HASHTAG_INFO = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "hashtag_top_medias_default_p1.json", "rb") as f:
        HASHTAG_TOP_MEDIAS_DEFAULT_P1 = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "hashtag_top_medias_default_p2.json", "rb") as f:
        HASHTAG_TOP_MEDIAS_DEFAULT_P2 = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "hashtag_top_medias_fields_p1.json", "rb") as f:
        HASHTAG_TOP_MEDIAS_FIELDS_P1 = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "hashtag_top_medias_fields_p2.json", "rb") as f:
        HASHTAG_TOP_MEDIAS_FIELDS_P2 = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "hashtag_recent_medias_default_p1.json", "rb") as f:
        HASHTAG_RECENT_MEDIAS_DEFAULT_P1 = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "hashtag_recent_medias_default_p2.json", "rb") as f:
        HASHTAG_RECENT_MEDIAS_DEFAULT_P2 = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "hashtag_recent_medias_fields_p1.json", "rb") as f:
        HASHTAG_RECENT_MEDIAS_FIELDS_P1 = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "hashtag_recent_medias_fields_p2.json", "rb") as f:
        HASHTAG_RECENT_MEDIAS_FIELDS_P2 = json.loads(f.read().decode("utf-8"))

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

            hashtags = self.api.search_hashtag(
                q="liukun"
            )
            self.assertEqual(len(hashtags), 1)
            self.assertEqual(hashtags[0].id, "17843421130029320")

            hashtags_json = self.api.search_hashtag(
                q="liukun",
                return_json=True
            )
            self.assertEqual(hashtags_json[0]["id"], "17843421130029320")

    def testGetHashtagInfo(self):
        hashtag_id = "17843826142012701"
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL + hashtag_id, json=self.HASHTAG_INFO)

            hashtag = self.api.get_hashtag_info(hashtag_id=hashtag_id)
            self.assertEqual(hashtag.id, hashtag_id)

            hashtag_json = self.api.get_hashtag_info(hashtag_id=hashtag_id, return_json=True)
            self.assertEqual(hashtag_json["name"], "love")

    def testGetHashtagTopMedias(self):
        hashtag_id = "17843826142012701"
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL + hashtag_id + "/top_media", json=self.HASHTAG_TOP_MEDIAS_DEFAULT_P1)
            m.add("GET", self.BASE_URL + hashtag_id + "/top_media", json=self.HASHTAG_TOP_MEDIAS_DEFAULT_P2)

            medias = self.api.get_hashtag_top_medias(
                hashtag_id=hashtag_id,
                count=None,
            )
            self.assertEqual(len(medias), 50)
            self.assertEqual(medias[0].id, "18088158883149835")

        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL + hashtag_id + "/top_media", json=self.HASHTAG_TOP_MEDIAS_FIELDS_P1)
            m.add("GET", self.BASE_URL + hashtag_id + "/top_media", json=self.HASHTAG_TOP_MEDIAS_FIELDS_P2)

            medias_json = self.api.get_hashtag_top_medias(
                hashtag_id=hashtag_id,
                fields=["id", "media_type", "comments_count", "like_count"],
                count=8,
                limit=5,
                return_json=True
            )
            self.assertEqual(len(medias_json), 8)
            self.assertEqual(medias_json[0]["id"], "18088158883149835")
            self.assertEqual(medias_json[0]["like_count"], 804)

    def testGetHashtagRecentMedias(self):
        hashtag_id = "17843826142012701"
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL + hashtag_id + "/recent_media", json=self.HASHTAG_RECENT_MEDIAS_DEFAULT_P1)
            m.add("GET", self.BASE_URL + hashtag_id + "/recent_media", json=self.HASHTAG_RECENT_MEDIAS_DEFAULT_P2)

            medias = self.api.get_hashtag_recent_medias(
                hashtag_id=hashtag_id,
                count=None,
            )
            self.assertEqual(len(medias), 50)
            self.assertEqual(medias[0].id, "17861656786698079")

        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL + hashtag_id + "/recent_media", json=self.HASHTAG_RECENT_MEDIAS_FIELDS_P1)
            m.add("GET", self.BASE_URL + hashtag_id + "/recent_media", json=self.HASHTAG_RECENT_MEDIAS_FIELDS_P2)

            medias_json = self.api.get_hashtag_recent_medias(
                hashtag_id=hashtag_id,
                fields=("id", "media_type", "comments_count", "like_count"),
                count=8,
                limit=5,
                return_json=True
            )
            self.assertEqual(len(medias_json), 8)
            self.assertEqual(medias_json[0]["id"], "17983329973290591")

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
                access_token=self.api._access_token
            )

            self.assertEqual(len(hashtags), 3)
            self.assertEqual(hashtags[0].name, "loveyou")

            hashtags_json = self.api.get_user_recently_searched_hashtags(
                user_id=self.instagram_business_id,
                limit=3,
                access_token=self.api._access_token,
                return_json=True
            )
            self.assertEqual(hashtags_json[1]["name"], "love")
