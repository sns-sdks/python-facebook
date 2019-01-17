import pyfacebook
import unittest


class PostsTest(unittest.TestCase):
    def setUp(self):
        self.api = pyfacebook.Api(
            long_term_token='test'
        )

    def testSimplePosts(self):
        data = self.api.get_posts(page_id=149515305173840, count=10)
        self.assertEqual(type(data), list)
