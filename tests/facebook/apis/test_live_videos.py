import json
import unittest

import responses
from six import iteritems

import pyfacebook


class LiveVideoApiTest(unittest.TestCase):
    BASE_PATH = "testdata/facebook/apidata/live/"
    BASE_URL = "https://graph.facebook.com/v8.0/"

    with open(BASE_PATH + "live_videos_p1.json", "rb") as f:
        LIVE_VIDEOS_PAGED_1 = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "live_videos_p2.json", "rb") as f:
        LIVE_VIDEOS_PAGED_2 = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "live_video.json", "rb") as f:
        LIVE_VIDEO = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "live_videos.json", "rb") as f:
        LIVE_VIDEOS = json.loads(f.read().decode("utf-8"))

    def setUp(self):
        self.api = pyfacebook.Api(
            app_id="12345678",
            app_secret="secret",
            long_term_token="token",
            version="v8.0"
        )

    def testGetLiveVideosByObject(self):
        page_id = "2121008874780932"

        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL + page_id + "/live_videos", json=self.LIVE_VIDEOS_PAGED_1)
            m.add("GET", self.BASE_URL + page_id + "/live_videos", json=self.LIVE_VIDEOS_PAGED_2)

            live_videos = self.api.get_live_videos_by_object(
                object_id=page_id,
                count=None,
                limit=2,
            )
            self.assertEqual(len(live_videos), 4)

        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL + page_id + "/live_videos", json=self.LIVE_VIDEOS_PAGED_1)
            m.add("GET", self.BASE_URL + page_id + "/live_videos", json=self.LIVE_VIDEOS_PAGED_2)

            live_videos = self.api.get_live_videos_by_object(
                object_id=page_id,
                count=3,
                limit=2,
                return_json=True
            )
            self.assertEqual(len(live_videos), 3)

    def testGetLiveVideo(self):
        vid = "2814245952123884"

        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL + vid, json=self.LIVE_VIDEO)

            live_video = self.api.get_live_video_info(
                live_video_id=vid,
                fields=["id", "title", "creation_time", "status"],
            )
            self.assertEqual(live_video.id, vid)
            self.assertEqual(live_video.status, "VOD")

            lv_json = self.api.get_live_video_info(
                live_video_id=vid,
                return_json=True
            )
            self.assertEqual(lv_json["id"], vid)

    def testGetLiveVideos(self):
        ids = ["2809188389296307", "2814245952123884"]

        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=self.LIVE_VIDEOS)

            video_dict = self.api.get_live_videos(
                ids=ids,
            )
            for _id, data in iteritems(video_dict):
                self.assertIn(_id, ids)
                self.assertEqual(_id, data.id)

            video_dict = self.api.get_live_videos(
                ids=ids,
                fields=["id", "description", "content_category", "created_time"],
                return_json=True
            )
            for _id, data in iteritems(video_dict):
                self.assertIn(_id, ids)
                self.assertEqual(_id, data["id"])


class LiveVideoInputStream(unittest.TestCase):
    BASE_PATH = "testdata/facebook/apidata/live/"
    BASE_URL = "https://graph.facebook.com/v8.0/"

    with open(BASE_PATH + "stream.json", "rb") as f:
        STREAM = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "streams.json", "rb") as f:
        STREAMS = json.loads(f.read().decode("utf-8"))

    def setUp(self):
        self.api = pyfacebook.Api(
            app_id="12345678",
            app_secret="secret",
            long_term_token="token",
            version="v8.0"
        )

    def testGetInputStream(self):
        stream_id = "2814245955457217"

        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL + stream_id, json=self.STREAM)

            stream = self.api.get_live_video_input_stream(
                live_video_input_stream_id=stream_id,
                fields=["id", "dash_ingest_url", "is_master", "stream_health"],
            )

            self.assertEqual(stream.id, stream_id)
            self.assertEqual(stream.stream_health.video_bitrate, 0)

            stream_json = self.api.get_live_video_input_stream(
                live_video_input_stream_id=stream_id,
                return_json=True
            )
            self.assertEqual(stream_json["id"], stream_id)

    def testGetInputStreams(self):
        ids = ["2809188399296306", "2814245955457217"]

        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=self.STREAMS)

            stream_dict = self.api.get_live_video_input_streams(
                ids=ids,
            )
            for _id, data in iteritems(stream_dict):
                self.assertIn(_id, ids)
                self.assertEqual(_id, data.id)

            stream_dict = self.api.get_live_video_input_streams(
                ids=ids,
                fields=["id", "description", "content_category", "created_time"],
                return_json=True
            )
            for _id, data in iteritems(stream_dict):
                self.assertIn(_id, ids)
                self.assertEqual(_id, data["id"])
