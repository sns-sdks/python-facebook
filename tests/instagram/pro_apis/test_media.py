import json
import unittest

import responses

import pyfacebook


class ApiMediaTest(unittest.TestCase):
    BASE_PATH = "testdata/instagram/apidata/medias/"
    BASE_URL = "https://graph.facebook.com/v5.0/"

    with open(BASE_PATH + "media_default_fields_p1.json", "rb") as f:
        MEDIAS_DEFAULT_p1 = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "media_default_fields_p2.json", "rb") as f:
        MEDIAS_DEFAULT_p2 = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "media_default_fields_p3.json", "rb") as f:
        MEDIAS_DEFAULT_p3 = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "media_fields_p1.json", "rb") as f:
        MEDIAS_FIELDS_p1 = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "media_fields_p2.json", "rb") as f:
        MEDIAS_FIELDS_p2 = json.loads(f.read().decode("utf-8"))

    def setUp(self):
        self.instagram_business_id = "17841406338772941"
        self.api = pyfacebook.IgProApi(
            app_id="123456", app_secret="secret",
            long_term_token="token"
        )

    def testGetMedias(self):
        # test all items
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL + self.instagram_business_id + "/media", json=self.MEDIAS_DEFAULT_p1)
            m.add("GET", self.BASE_URL + self.instagram_business_id + "/media", json=self.MEDIAS_DEFAULT_p2)
            m.add("GET", self.BASE_URL + self.instagram_business_id + "/media", json=self.MEDIAS_DEFAULT_p3)

            res = self.api.get_medias(
                user_id=self.instagram_business_id,
                count=None,
                limit=5,
                return_json=True
            )
            self.assertEqual(len(res), 8)

        # test count
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL + self.instagram_business_id + "/media", json=self.MEDIAS_FIELDS_p1)
            m.add("GET", self.BASE_URL + self.instagram_business_id + "/media", json=self.MEDIAS_FIELDS_p2)

            res = self.api.get_medias(
                user_id=self.instagram_business_id,
                fields=["id", "caption", "media_url", "like_count"],
                count=7,
                limit=5
            )
            self.assertEqual(len(res), 7)

        # test time filter
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL + self.instagram_business_id + "/media", json=self.MEDIAS_DEFAULT_p1)
            # m.add("GET", self.BASE_URL + self.instagram_business_id + "/media", json=self.MEDIAS_DEFAULT_p2)

            res = self.api.get_medias(
                user_id=self.instagram_business_id,
                since_time="2019-10-1",
                until_time="2019-11-1",
                count=None,
                limit=5
            )
            self.assertEqual(len(res), 2)

        with self.assertRaises(pyfacebook.PyFacebookException):
            self.api.get_medias(user_id=self.instagram_business_id, since_time="2019")





