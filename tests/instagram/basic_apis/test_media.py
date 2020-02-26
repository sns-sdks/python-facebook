import json
import unittest

import responses

import pyfacebook


class ApiMediaTest(unittest.TestCase):
    BASE_PATH = "testdata/instagram_basic/apidata/media/"

    with open(BASE_PATH + "user_medias_p1.json", "rb") as f:
        USER_MEDIAS_P1 = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "user_medias_p2.json", "rb") as f:
        USER_MEDIAS_P2 = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "media_info.json", "rb") as f:
        MEDIA_INFO = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "media_children.json", "rb") as f:
        MEDIA_CHILDREN = json.loads(f.read().decode("utf-8"))

    def setUp(self):
        self.api = pyfacebook.IgBasicApi(long_term_token="token")

    def testGetUserMedia(self):
        user_id = "17841406338772941"

        # test count
        with responses.RequestsMock() as m:
            m.add("GET", self.api.GRAPH_URL + "me/media", json=self.USER_MEDIAS_P1)

            medias = self.api.get_user_medias(
                count=4,
                limit=6
            )
            self.assertEqual(len(medias), 4)

        # test all medias
        with responses.RequestsMock() as m:
            m.add("GET", self.api.GRAPH_URL + user_id + "/media", json=self.USER_MEDIAS_P1)
            m.add("GET", self.api.GRAPH_URL + user_id + "/media", json=self.USER_MEDIAS_P2)

            medias_json = self.api.get_user_medias(
                user_id=user_id,
                count=None,
                limit=6,
                return_json=True
            )
            self.assertEqual(len(medias_json), 10)

    def testGetMediaInfo(self):
        media_id = "18027939643230671"

        with responses.RequestsMock() as m:
            m.add("GET", self.api.GRAPH_URL + media_id, json=self.MEDIA_INFO)

            media = self.api.get_media_info(
                media_id=media_id,
            )
            self.assertEqual(media.id, media_id)
            self.assertEqual(len(media.children), 2)

            media_json = self.api.get_media_info(
                media_id=media_id,
                return_json=True
            )
            self.assertEqual(media_json["id"], media_id)
            self.assertEqual(media_json["media_type"], "CAROUSEL_ALBUM")

    def testGetMediaChildren(self):
        media_id = "18027939643230671"

        with responses.RequestsMock() as m:
            m.add("GET", self.api.GRAPH_URL + media_id + "/children", json=self.MEDIA_CHILDREN)

            children = self.api.get_media_children(
                media_id=media_id,
            )
            self.assertEqual(len(children), 2)
            self.assertEqual(children[0].id, "17895013408404508")

            children_json_list = self.api.get_media_children(
                media_id=media_id,
                return_json=True
            )
            self.assertEqual(len(children_json_list), 2)
            self.assertEqual(children_json_list[0]["id"], "17895013408404508")
