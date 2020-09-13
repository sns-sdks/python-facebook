import json
import unittest

import pyfacebook.models as models


class PhotoModelTest(unittest.TestCase):
    BASE_PATH = "testdata/facebook/models/photos/"

    with open(BASE_PATH + 'photo.json', 'rb') as f:
        PHOTO_INFO = json.loads(f.read().decode('utf-8'))

    def testPhoto(self):
        m = models.Photo.new_from_json_dict(self.PHOTO_INFO)

        self.assertEqual(m.id, "166370841591183")
        self.assertEqual(m.album.id, "108824087345859")
        self.assertEqual(len(m.images), 8)
        self.assertEqual(m.webp_images[0].height, 800)
