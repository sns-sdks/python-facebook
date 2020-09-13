import json
import unittest

import responses
from six import iteritems

import pyfacebook


class VideoApiTest(unittest.TestCase):
    BASE_PATH = "testdata/facebook/apidata/videos/"
    BASE_URL = "https://graph.facebook.com/{}/".format(pyfacebook.Api.VALID_API_VERSIONS[-1])

    with open(BASE_PATH + "page_videos_p1.json", "rb") as f:
        VIDEOS_PAGED_1 = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "page_videos_p2.json", "rb") as f:
        VIDEOS_PAGED_2 = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "video_info.json", "rb") as f:
        VIDEO_INFO = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "videos_info.json", "rb") as f:
        VIDEOS_INFO = json.loads(f.read().decode("utf-8"))

    with open(BASE_PATH + "video_caption.json", "rb") as f:
        VIDEO_CAPTION_INFO = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "video_captions.json", "rb") as f:
        VIDEO_CAPTIONS_INFO = json.loads(f.read().decode("utf-8"))

    def setUp(self):
        self.api = pyfacebook.Api(
            app_id="12345678",
            app_secret="secret",
            long_term_token="token",
            version="v8.0"
        )

    def testGetVideosByObject(self):
        page_id = "367152833370567"
        # Test count
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL + page_id + "/videos", json=self.VIDEOS_PAGED_1)

            videos = self.api.get_videos_by_object(
                object_id=page_id,
                count=3,
                limit=5,
                return_json=True,
            )
            self.assertEqual(len(videos), 3)

        # Test count is None
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL + page_id + "/videos", json=self.VIDEOS_PAGED_1)
            m.add("GET", self.BASE_URL + page_id + "/videos", json=self.VIDEOS_PAGED_2)

            videos = self.api.get_videos_by_object(
                object_id=page_id,
                count=None,
                limit=5,
            )
            self.assertEqual(len(videos), 9)

    def testGetVideoInfo(self):
        video_id = "320504219400220"
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL + video_id, json=self.VIDEO_INFO)

            video = self.api.get_video_info(
                video_id=video_id,
                fields=['id',
                        'description',
                        'created_time',
                        'embed_html',
                        'embeddable',
                        'is_crosspost_video',
                        'is_crossposting_eligible',
                        'is_episode',
                        'is_instagram_eligible',
                        'length',
                        'live_status',
                        'permalink_url',
                        'picture',
                        'published',
                        'status',
                        'updated_time',
                        "likes.summary(true).limit(0)",
                        "comments.summary(true).limit(0)"]
            )
            self.assertEqual(video.id, video_id)
            self.assertEqual(video.likes.total_count, 1525)

            video_json = self.api.get_video_info(
                video_id=video_id,
                return_json=True
            )
            self.assertEqual(video_json["id"], video_id)

    def testGetVideos(self):
        ids = ["320504219400220", "1237122236642185"]
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=self.VIDEOS_INFO)

            video_dict = self.api.get_videos(
                ids=ids,
            )
            for _id, data in iteritems(video_dict):
                self.assertIn(_id, ids)
                self.assertEqual(_id, data.id)

        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=self.VIDEOS_INFO)
            video_dict = self.api.get_videos(
                ids=ids,
                fields=["id", "description", "content_category", "created_time"],
                return_json=True
            )
            for _id, data in iteritems(video_dict):
                self.assertIn(_id, ids)
                self.assertEqual(_id, data["id"])

    def testGetCaptionByVideoID(self):
        video_id = "969222676905304"
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL + video_id + "/captions", json=self.VIDEO_CAPTION_INFO)

            captions = self.api.get_caption_by_video_id(
                video_id=video_id
            )
            self.assertEqual(len(captions), 1)
            self.assertEqual(captions[0].create_time, "1599928066")

            captions_json = self.api.get_caption_by_video_id(
                video_id=video_id,
                return_json=True
            )
            self.assertEqual(len(captions_json["data"]), 1)

    def testGetCaptionByVideoIDs(self):
        ids = ["969222676905304", "210174653594254"]

        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL + "captions", json=self.VIDEO_CAPTIONS_INFO)

            captions_dict = self.api.get_caption_by_video_ids(
                ids=ids,
            )
            for _id, data in iteritems(captions_dict):
                self.assertIn(_id, ids)

        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL + "captions", json=self.VIDEO_CAPTIONS_INFO)
            video_dict = self.api.get_caption_by_video_ids(
                ids=ids,
                return_json=True
            )
            for _id, data in iteritems(video_dict):
                self.assertIn(_id, ids)
