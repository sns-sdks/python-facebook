import json
import unittest

import responses

import pyfacebook


class ApiPageTest(unittest.TestCase):
    BASE_PATH = "testdata/facebook/apidata/"
    BASE_URL = "https://graph.facebook.com/" + pyfacebook.Api.VALID_API_VERSIONS[-1] + "/"

    with open(BASE_PATH + "page.json", "rb") as f:
        PAGE_INFO = json.loads(f.read().decode("utf-8"))

    def setUp(self):
        self.api = pyfacebook.Api(
            long_term_token="token"
        )

    def testPage(self):
        page_id = "20531316728"
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL + page_id, json=self.PAGE_INFO)

            page = self.api.get_page_info(
                page_id=page_id,
            )
            self.assertEqual(page.id, "20531316728")
