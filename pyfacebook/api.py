import json
import re

import requests

from pyfacebook.error import PyFacebookError
from pyfacebook.models import AccessToken, Page, Post
from pyfacebook.ratelimit import RateLimit
from pyfacebook.utils import constant


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

    def get_page_info(self, page_id=None, username=None, return_json=False):
        """
        Obtain give page's basic info.

        Args:
            page_id (int, optional)
                The id for you want to retrieve data
            username (str, optional)
                The username (page username) for you want to retrieve data
                Either page_id or username is required. if all given. use username.
            return_json (bool, optional):
                If True JSON data will be returned, instead of pyfacebook.Page
        :return:
        """
        if page_id:
            target = page_id
        elif username:
            target = username
        else:
            raise PyFacebookError({'message': "Specify at least one of page_id or username"})

        args = {
            'fields': ','.join(constant.PAGE_FIELDS)
        }

        resp = self._request(
            method='GET',
            path='{0}/{1}'.format(self.version, target),
            args=args
        )
        data = self._parse_response(resp.content.decode('utf-8'))
        if return_json:
            return data
        else:
            return Page.new_from_json_dict(data)

    def get_posts(self,
                  page_id=None,
                  username=None,
                  since_time=None,
                  until_time=None,
                  count=100):
        """
        Obtain give page's posts info.

        Args:
            page_id (int, optional)
                The id for you want to retrieve data
            username (str, optional)
                The username (page username) for you want to retrieve data
                Either page_id or username is required. if all given. use username.
            since_time (str, optional)
                The posts retrieve begin time.
            until_time ()
                The posts retrieve until time.
                If neither since_time or until_time, it will by now time.
            count (int, optional)
                The count to retrieve posts, may be paging.
        :return:
        """
        if page_id:
            target = page_id
        elif username:
            target = username
        else:
            raise PyFacebookError({'message': "Specify at least one of page_id or username"})

        args = {
            'fields': ','.join(set(constant.POST_BASIC_FIELDS + constant.POST_REACTIONS_FIELD)),
            'since': since_time,
            'until': until_time,
            'limit': count,
        }

        resp = self._request(
            method='GET',
            path='{0}/{1}/{2}'.format(self.version, target, 'posts'),
            args=args
        )

        data = self._parse_response(resp.content.decode('utf-8'))

        return [Post.new_from_json_dict(item) for item in data['data']]

    def get_post_info(self,
                      post_id=None,
                      return_json=False):
        """
        Obtain give page's basic info.

        Args:
            post_id (str)
                The id for you want to retrieve post.
            return_json (bool, optional):
                If True JSON data will be returned, instead of pyfacebook.Page
        :return:
        """
        if post_id is None:
            raise PyFacebookError({'message': "Must specify the post id"})

        args = {
            'fields': ','.join(set(constant.POST_BASIC_FIELDS + constant.POST_REACTIONS_FIELD))
        }
        resp = self._request(
            method='GET',
            path='{0}/{1}'.format(self.version, post_id),
            args=args
        )

        data = self._parse_response(resp.content.decode('utf-8'))
        if return_json:
            return data
        else:
            return Post.new_from_json_dict(data)
