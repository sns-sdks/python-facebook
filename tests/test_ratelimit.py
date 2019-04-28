import unittest

import responses

import pyfacebook


class RateLimitTest(unittest.TestCase):
    def setUp(self):
        self.base_url = "https://graph.facebook.com/"
        self.version = "v3.2"
        self.api = pyfacebook.Api(
            long_term_token='testToken',
        )

    def testInitializeRateLimit(self):
        info = self.api.rate_limit.info()
        self.assertEqual(
            'Current Limit is RateLimit(call_count=0,total_cputime=0,total_time=0)',
            info
        )

    @responses.activate
    def testSetRateLimit(self):
        headers = {'x-app-usage': '{"call_count":10,"total_cputime":25,"total_time":12}'}
        responses.add(
            method=responses.GET,
            url=self.base_url + '{0}/debug_token'.format(self.version),
            json={'data': {}},
            adding_headers=headers
        )
        self.api.get_token_info()
        self.assertEqual(10, self.api.rate_limit.call_count)
        self.assertEqual(25, self.api.rate_limit.total_cputime)
        self.assertEqual(12, self.api.rate_limit.total_time)
        self.assertEqual(3, self.api.rate_limit.get_sleep_interval())

    @responses.activate
    def testGetRateLimitIntervalLess100(self):
        headers = {'x-app-usage': '{"call_count":91,"total_cputime":15,"total_time":12}'}
        responses.add(
            method=responses.GET,
            url=self.base_url + '{0}/debug_token'.format(self.version),
            json={'data': {}},
            adding_headers=headers
        )
        self.api.get_token_info()
        self.assertEqual(60 * 10, self.api.rate_limit.get_sleep_interval())

    @responses.activate
    def testGetRateLimitIntervalMore100(self):
        headers = {'x-app-usage': '{"call_count":150,"total_cputime":15,"total_time":12}'}
        responses.add(
            method=responses.GET,
            url=self.base_url + '{0}/debug_token'.format(self.version),
            json={'data': {}},
            adding_headers=headers
        )
        self.api.get_token_info()
        self.assertEqual(60 * 20, self.api.rate_limit.get_sleep_interval())

    @responses.activate
    def testGetRateLimitIntervalLess90(self):
        headers = {'x-app-usage': '{"call_count":89,"total_cputime":15,"total_time":12}'}
        responses.add(
            method=responses.GET,
            url=self.base_url + '{0}/debug_token'.format(self.version),
            json={'data': {}},
            adding_headers=headers
        )
        self.api.get_token_info()
        self.assertEqual(60 * 5, self.api.rate_limit.get_sleep_interval())

    @responses.activate
    def testGetRateLimitIntervalLess90(self):
        headers = {'x-app-usage': ''}
        responses.add(
            method=responses.GET,
            url=self.base_url + '{0}/debug_token'.format(self.version),
            json={'data': {}},
            adding_headers=headers
        )
        self.api.get_token_info()
        self.assertEqual(1, self.api.rate_limit.get_sleep_interval())
