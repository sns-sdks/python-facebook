import json
import unittest

import responses
from requests import HTTPError

import pyfacebook
from pyfacebook.api.base import BaseApi


class BaseApiTest(unittest.TestCase):
    BASE_PATH = "testdata/base/"
    ACCESS_TOKEN_URL = "https://graph.facebook.com/v5.0/oauth/access_token"

    with open(BASE_PATH + "app_token.json", "rb") as f:
        APP_ACCESS_TOKEN = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "long_term_token.json", "rb") as f:
        LONG_TERM_TOKEN = json.loads(f.read().decode("utf-8"))

    def testApiVersion(self):
        with self.assertRaises(pyfacebook.PyFacebookException):
            BaseApi(version="1.0")

        with self.assertRaises(pyfacebook.PyFacebookException):
            BaseApi(version="v1.0")

        with self.assertRaises(pyfacebook.PyFacebookException):
            BaseApi(version="version")

        api = BaseApi(long_term_token="token", version=None)
        self.assertEqual(api.version, api.VALID_API_VERSIONS[-1])

        api = BaseApi(long_term_token="token", version="3.3")
        self.assertEqual(api.version, "v3.3")

    def testApiToken(self):
        with self.assertRaises(pyfacebook.PyFacebookException):
            BaseApi()

        api = BaseApi(long_term_token="token", debug_http=True)
        self.assertEqual(api._access_token, "token")

        with responses.RequestsMock() as m:
            m.add("GET", self.ACCESS_TOKEN_URL, json=self.APP_ACCESS_TOKEN)
            api = BaseApi(app_id="123456789", app_secret="secret", application_only_auth=True)
            self.assertEqual(api._access_token, "123456789|fvYq7ORmqKa2IDCijArPOYKB0")

        with responses.RequestsMock() as m:
            m.add("GET", self.ACCESS_TOKEN_URL, json=self.LONG_TERM_TOKEN)
            api = BaseApi(app_id="123456789", app_secret="secret", short_token="short-lived token")
            self.assertEqual(api._access_token, "token")

    def testRequest(self):
        api = BaseApi(long_term_token="token")
        with responses.RequestsMock() as m:
            m.add("GET", "https://graph.facebook.com/", json={"message": "message"})

            r = api._request(
                path="", args=None
            )
            r.json()["message"] = "message"

        with responses.RequestsMock() as m:
            m.add("POST", "https://graph.facebook.com/", json={"message": "message"})

            r = api._request(
                path="", method="POST", args=None, post_args={"auth": 1},
            )
            r.json()["message"] = "message"

        with responses.RequestsMock() as m:
            m.add("GET", "https://graph.facebook.com/", body=HTTPError("..."))

            with self.assertRaises(pyfacebook.PyFacebookException):
                api._request(
                    path="",
                )

    def testCheckError(self):
        data = {"error": {"code": 100}}
        api = BaseApi(long_term_token="token")
        with self.assertRaises(pyfacebook.PyFacebookException):
            api._check_graph_error(data)

    def testGetLongToken(self):
        api = BaseApi(app_id="id", app_secret="secret", long_term_token="token")

        with responses.RequestsMock() as m:
            m.add("GET", self.ACCESS_TOKEN_URL, json=self.LONG_TERM_TOKEN)

            token = api.get_long_token(short_token="short-lived token", return_json=True)

            self.assertEqual(token["access_token"], "token")

    def testGetAppToken(self):
        api = BaseApi(app_id="id", app_secret="secret", long_term_token="token")
        with responses.RequestsMock() as m:
            m.add("GET", self.ACCESS_TOKEN_URL, json=self.APP_ACCESS_TOKEN)

            token = api.get_app_token(return_json=True)

            self.assertEqual(token["access_token"], "123456789|fvYq7ORmqKa2IDCijArPOYKB0")
