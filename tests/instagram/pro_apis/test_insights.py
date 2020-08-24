import json
import unittest

import responses

import pyfacebook


class ApiMediaTest(unittest.TestCase):
    BASE_PATH = "testdata/instagram/apidata/insights/"
    BASE_URL = "https://graph.facebook.com/{}/".format(pyfacebook.Api.VALID_API_VERSIONS[-1])

    with open(BASE_PATH + "user_insights.json", "rb") as f:
        USER_INSIGHTS = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "user_insights_2.json", "rb") as f:
        USER_INSIGHTS_2 = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "media_album_insights.json", "rb") as f:
        MEDIA_ALBUM_INSIGHTS = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "media_photo_insights.json", "rb") as f:
        MEDIA_PHOTO_INSIGHTS = json.loads(f.read().decode("utf-8"))

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
                until=1577635200,
                access_token=self.api._access_token,
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
                access_token=self.api._access_token,
                return_json=True,
            )
            self.assertEqual(len(res_json), 2)
            self.assertEqual(res_json[1]["name"], "reach")
            self.assertEqual(len(res_json[1]["values"]), 10)

    def testGetMediaInsights(self):
        media_album_id = "12345"
        media_photo_id = "67890"
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL + media_album_id + "/insights", json=self.MEDIA_ALBUM_INSIGHTS)
            m.add("GET", self.BASE_URL + media_photo_id + "/insights", json=self.MEDIA_PHOTO_INSIGHTS)

            media_album_insights = self.api.get_media_insights(
                media_id=media_album_id,
                metrics=[
                    "carousel_album_engagement", "carousel_album_impressions",
                    "carousel_album_reach", "saved", "video_views"
                ],
                access_token=self.api._access_token,
            )
            self.assertEqual(len(media_album_insights), 5)
            self.assertEqual(media_album_insights[0].period, "lifetime")
            self.assertEqual(media_album_insights[0].values[0].value, 138)

            media_photo_insights = self.api.get_media_insights(
                media_id=media_photo_id,
                metrics=[
                    "engagement", "impressions", "reach", "saved"
                ],
                access_token=self.api._access_token,
                return_json=True
            )
            self.assertEqual(len(media_photo_insights), 4)
            self.assertEqual(media_photo_insights[0]["values"][0]["value"], 65)
