import json
import unittest

import pyfacebook.models as models


class PostModelTest(unittest.TestCase):
    BASE_PATH = "testdata/facebook/models/posts/"

    with open(BASE_PATH + 'post.json', 'rb') as f:
        POST_INFO = json.loads(f.read().decode('utf-8'))

    def testPost(self):
        m = models.Post.new_from_json_dict(self.POST_INFO)

        self.assertEqual(m.id, "565225540184937_4018908568149933")
        self.assertEqual(m.created_time, "2020-02-18T05:20:33+0000")
        self.assertEqual(len(m.attachments), 1)
        self.assertEqual(m.attachments[0].media_type, "album")
        self.assertEqual(len(m.attachments[0].subattachments), 7)
        self.assertEqual(m.attachments[0].subattachments[0].media.image.height, 405)
        self.assertTrue(m.attachments[0].target.url)
        self.assertEqual(m.comments.total_count, 47)
        self.assertEqual(m.reactions.total_count, 8878)
        self.assertEqual(m.reactions.viewer_reaction, "NONE")
        self.assertEqual(m.like.total_count, 8575)
