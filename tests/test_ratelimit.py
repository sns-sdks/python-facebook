import unittest

from pyfacebook.ratelimit import RateLimit


class RateLimitTest(unittest.TestCase):

    def testParseHeaders(self):
        headers = {"key": "None"}
        self.assertIsNone(RateLimit.parse_headers(headers, key="key"))

    def testAppLimit(self):
        headers = {'x-app-usage': '{"call_count":91,"total_cputime":15,"total_time":12}'}
        r = RateLimit()
        r.set_limit(headers)

        self.assertEqual(r.get_limit().call_count, 91)
        self.assertEqual(r.get_limit().max_percent(), 91)
        self.assertEqual(r.get_max_percent(), 91)
        self.assertEqual(r.get_sleep_seconds(), 2)

    def testBusinessLimit(self):
        r = RateLimit()

        headers = {
            "x-business-use-case-usage": "{\"112130216863063\":[{\"type\":\"pages\",\"call_count\":1,\"total_cputime\":1,\"total_time\":1,\"estimated_time_to_regain_access\":0}]}"}

        r.set_limit(headers)

        self.assertEqual(r.get_limit(object_id="112130216863063", endpoint="pages").call_count, 1)
