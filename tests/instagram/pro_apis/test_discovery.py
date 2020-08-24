import json
import unittest

import responses

import pyfacebook


class ApiDiscoveryTest(unittest.TestCase):
    BASE_PATH = "testdata/instagram/apidata/discovery/"
    BASE_URL = "https://graph.facebook.com/{}/".format(pyfacebook.Api.VALID_API_VERSIONS[-1])

    with open(BASE_PATH + "user_default.json", "rb") as f:
        USER_DEFAULT = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "user_fields.json", "rb") as f:
        USER_FIELDS = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "media_default_p1.json", "rb") as f:
        MEDIA_DEFAULT_P1 = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "media_default_p2.json", "rb") as f:
        MEDIA_DEFAULT_P2 = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "media_fields.json", "rb") as f:
        MEDIA_FIELDS = json.loads(f.read().decode("utf-8"))

    def setUp(self):
        self.instagram_business_id = "123456789"
        self.api = pyfacebook.IgProApi(
            app_id="123456", app_secret="secret",
            long_term_token="token",
            instagram_business_id=self.instagram_business_id
        )

    def testDiscoveryUser(self):
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL + self.instagram_business_id, json=self.USER_DEFAULT)
            m.add("GET", self.BASE_URL + self.instagram_business_id, json=self.USER_FIELDS)

            user_json = self.api.discovery_user(
                username="facebook",
                return_json=True,
            )

            self.assertEqual(user_json["id"], "17841400455970028")
            self.assertEqual(user_json["followers_count"], 3502538)

            user_model = self.api.discovery_user(
                username="facebook",
                fields=["id", "followers_count", "follows_count", "name", "username"]
            )
            self.assertEqual(user_model.id, "17841400455970028")
            self.assertEqual(user_model.followers_count, 3502538)

    def testDiscoveryMedia(self):
        # test for error time
        with self.assertRaises(pyfacebook.PyFacebookException):
            self.api.discovery_user_medias("facebook", since_time="2019")
            self.api.discovery_user_medias("facebook", until_time="2019")

        # test time interval all medias.
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL + self.instagram_business_id, json=self.MEDIA_DEFAULT_P1)
            m.add("GET", self.BASE_URL + self.instagram_business_id, json=self.MEDIA_DEFAULT_P2)

            medias = self.api.discovery_user_medias(
                username="facebook",
                count=None,
                limit=5,
                since_time="2019-11-1",
                until_time="2019-12-20",
            )
            self.assertEqual(len(medias), 5)

        # test get all medias.
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL + self.instagram_business_id, json=self.MEDIA_DEFAULT_P1)
            m.add("GET", self.BASE_URL + self.instagram_business_id, json=self.MEDIA_DEFAULT_P2)

            medias = self.api.discovery_user_medias(
                username="facebook",
                count=None,
                limit=5,
            )

            self.assertEqual(len(medias), 10)

        # test count and with fields
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL + self.instagram_business_id, json=self.MEDIA_FIELDS)

            medias = self.api.discovery_user_medias(
                username="facebook",
                fields=["id", "caption", "comments_count", "like_count"],
                count=4,
                return_json=True
            )

            self.assertEqual(len(medias), 4)

        # test time and not timestamp field
        with self.assertRaises(pyfacebook.PyFacebookException):
            self.api.discovery_user_medias(
                username="facebook",
                fields=["id", "caption", "comments_count", "like_count"],
                since_time="2019-10-1",
            )
