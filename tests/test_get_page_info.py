import pyfacebook
import unittest


class PageInfoTest(unittest.TestCase):
    def setUp(self):
        self.api = pyfacebook.Api(
           long_term_token='test'
        )

    def testSimplePageInfo(self):
        data = self.api.get_page_info(page_id=149515305173840)
        print(data)
        self.assertEqual(type(data), pyfacebook.Page)
