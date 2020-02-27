import json
import unittest

import responses

import pyfacebook


class IgBasicApiTest(unittest.TestCase):
    BASE_PATH = "testdata/instagram_basic/apidata/"

    with open(BASE_PATH + "long_access_token_info.json", "rb") as f:
        LONG_ACCESS_TOKEN_INFO = json.loads(f.read().decode("utf-8"))

    def setUp(self):
        self.api = pyfacebook.IgBasicApi(
            app_id="app id",
            app_secret="app secret",
            initial_access_token=False,
        )

    def testNotSupportMethod(self):
        self.assertIsNone(self.api._generate_secret_proof("secret", "token"))
        with self.assertRaises(pyfacebook.PyFacebookException):
            self.api.get_app_token()

        with self.assertRaises(pyfacebook.PyFacebookException):
            self.api.get_token_info(input_token="token")

        with self.assertRaises(pyfacebook.PyFacebookException):
            self.api.exchange_insights_token(page_id="page id", access_token="token")

    def testGetLongToken(self):
        with responses.RequestsMock() as m:
            m.add("GET", self.api.GRAPH_URL + "access_token", json=self.LONG_ACCESS_TOKEN_INFO)

            token = self.api.get_long_token(
                short_token="token"
            )
            self.assertEqual(token.access_token, "access-token")

            token_json = self.api.get_long_token(
                short_token="other token",
                app_secret="secret",
                return_json=True
            )
            self.assertEqual(token_json["expires_in"], 7200)

    def testGetRefreshToken(self):
        api = pyfacebook.IgBasicApi(long_term_token="token")

        with responses.RequestsMock() as m:
            m.add("GET", self.api.GRAPH_URL + "refresh_access_token", json=self.LONG_ACCESS_TOKEN_INFO)

            token = api.refresh_access_token()
            self.assertEqual(token.access_token, "access-token")

            token_json = api.refresh_access_token(
                access_token=self.api._access_token,
                return_json=True
            )
            self.assertEqual(token_json["access_token"], "access-token")
