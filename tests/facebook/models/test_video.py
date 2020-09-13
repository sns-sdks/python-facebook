import json
import unittest

import pyfacebook.models as models


class VideoModelTest(unittest.TestCase):
    BASE_PATH = "testdata/facebook/models/videos/"

    with open(BASE_PATH + 'video.json', 'rb') as f:
        VIDEO_INFO = json.loads(f.read().decode('utf-8'))
    with open(BASE_PATH + 'caption.json', 'rb') as f:
        CAPTION_INFO = json.loads(f.read().decode('utf-8'))

    def testVideo(self):
        m = models.Video.new_from_json_dict(self.VIDEO_INFO)

        self.assertEqual(m.id, "969222676905304")
        self.assertEqual(m.created_time, "2020-09-12T09:53:06+0000")
        self.assertEqual(len(m.content_tags), 2)
        self.assertEqual(m.format[0].height, 229)
        self.assertEqual(m.place.id, "406584169736960")
        self.assertEqual(m.place.location.zip, "100037")
        self.assertEqual(m.status.video_status, "ready")

        self.assertEqual(m.privacy.value, "EVERYONE")
        self.assertFalse(m.is_crosspost_video)

        self.assertEqual(m.likes.total_count, 1525)
        self.assertEqual(m.comments.total_count, 139)

    def testCaption(self):
        m = models.VideoCaption.new_from_json_dict(self.CAPTION_INFO)

        self.assertEqual(m.locale, "zh_CN")
        self.assertEqual(m.create_time, "1599928066")
