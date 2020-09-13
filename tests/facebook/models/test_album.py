import json
import unittest

import pyfacebook.models as models


class AlbumModelTest(unittest.TestCase):
    BASE_PATH = "testdata/facebook/models/albums/"

    with open(BASE_PATH + 'album.json', 'rb') as f:
        ALBUM_INFO = json.loads(f.read().decode('utf-8'))

    def testAlbum(self):
        m = models.Album.new_from_json_dict(self.ALBUM_INFO)

        self.assertEqual(m.id, "145161477045453")
        self.assertEqual(m.cover_photo.id, "198814975013436")
        self.assertEqual(m.type, "wall")
