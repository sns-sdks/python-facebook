import json
import unittest

import responses

import pyfacebook


class ApiUserTest(unittest.TestCase):
    BASE_PATH = "testdata/instagram_basic/apidata/user/"

    with open(BASE_PATH + "user_info_default.json", "rb") as f:
        USER_INFO_DEFAULT = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "user_with_fields.json", "rb") as f:
        USER_INFO_FIELDS = json.loads(f.read().decode("utf-8"))

    def setUp(self):
        self.api = pyfacebook.IgBasicApi(long_term_token="token")

    def testGetUserInfo(self):
        user_id = "17841406338772941"

        with responses.RequestsMock() as m:
            m.add("GET", self.api.GRAPH_URL + "me", json=self.USER_INFO_DEFAULT)
            m.add("GET", self.api.GRAPH_URL + user_id, json=self.USER_INFO_FIELDS)

            me_info = self.api.get_user_info()
            self.assertEqual(me_info.id, user_id)
            self.assertEqual(me_info.account_type, "BUSINESS")

            user_info = self.api.get_user_info(
                user_id=user_id,
                fields=["id", "username"],
                return_json=True
            )
            self.assertEqual(user_info["id"], user_id)
            self.assertEqual(user_info["username"], "ikroskun")
