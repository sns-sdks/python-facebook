import unittest
import pyfacebook


class PostInfoTest(unittest.TestCase):
    def setUp(self):
        self.api = pyfacebook.Api(
            long_term_token='test'
        )

    def testSimplePage(self):
        data = self.api.get_post_info(post_id='321662419491_10156176725159492')
        self.assertEqual(type(data), pyfacebook.Post)
