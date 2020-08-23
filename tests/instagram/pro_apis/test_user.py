import json
import unittest

import responses

import pyfacebook


class ApiUserTest(unittest.TestCase):
    BASE_PATH = "testdata/instagram/apidata/users/"
    BASE_URL = "https://graph.facebook.com/{}/".format(pyfacebook.Api.VALID_API_VERSIONS[-1])

    with open(BASE_PATH + "user_default_fields.json", "rb") as f:
        USER_DEFAULT = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "user_fields.json", "rb") as f:
        USER_FIELDS = json.loads(f.read().decode("utf-8"))

    def setUp(self):
        self.instagram_business_id = "17841406338772941"
        self.api = pyfacebook.IgProApi(
            app_id="123456", app_secret="secret",
            long_term_token="token"
        )

    def testGetUserInfo(self):
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL + self.instagram_business_id, json=self.USER_DEFAULT)
            m.add("GET", self.BASE_URL + self.instagram_business_id, json=self.USER_FIELDS)

            user_full_fields = self.api.get_user_info(
                user_id=self.instagram_business_id
            )
            self.assertEqual(user_full_fields.id, self.instagram_business_id)
            self.assertEqual(user_full_fields.follows_count, 17)
            self.assertEqual(user_full_fields.username, "ikroskun")

            user_fields = self.api.get_user_info(
                user_id=self.instagram_business_id,
                fields=["id", "username", "name"],
                return_json=True
            )
            self.assertEqual(user_fields["id"], self.instagram_business_id)
            self.assertEqual(user_fields["name"], "LiuKun")
