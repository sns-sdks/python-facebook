import json
import re

import requests

from pyfacebook.error import PyFacebookError
from pyfacebook.ratelimit import RateLimit


class Api(object):
    VALID_API_VERSIONS = ["3.1", "3.2"]
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
        self.__timeout = timeout
        self.base_url = Api.GRAPH_URL
        self.proxies = proxies
        self.session = requests.Session()
        self.sleep_on_rate_limit = sleep_on_rate_limit

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

        if not (long_term_token or all([app_id, app_secret, short_token])):
            raise PyFacebookError({'message': 'Missing long term token or app account'})

        if long_term_token:
            self.token = long_term_token
        else:
            self.set_token(app_id=app_id, app_secret=app_secret, short_token=short_token)

        self.rate_limit = RateLimit()

        if interval_between_request is None:
            self.interval_between_request = Api.INTERVAL_BETWEEN_REQUEST
        if interval_between_request < 1:
            raise PyFacebookError({"message": "Min interval is 1"})

    def set_token(self, app_id, app_secret, short_token):
        response = self._request(
            method='GET',
            path='{}/oauth/access_token',
            args={
                'grant_type': 'fb_exchange_token',
                'client_id': app_id,
                'client_secret': app_secret,
                'fb_exchange_token': short_token
            }
        )
        if 'access_token' in response:
            self.token = response['access_token']
        else:
            raise PyFacebookError(response)

    def _request(self, path, method=None, args=None, post_args=None):
        if method is None:
            method = 'GET'
        if args is None:
            args = dict()
        if post_args is not None:
            method = "POST"
        if self.token:
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
        if "json" in headers["content-type"]:
            result = response.json()
        else:
            raise PyFacebookError({response.text})

        return result
