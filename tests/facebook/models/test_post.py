import json
import unittest

import pyfacebook.model as models


class PostModelTest(unittest.TestCase):
    BASE_PATH = "testdata/facebook/models/posts/"

    with open(BASE_PATH + 'post.json', 'rb') as f:
        POST_INFO = json.loads(f.read().decode('utf-8'))

    def testPost(self):
        m = models.Post.new_from_json_dict(self.POST_INFO)

        self.assertEqual(m.id, "2121008874780932_2498598377021978")
        self.assertEqual(m.backdated_time, "2019-12-15T04:00:00+0000")
        self.assertEqual(len(m.attachments), 1)
        self.assertEqual(m.attachments[0].media_type, "link")
        self.assertEqual(m.attachments[0].media.image.height, 368)
        self.assertTrue(m.attachments[0].target.url)
        self.assertEqual(m.comments.total_count, 1)
        self.assertEqual(m.reactions.total_count, 3)
        self.assertEqual(m.reactions.viewer_reaction, "LIKE")
        self.assertEqual(m.like.total_count, 3)
        self.assertEqual(m.like.viewer_reaction, "like")
