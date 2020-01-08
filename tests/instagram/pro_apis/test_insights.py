import json
import unittest

import responses

import pyfacebook


class ApiMediaTest(unittest.TestCase):
    BASE_PATH = "testdata/instagram/apidata/insights/"
    BASE_URL = "https://graph.facebook.com/v5.0/"

    with open(BASE_PATH + "user_insights.json", "rb") as f:
        USER_INSIGHTS = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "user_insights_2.json", "rb") as f:
        USER_INSIGHTS_2 = json.loads(f.read().decode("utf-8"))

    def setUp(self):
        self.instagram_business_id = "123456"
        self.api = pyfacebook.IgProApi(
            app_id="123456", app_secret="secret",
            long_term_token="token"
        )

    def testGetUserInsights(self):
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL + self.instagram_business_id + "/insights", json=self.USER_INSIGHTS)
            m.add("GET", self.BASE_URL + self.instagram_business_id + "/insights", json=self.USER_INSIGHTS_2)

            res = self.api.get_user_insights(
                user_id=self.instagram_business_id,
                period="day",
                metrics=["impressions", "follower_count"],
                since=1576771200,
                until=1577635200
            )
            self.assertEqual(len(res), 2)
            self.assertEqual(res[0].name, "impressions")
            self.assertEqual(len(res[1].values), 10)

            res_json = self.api.get_user_insights(
                user_id=self.instagram_business_id,
                period="days_28",
                metrics=("impressions", "reach"),
                since=1576771200,
                until=1577635200,
                return_json=True,
            )
            self.assertEqual(len(res_json), 2)
            self.assertEqual(res_json[1]["name"], "reach")
            self.assertEqual(len(res_json[1]["values"]), 10)
