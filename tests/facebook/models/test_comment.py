import json
import unittest

import pyfacebook.models as models


class CommentModelTest(unittest.TestCase):
    BASE_PATH = "testdata/facebook/models/comments/"

    with open(BASE_PATH + 'comment.json', 'rb') as f:
        COMMENT_INFO = json.loads(f.read().decode('utf-8'))

    def testComment(self):
        m = models.Comment.new_from_json_dict(self.COMMENT_INFO)

        self.assertEqual(m.id, "2498598377021978_2498617433686739")
        self.assertEqual(m.comment_count, 0)
        self.assertEqual(m.attachment.media.image.height, 474)
