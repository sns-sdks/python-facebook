import json
import unittest

import responses
from six import iteritems

import pyfacebook


class PhotoApiTest(unittest.TestCase):
    BASE_PATH = "testdata/facebook/apidata/photos/"
    BASE_URL = "https://graph.facebook.com/{}/".format(pyfacebook.Api.VALID_API_VERSIONS[-1])

    with open(BASE_PATH + "photos_page_1.json", "rb") as f:
        PHOTO_PAGED_1 = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "photos_page_2.json", "rb") as f:
        PHOTO_PAGED_2 = json.loads(f.read().decode("utf-8"))

    with open(BASE_PATH + "photo_info.json", "rb") as f:
        PHOTO_INFO = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "photos_info.json", "rb") as f:
        PHOTOS_INFO = json.loads(f.read().decode("utf-8"))

    def setUp(self):
        self.api = pyfacebook.Api(
            app_id="12345678",
            app_secret="secret",
            long_term_token="token",
            version="v8.0"
        )

    def testGetPhotosByObject(self):
        object_id = "145161477045453"

        # Test count
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL + object_id + "/photos", json=self.PHOTO_PAGED_1)

            photos = self.api.get_photos_by_object(
                object_id=object_id,
                count=3,
                limit=5,
                return_json=True,
            )
            self.assertEqual(len(photos), 3)

        # Test count is None
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL + object_id + "/photos", json=self.PHOTO_PAGED_1)
            m.add("GET", self.BASE_URL + object_id + "/photos", json=self.PHOTO_PAGED_2)

            photos = self.api.get_photos_by_object(
                object_id=object_id,
                count=None,
                limit=5,
            )
            self.assertEqual(len(photos), 10)

    def testGetPhotoInfo(self):
        photo_id = "166370841591183"

        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL + photo_id, json=self.PHOTO_INFO)

            photo = self.api.get_photo_info(
                photo_id=photo_id,
            )
            self.assertEqual(photo.id, photo_id)
            self.assertEqual(photo.album.id, "108824087345859")

            photo_json = self.api.get_photo_info(
                photo_id=photo_id,
                return_json=True
            )
            self.assertEqual(photo_json["id"], photo_id)

    def testGetPhotos(self):
        ids = ["166370841591183", "198814968346770"]

        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=self.PHOTOS_INFO)

            photo_dict = self.api.get_photos(
                ids=ids,
            )
            for _id, data in iteritems(photo_dict):
                self.assertIn(_id, ids)
                self.assertEqual(_id, data.id)

        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=self.PHOTOS_INFO)
            photo_dict = self.api.get_photos(
                ids=ids,
                return_json=True
            )
            for _id, data in iteritems(photo_dict):
                self.assertIn(_id, ids)
                self.assertEqual(_id, data["id"])
