import json
import unittest

import pyfacebook.models as models


class LiveVideoModelTest(unittest.TestCase):
    BASE_PATH = "testdata/facebook/models/live/"

    with open(BASE_PATH + 'live_video.json', 'rb') as f:
        LIVE_VIDEO_INFO = json.loads(f.read().decode('utf-8'))

    def testLiveVideo(self):
        m = models.LiveVideo.new_from_json_dict(self.LIVE_VIDEO_INFO)

        self.assertEqual(m.id, "178598660650827")
        self.assertEqual(m.status, "LIVE")
        self.assertEqual(m.ingest_streams[0].stream_id, "0")
        self.assertEqual(m.ingest_streams[0].stream_health.video_bitrate, 2511983)
        self.assertEqual(m.comments.total_count, 45)
