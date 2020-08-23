import json
import unittest

import responses
from six import iteritems

import pyfacebook


class CommentTestApi(unittest.TestCase):
    BASE_PATH = "testdata/facebook/apidata/pictures/"
    BASE_URL = "https://graph.facebook.com/{}/".format(pyfacebook.Api.VALID_API_VERSIONS[-1])

    with open(BASE_PATH + "single_picture.json", "rb") as f:
        SINGLE_PICTURE = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "multi_pictures.json", "rb") as f:
        MULTI_PICTURE = json.loads(f.read().decode("utf-8"))

    def setUp(self):
        self.api = pyfacebook.Api(
            app_id="123456", app_secret="secret",
            long_term_token="token"
        )

    def testGetPictureInfo(self):
        page_id = "2121008874780932"
        with self.assertRaises(pyfacebook.PyFacebookException):
            self.api.get_picture(page_id=page_id, pic_type="not")

        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL + page_id + "/picture", json=self.SINGLE_PICTURE)

            picture = self.api.get_picture(
                page_id=page_id,
            )
            self.assertEqual(picture.height, 200)

        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL + page_id + "/picture", json=self.SINGLE_PICTURE)

            picture = self.api.get_picture(
                page_id=page_id, pic_type="large",
                return_json=True
            )
            self.assertEqual(picture["height"], 200)

    def testGetPictures(self):
        ids = ["2121008874780932", "20531316728"]

        with self.assertRaises(pyfacebook.PyFacebookException):
            self.api.get_pictures(ids=ids, pic_type="not")

        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL + "picture", json=self.MULTI_PICTURE)

            picture_dict = self.api.get_pictures(
                ids=ids
            )

            for _id, data in iteritems(picture_dict):
                self.assertIn(_id, ids)
                self.assertEqual(200, data.height)

        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL + "picture", json=self.MULTI_PICTURE)

            picture_dict = self.api.get_pictures(
                ids=ids,
                pic_type="large",
                return_json=True
            )

            for _id, data in iteritems(picture_dict):
                self.assertIn(_id, ids)
                self.assertEqual(200, data["height"])
