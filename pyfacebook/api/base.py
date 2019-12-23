"""
    Base Api Impl
"""
import six
import logging
import re

import requests
from requests import Response

from pyfacebook.error import PyFacebookError, PyFacebookException, ErrorMessage, ErrorCode
from pyfacebook.models import AccessToken
from pyfacebook.ratelimit import InstagramRateLimit, RateLimit


class BaseApi(object):
    VALID_API_VERSIONS = ["v3.3", "v4.0", "v5.0"]
    GRAPH_URL = "https://graph.facebook.com/"

    def __init__(
            self, app_id=None,
            app_secret=None,
            short_token=None,
            long_term_token=None,
            version=None,
            timeout=None,
            sleep_on_rate_limit=False,
            proxies=None,
            is_instagram=False,
            debug_http=False,
    ):
        self.app_id = app_id
        self.app_secret = app_secret
        self.short_token = short_token
        self.__timeout = timeout
        self.base_url = self.GRAPH_URL
        self.proxies = proxies
        self.session = requests.Session()
        self.sleep_on_rate_limit = sleep_on_rate_limit
        self.is_instagram = is_instagram
        self.instagram_business_id = None
        if self.is_instagram:
            self.rate_limit = InstagramRateLimit()
        else:
            self.rate_limit = RateLimit()
        self._debug_http = debug_http

        if version is None:
            # default version is last new.
            self.version = self.VALID_API_VERSIONS[-1]
        else:
            version = str(version)
            if not version.startswith('v'):
                version = 'v' + version
            version_regex = re.compile(r"^v\d.\d{1,2}$")
            match = version_regex.search(str(version))
            if match is not None:
                if version not in self.VALID_API_VERSIONS:
                    raise PyFacebookError({
                        "message": "Valid API version are {}".format(",".join(self.VALID_API_VERSIONS))
                    })
                else:
                    self.version = version
            else:
                self.version = self.VALID_API_VERSIONS[-1]

        if not (long_term_token or all([self.app_id, self.app_secret, self.short_token])):
            raise PyFacebookError({'message': 'Missing long term token or app account'})

        if long_term_token:
            self.token = long_term_token
        else:
            self.set_token(app_id=self.app_id, app_secret=self.app_secret, short_token=self.short_token)

        if debug_http:
            from six.moves import http_client
            http_client.HTTPConnection.debuglevel = 1

            logging.basicConfig()  # you need to initialize logging, otherwise you will not see anything from requests
            logging.getLogger().setLevel(logging.DEBUG)
            requests_log = logging.getLogger("requests.packages.urllib3")
            requests_log.setLevel(logging.DEBUG)
            requests_log.propagate = True

    def set_token(self, app_id, app_secret, short_token):
        response = self._request(
            method='GET',
            path='{}/oauth/access_token'.format(self.version),
            args={
                'grant_type': 'fb_exchange_token',
                'client_id': app_id,
                'client_secret': app_secret,
                'fb_exchange_token': short_token
            },
            enforce_auth=False
        )
        data = self._parse_response(response)
        self.token = data['access_token']

    def _request(self, path, method=None, args=None, post_args=None, enforce_auth=True):
        if method is None:
            method = 'GET'
        if args is None:
            args = dict()
        if post_args is not None:
            method = "POST"
        if enforce_auth:
            if post_args and "access_token" not in post_args:
                post_args["access_token"] = self.token
            elif "access_token" not in args:
                args["access_token"] = self.token
        try:
            response = self.session.request(
                method,
                self.base_url + path,
                timeout=self.__timeout,
                params=args,
                data=post_args,
                proxies=self.proxies
            )
        except requests.HTTPError as e:
            raise PyFacebookException(ErrorMessage(code=ErrorCode.HTTP_ERROR, message=e.args[0]))
        headers = response.headers
        # do update app rate limit
        if self.is_instagram:
            self.rate_limit.set_limit(headers, self.instagram_business_id)
        else:
            self.rate_limit.set_limit(headers)
        return response

    def _parse_response(self, response):
        # type: (Response) -> dict
        data = response.json()
        self._check_graph_error(data)
        return data

    @staticmethod
    def _check_graph_error(data):
        # type: (dict) -> None
        """
        Check the facebook response data. If have error raise a PyFacebookException.
        :param data: The data return by facebook.
        :return: None
        """
        if 'error' in data:
            error_data = data['error']
            raise PyFacebookException(error_data)

    def get_token_info(self, return_json=False):
        """
        Obtain the current access token info if provide the app_id and app_secret.

        Args:
            return_json (bool, optional):
                If True JSON data will be returned, instead of pyfacebook.AccessToken
        Returns:
            Current access token's info,  pyfacebook.AccessToken instance.
        """
        if all([self.app_id, self.app_secret]):
            access_token = "{0}|{1}".format(self.app_id, self.app_secret)
        else:
            access_token = self.token
        args = {
            "input_token": self.token,
            "access_token": access_token,
        }
        resp = self._request(
            '{0}/debug_token'.format(self.version),
            args=args
        )
        data = self._parse_response(resp.content.decode('utf-8'))

        if return_json:
            return data
        else:
            return AccessToken.new_from_json_dict(data['data'])
