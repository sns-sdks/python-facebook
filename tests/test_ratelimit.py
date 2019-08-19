import json
import unittest

import responses

import pyfacebook


class RateLimitTest(unittest.TestCase):
    def setUp(self):
        self.base_url = "https://graph.facebook.com/"
        self.version = pyfacebook.Api.VALID_API_VERSIONS[-1]
        self.api = pyfacebook.Api(
            long_term_token='testToken',
        )

    def testInitializeRateLimit(self):
        info = self.api.rate_limit.info
        self.assertEqual(
            'Current Limit is RateLimit(call_count=0,total_cputime=0,total_time=0)',
            info
        )
        self.api.rate_limit.set_limit(headers={'x-app-usage': 'test'})
        self.assertEqual(self.api.rate_limit.call_count, 0)

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
    def testGetRateLimitIntervalBlank(self):
        headers = {'x-app-usage': ''}
        responses.add(
            method=responses.GET,
            url=self.base_url + '{0}/debug_token'.format(self.version),
            json={'data': {}},
            adding_headers=headers
        )
        self.api.get_token_info()
        self.assertEqual(1, self.api.rate_limit.get_sleep_interval())


class InstagramRateLimitTest(unittest.TestCase):
    def setUp(self) -> None:
        self.base_path = 'testdata/instagram/'
        self.base_url = "https://graph.facebook.com/"
        self.version = pyfacebook.InstagramApi.VALID_API_VERSIONS[-1]
        self.api = pyfacebook.InstagramApi(
            long_term_token='testToken',
            instagram_business_id='17841400455970028',
        )

    def testInitializeRateLimit(self):
        rate_limit = self.api.rate_limit
        self.assertEqual(rate_limit.type, 'instagram')
        self.assertTrue('reset_at' in rate_limit.info)
        self.api.rate_limit.set_limit({'x-business-use-case-usage': 'test'}, self.api.instagram_business_id)
        self.assertEqual(self.api.rate_limit.call_count, 0)

    @responses.activate
    def testSetRateLimit(self):
        with open(self.base_path + 'headers.json', 'rb') as f:
            headers = json.loads(f.read().decode('utf-8'))
        with open(self.base_path + 'page_info.json', 'rb') as f:
            page_data = json.loads(f.read().decode('utf-8'))
        responses.add(
            method=responses.GET,
            url=self.base_url + '{0}/{1}'.format(self.version, self.api.instagram_business_id),
            json=page_data,
            adding_headers=headers
        )
        self.api.get_user_info(username='facebook')
        self.assertEqual(12, self.api.rate_limit.call_count)
        self.assertEqual(72, self.api.rate_limit.total_cputime)
        self.assertEqual(10, self.api.rate_limit.total_time)
        self.assertTrue(self.api.rate_limit.reset_at > 0)
        self.assertEqual(20, self.api.rate_limit.get_sleep_interval())
