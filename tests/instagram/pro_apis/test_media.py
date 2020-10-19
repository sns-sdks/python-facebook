import json
import unittest

import responses
from six import iteritems

import pyfacebook


class ApiMediaTest(unittest.TestCase):
    BASE_PATH = "testdata/instagram/apidata/medias/"
    BASE_URL = "https://graph.facebook.com/{}/".format(pyfacebook.Api.VALID_API_VERSIONS[-1])

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
    with open(BASE_PATH + "media_default.json", "rb") as f:
        MEDIA_DEFAULT = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "media_fields.json", "rb") as f:
        MEDIA_FIELDS = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "medias_default.json", "rb") as f:
        MEDIAS_DEFAULT = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "medias_fields.json", "rb") as f:
        MEDIAS_FIELDS = json.loads(f.read().decode("utf-8"))

    with open(BASE_PATH + "tags_medias.json", "rb") as f:
        TAGS_MEDIAS = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "tags_medias_p1.json", "rb") as f:
        TAGS_MEDIAS_P1 = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "tags_medias_p2.json", "rb") as f:
        TAGS_MEDIAS_P2 = json.loads(f.read().decode("utf-8"))

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

            res = self.api.get_user_medias(
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

            res = self.api.get_user_medias(
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

            res = self.api.get_user_medias(
                user_id=self.instagram_business_id,
                since_time="2019-10-1",
                until_time="2019-11-1",
                count=None,
                limit=5
            )
            self.assertEqual(len(res), 2)

        with self.assertRaises(pyfacebook.PyFacebookException):
            self.api.get_user_medias(user_id=self.instagram_business_id, since_time="2019")

    def testGetMediaInfo(self):
        media_id = "18027939643230671"
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL + media_id, json=self.MEDIA_DEFAULT)
            m.add("GET", self.BASE_URL + media_id, json=self.MEDIA_FIELDS)

            res_default = self.api.get_media_info(
                media_id=media_id
            )
            self.assertEqual(res_default.id, media_id)
            self.assertEqual(res_default.owner.id, self.instagram_business_id)

            res_fields = self.api.get_media_info(
                media_id=media_id,
                fields=["id", "timestamp", "media_type", "comments_count"],
                return_json=True
            )
            self.assertEqual(res_fields["id"], media_id)
            self.assertEqual(res_fields["comments_count"], 0)

    def testGetMediasInfo(self):
        media_ids = ["17861821972334188", "17864312515295083"]
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=self.MEDIAS_DEFAULT)
            m.add("GET", self.BASE_URL, json=self.MEDIAS_FIELDS)

            res_default = self.api.get_medias_info(
                media_ids=media_ids
            )
            for _id, data in iteritems(res_default):
                self.assertIn(_id, media_ids)
                self.assertIn(_id, data.id)

            res_fields = self.api.get_medias_info(
                media_ids=media_ids,
                fields=["id", "timestamp", "media_type", "comments_count"],
                return_json=True
            )
            for _id, data in iteritems(res_fields):
                self.assertIn(_id, media_ids)
                self.assertIn(_id, data["id"])

    def testGetTagsMedias(self):
        # test all items
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL + self.instagram_business_id + "/tags", json=self.TAGS_MEDIAS)
            m.add("GET", self.BASE_URL + self.instagram_business_id + "/tags", json=self.TAGS_MEDIAS_P1)
            m.add("GET", self.BASE_URL + self.instagram_business_id + "/tags", json=self.TAGS_MEDIAS_P2)

            res = self.api.get_tags_medias(
                user_id=self.instagram_business_id,
                fields=["id", "like_count", "media_type", "timestamp", "username"],
                count=4
            )

            self.assertEqual(len(res), 4)
            self.assertEqual(res[0].id, "18027939643230671")

            res_json = self.api.get_tags_medias(
                user_id=self.instagram_business_id,
                count=None,
                limit=3,
                return_json=True
            )
            self.assertEqual(len(res_json), 5)
            self.assertEqual(res_json[0]["id"], "18027939643230671")
