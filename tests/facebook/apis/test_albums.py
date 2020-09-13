import json
import unittest

import responses
from six import iteritems

import pyfacebook


class AlbumApiTest(unittest.TestCase):
    BASE_PATH = "testdata/facebook/apidata/albums/"
    BASE_URL = "https://graph.facebook.com/{}/".format(pyfacebook.Api.VALID_API_VERSIONS[-1])

    with open(BASE_PATH + "albums_paged_1.json", "rb") as f:
        ALBUM_PAGED_1 = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "albums_paged_2.json", "rb") as f:
        ALBUM_PAGED_2 = json.loads(f.read().decode("utf-8"))

    with open(BASE_PATH + "album_info.json", "rb") as f:
        ALBUM_INFO = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "albums_info.json", "rb") as f:
        ALBUMS_INFO = json.loads(f.read().decode("utf-8"))

    def setUp(self):
        self.api = pyfacebook.Api(
            app_id="12345678",
            app_secret="secret",
            long_term_token="token",
            version="v8.0"
        )

    def testGetAlbumByObject(self):
        object_id = "367152833370567"

        # Test count
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL + object_id + "/albums", json=self.ALBUM_PAGED_1)

            albums = self.api.get_albums_by_object(
                object_id=object_id,
                count=3,
                limit=5,
                return_json=True,
            )
            self.assertEqual(len(albums), 3)

        # Test count is None
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL + object_id + "/albums", json=self.ALBUM_PAGED_1)
            m.add("GET", self.BASE_URL + object_id + "/albums", json=self.ALBUM_PAGED_2)

            albums = self.api.get_albums_by_object(
                object_id=object_id,
                count=None,
                limit=5,
            )
            self.assertEqual(len(albums), 10)

    def testGetAlbumInfo(self):
        album_id = "372558296163354"

        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL + album_id, json=self.ALBUM_INFO)

            album = self.api.get_album_info(
                album_id=album_id,
            )
            self.assertEqual(album.id, album_id)
            self.assertEqual(album.cover_photo.id, "3293405020745319")

            album_json = self.api.get_album_info(
                album_id=album_id,
                return_json=True
            )
            self.assertEqual(album_json["id"], album_id)

    def testGetAlbums(self):
        ids = ["372558296163354", "443259089093274"]

        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=self.ALBUMS_INFO)

            album_dict = self.api.get_albums(
                ids=ids,
            )
            for _id, data in iteritems(album_dict):
                self.assertIn(_id, ids)
                self.assertEqual(_id, data.id)

        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=self.ALBUMS_INFO)
            album_dict = self.api.get_albums(
                ids=ids,
                fields=["id", "description", "content_category", "created_time"],
                return_json=True
            )
            for _id, data in iteritems(album_dict):
                self.assertIn(_id, ids)
                self.assertEqual(_id, data["id"])
