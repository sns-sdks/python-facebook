import json
import unittest

import responses
from six import iteritems

import pyfacebook


class LiveVideoApiTest(unittest.TestCase):
    BASE_PATH = "testdata/facebook/apidata/live/"
    BASE_URL = "https://graph.facebook.com/{}/".format(pyfacebook.Api.VALID_API_VERSIONS[-1])

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
            version=pyfacebook.Api.VALID_API_VERSIONS[-1]
        )

    def testGetLiveVideosByObject(self):
        page_id = "2121008874780932"

        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL + page_id + "/live_videos", json=self.LIVE_VIDEOS_PAGED_1)
            m.add("GET", self.BASE_URL + page_id + "/live_videos", json=self.LIVE_VIDEOS_PAGED_2)


class LiveVideoInputStream(unittest.TestCase):
    BASE_PATH = "testdata/facebook/apidata/live/"
    BASE_URL = "https://graph.facebook.com/{}/".format(pyfacebook.Api.VALID_API_VERSIONS[-1])

    with open(BASE_PATH + "stream.json", "rb") as f:
        STEAM = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "streams.json", "rb") as f:
        STEAMS = json.loads(f.read().decode("utf-8"))

    def setUp(self):
        self.api = pyfacebook.Api(
            app_id="12345678",
            app_secret="secret",
            long_term_token="token",
            version=pyfacebook.Api.VALID_API_VERSIONS[-1]
        )
