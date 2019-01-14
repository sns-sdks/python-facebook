import json
import re

import requests

from pyfacebook.error import PyFacebookError
from pyfacebook.ratelimit import RateLimit
from pyfacebook.models import AccessToken, Page, Post


class Api(object):
    VALID_API_VERSIONS = ["v3.1", "v3.2"]
    GRAPH_URL = "https://graph.facebook.com/"
    INTERVAL_BETWEEN_REQUEST = 3  # seconds

    def __init__(
            self, app_id=None,
            app_secret=None,
            short_token=None,
            long_term_token=None,
            version=None,
            timeout=None,
            interval_between_request=None,  # if loop get data. should use this.
            sleep_on_rate_limit=False,
            proxies=None,
    ):
        self.app_id = app_id
        self.app_secret = app_secret
        self.short_token = short_token
        self.__timeout = timeout
        self.base_url = Api.GRAPH_URL
        self.proxies = proxies
        self.session = requests.Session()
        self.sleep_on_rate_limit = sleep_on_rate_limit
        self.rate_limit = RateLimit()

        self.interval_between_request = interval_between_request
        if self.interval_between_request is None:
            self.interval_between_request = Api.INTERVAL_BETWEEN_REQUEST
        if self.interval_between_request < 1:
            raise PyFacebookError({"message": "Min interval is 1"})

        if version is None:
            # default version is last new.
            self.version = Api.VALID_API_VERSIONS[-1]
        else:
            version_regex = re.compile("^\\d.\\d{1,2}$")
            match = version_regex.search(str(version))
            if match is not None:
                if str(version) not in Api.VALID_API_VERSIONS:
                    raise PyFacebookError({
                        "message": "Valid API version are {}".format(",".join(Api.VALID_API_VERSIONS))
                    })
                else:
                    self.version = "v" + str(version)

        if not (long_term_token or all([self.app_id, self.app_secret, self.short_token])):
            raise PyFacebookError({'message': 'Missing long term token or app account'})

        if long_term_token:
            self.token = long_term_token
        else:
            self.set_token(app_id=self.app_id, app_secret=self.app_secret, short_token=self.short_token)

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
        data = self._parse_response(response.content.decode('utf-8'))
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
            response = json.loads(e.read())
            raise PyFacebookError(response)
        headers = response.headers
        # do update app rate limit
        self.rate_limit.set_limit(headers)
        return response

    def _parse_response(self, json_data):
        try:
            data = json.loads(json_data)
        except ValueError:
            raise PyFacebookError(json_data)
        self._check_graph_error(data)
        return data

    @staticmethod
    def _check_graph_error(data):
        if 'error' in data:
            try:
                error = data['error']
                raise PyFacebookError(error)
            except (KeyError, TypeError):
                raise PyFacebookError({
                    'message': data
                })

    def get_token_info(self, return_json=False):
        """
        Obtain the current access token info if provide the app_id and app_secret.

        Args:
            return_json (bool, optional):
            If True JSON data will be returned, instead of pyfacebook.AccessToken
        :return:
        """
        if not all([self.app_id, self.app_secret]):
            raise PyFacebookError({
                'message': 'Get token info need provide app account.'
            })
        args = {
            "input_token": self.token,
            "access_token": "{0}|{1}".format(self.app_id, self.app_secret),
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
