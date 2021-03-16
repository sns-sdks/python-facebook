"""
    tests for publish
"""

import json
import unittest

import responses

import pyfacebook


class ApiPublishTest(unittest.TestCase):
    BASE_PATH = "testdata/instagram/apidata/publish/"
    BASE_URL_WITHOUT_VERSION = "https://graph.facebook.com/"
    BASE_URL = BASE_URL_WITHOUT_VERSION + "{}/".format(pyfacebook.Api.VALID_API_VERSIONS[-1])

    with open(BASE_PATH + "container_info.json", "rb") as f:
        CONTAINER_INFO = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "create_photo.json", "rb") as f:
        CREATE_PHOTO = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "create_video.json", "rb") as f:
        CREATE_VIDEO = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "publish_container.json", "rb") as f:
        PUBLISH_CONTAINER = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "publish_limit_resp.json", "rb") as f:
        PUBLISH_LIMIT_RESP = json.loads(f.read().decode("utf-8"))

    def setUp(self):
        self.instagram_business_id = "17841406338772941"
        self.api = pyfacebook.IgProApi(
            app_id="123456", app_secret="secret",
            long_term_token="token",
            instagram_business_id=self.instagram_business_id,
        )

    def testCreatePhoto(self):
        with responses.RequestsMock() as m:
            m.add("POST", self.BASE_URL_WITHOUT_VERSION + self.instagram_business_id + "/media", json=self.CREATE_PHOTO)

            resp = self.api.create_photo(
                image_url="https//www.example.com/images/bronz-fonz.jpg",
                caption="BronzFonz",
            )
            self.assertEqual(resp.id, "17889455560051444")

            resp = self.api.create_photo(
                image_url="https//www.example.com/images/bronz-fonz.jpg",
                caption="BronzFonz",
                return_json=True,
            )
            self.assertEqual(resp["id"], "17889455560051444")

    def testCreateVideo(self):
        with responses.RequestsMock() as m:
            m.add("POST", self.BASE_URL_WITHOUT_VERSION + self.instagram_business_id + "/media", json=self.CREATE_VIDEO)

            resp = self.api.create_video(
                video_url="https://www.example.com/videos/hungry-fonzes.mov",
                caption="Heyyyyyyyy",
            )
            self.assertEqual(resp.id, "17889455560051447")

            resp = self.api.create_video(
                video_url="https://www.example.com/videos/hungry-fonzes.mov",
                caption="Heyyyyyyyy",
                return_json=True,
            )
            self.assertEqual(resp["id"], "17889455560051447")

    def testPublishContainer(self):
        with responses.RequestsMock() as m:
            m.add(
                "POST",
                self.BASE_URL_WITHOUT_VERSION + self.instagram_business_id + "/media_publish",
                json=self.PUBLISH_CONTAINER,
            )

            resp = self.api.publish_container(
                creation_id="17889455560051447",
            )
            self.assertEqual(resp["id"], "17920238422030506")

    def testGetContainerInfo(self):
        container_id = "17889455560051447"

        with responses.RequestsMock() as m:
            m.add(
                "GET",
                self.BASE_URL + container_id,
                json=self.CONTAINER_INFO,
            )

            resp = self.api.get_container_info(
                container_id=container_id,
            )
            self.assertEqual(resp.id, container_id)
            self.assertEqual(resp.status_code, "PUBLISHED")

            resp_json = self.api.get_container_info(
                container_id=container_id,
                fields="id,status_code",
                return_json=True
            )
            self.assertEqual(resp_json["id"], container_id)

    def testPublishLimit(self):
        with responses.RequestsMock() as m:
            m.add(
                "GET",
                self.BASE_URL + self.instagram_business_id + "/content_publishing_limit",
                json=self.PUBLISH_LIMIT_RESP,
            )

            resp = self.api.get_publish_limit()
            self.assertEqual(resp.quota_usage, 0)
            self.assertEqual(resp.config.quota_total, 25)

            resp_json = self.api.get_publish_limit(
                fields="quota_usage",
                return_json=True,
            )
            self.assertEqual(resp_json["data"][0]["quota_usage"], 0)
