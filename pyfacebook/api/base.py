"""
    Base Api Impl
"""
import six
import logging
import re
from typing import Dict, Optional, Union, List

import requests
from requests import Response
from requests_oauthlib import OAuth2Session
from requests_oauthlib.compliance_fixes.facebook import facebook_compliance_fix

from pyfacebook.error import PyFacebookError, PyFacebookException, ErrorMessage, ErrorCode
from pyfacebook.model import AccessToken, AuthAccessToken
from pyfacebook.ratelimit import InstagramRateLimit, RateLimit


class BaseApi(object):
    VALID_API_VERSIONS = ["v3.3", "v4.0", "v5.0"]
    GRAPH_URL = "https://graph.facebook.com/"
    DEFAULT_AUTHORIZATION_URL = 'https://www.facebook.com/dialog/oauth'
    DEFAULT_EXCHANGE_ACCESS_TOKEN_URL = 'https://graph.facebook.com/oauth/access_token'
    DEFAULT_REDIRECT_URI = 'https://localhost/'
    DEFAULT_SCOPE = []
    DEFAULT_STATE = 'PyFacebook'

    def __init__(self,
                 app_id=None,
                 app_secret=None,
                 short_token=None,
                 long_term_token=None,
                 application_only_auth=False,
                 version=None,
                 timeout=None,
                 sleep_on_rate_limit=False,
                 proxies=None,
                 is_instagram=False,
                 debug_http=False):
        """

        :param app_id: Your app id.
        :param app_secret: Your app secret.
        :param short_token: short-lived token
        :param long_term_token: long-lived token.
        :param application_only_auth: Use the `App Access Token` only.
        :param version: The version for the graph api.
        :param timeout: Request time out
        :param sleep_on_rate_limit: Use this will sleep between two request.
        :param proxies: Your proxies config.
        :param is_instagram:
        :param debug_http: Set to True to enable debug output from urllib when performing
        any HTTP requests.  Defaults to False.
        """
        self.app_id = app_id
        self.app_secret = app_secret
        self.short_token = short_token
        self.__timeout = timeout
        self.base_url = self.GRAPH_URL
        self.proxies = proxies
        self.session = requests.Session()
        self.sleep_on_rate_limit = sleep_on_rate_limit  # TODO
        self.instagram_business_id = None
        self._debug_http = debug_http
        self.authorization_url = self.DEFAULT_AUTHORIZATION_URL
        self.exchange_access_token_url = self.DEFAULT_EXCHANGE_ACCESS_TOKEN_URL
        self.redirect_uri = self.DEFAULT_REDIRECT_URI
        self.scope = self.DEFAULT_SCOPE
        self.auth_session = None  # Authorization session

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

        if long_term_token:
            self._access_token = long_term_token
        elif short_token and all([self.app_id, self.app_secret]):
            token = self.get_long_token(app_id=self.app_id, app_secret=self.app_secret, short_token=self.short_token)
            self._access_token = token.access_token
        elif application_only_auth and all([self.app_id, app_secret]):
            token = self.get_app_token()
            self._access_token = token.access_token
        else:
            raise PyFacebookException(ErrorMessage(
                code=ErrorCode.MISSING_PARAMS,
                message=(
                    "You can initial api with three methods: \n"
                    "1. Just provide long(short) lived token or app access token with param `long_term_token`.\n"
                    "2. Provide a short lived token and app credentials. Api will auto exchange long term token.\n"
                    "3. Provide app credentials and with application_only_auth set to true."
                    "Api will auto get and use app access token."
                )
            ))

        if debug_http:
            from six.moves import http_client
            http_client.HTTPConnection.debuglevel = 1

            logging.basicConfig()  # you need to initialize logging, otherwise you will not see anything from requests
            logging.getLogger().setLevel(logging.DEBUG)
            requests_log = logging.getLogger("requests.packages.urllib3")
            requests_log.setLevel(logging.DEBUG)
            requests_log.propagate = True

    def _request(self, path, method=None, args=None, post_args=None, enforce_auth=True):
        if method is None:
            method = 'GET'
        if args is None:
            args = dict()
        if post_args is not None:
            method = "POST"
        if enforce_auth:
            if post_args and "access_token" not in post_args:
                post_args["access_token"] = self._access_token
            elif "access_token" not in args:
                args["access_token"] = self._access_token
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
        # if self.is_instagram:
        #     self.rate_limit.set_limit(headers, self.instagram_business_id)
        # else:
        #     self.rate_limit.set_limit(headers)
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

    def get_long_token(self, short_token, app_id=None, app_secret=None, return_json=False):
        # type: (str, Optional[str], Optional[str], bool) -> Optional[Union[AuthAccessToken, Dict]]
        """
        Generate a long-lived token from a short-lived User access token.
        A long-lived token generally lasts about 60 days.
        :param app_id: Your app id.
        :param app_secret: Your app secret.
        :param short_token: short-lived token from the app.
        :param return_json: Set to false will return instance of AuthAccessToken.
        Or return json data. Default is false.
        """
        if app_id is None:
            app_id = self.app_id
            app_secret = self.app_secret

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
        if return_json:
            return data
        else:
            return AuthAccessToken.new_from_json_dict(data)

    def get_app_token(self, return_json=False):
        # type: (bool)-> Optional[Union[Dict, AuthAccessToken]]
        """
        Use app credentials to generate an app access token.
        :param return_json: Set to false will return instance of AuthAccessToken.
        Or return json data. Default is false.
        """
        resp = self._request(
            method="GET",
            path="{}/oauth/access_token".format(self.version),
            args={
                'grant_type': 'client_credentials',
                'client_id': self.app_id,
                'client_secret': self.app_secret,
            },
            enforce_auth=False
        )
        data = self._parse_response(resp)
        if return_json:
            return data
        else:
            return AuthAccessToken.new_from_json_dict(data)

    def get_token_info(self, input_token=None, return_json=False):
        # type: (Optional[str], bool) -> Optional[Union[Dict, AccessToken]]
        """
        Obtain the current access token info if provide the app_id and app_secret.
        :param input_token:
        :param return_json: Set to false will return instance of AccessToken.
        Or return json data. Default is false.
        """
        if input_token is None:
            input_token = self._access_token

        if all([self.app_id, self.app_secret]):
            access_token = "{0}|{1}".format(self.app_id, self.app_secret)
        else:
            access_token = self._access_token

        args = {
            "input_token": input_token,
            "access_token": access_token,
        }
        resp = self._request(
            '{0}/debug_token'.format(self.version),
            args=args
        )
        data = self._parse_response(resp)

        if return_json:
            return data["data"]
        else:
            return AccessToken.new_from_json_dict(data['data'])

    def get_authorization_url(self, redirect_uri=None, scope=None, **kwargs):
        # type: (str, List, Dict) -> (str, str)
        """
        Build authorization url to do authorize.

        Refer: https://developers.facebook.com/docs/facebook-login/manually-build-a-login-flow

        :param redirect_uri: The URL that you want to redirect the person logging in back to.
        Note: Your redirect uri need be set to `Valid OAuth redirect URIs` items in App Dashboard.
        :param scope: A list of Permissions to request from the person using your app.
        :param kwargs: Extend args for oauth.
        :return: Authorization url and state.
        """
        if not all([self.app_id, self.app_secret]):
            raise PyFacebookException(ErrorMessage(
                code=ErrorCode.MISSING_PARAMS,
                message="To do authorization need your app credentials"
            ))

        if redirect_uri is None:
            redirect_uri = self.redirect_uri

        if scope is None:
            scope = self.scope

        session = OAuth2Session(
            client_id=self.app_id, scope=scope, redirect_uri=redirect_uri,
            state=self.DEFAULT_STATE, **kwargs
        )
        self.auth_session = facebook_compliance_fix(session)

        authorization_url, state = self.auth_session.authorization_url(
            url=self.authorization_url
        )

        return authorization_url, state

    def exchange_access_token(self, response, return_json=False):
        # type: (str, bool) -> Union[AuthAccessToken, Dict]
        """
        :param response: The whole response url for your previous authorize step.
        :param return_json: Set to false will return instance of AuthAccessToken.
        Or return json data. Default is false.
        :return:
        """
        if self.auth_session is None:
            raise PyFacebookException(ErrorMessage(
                code=ErrorCode.MISSING_PARAMS,
                message="exchange token should do authorize first"
            ))

        self.auth_session.fetch_token(
            self.exchange_access_token_url, client_secret=self.app_secret,
            authorization_response=response
        )

        self._access_token = self.auth_session.access_token

        if return_json:
            return self.auth_session.token
        else:
            return AuthAccessToken.new_from_json_dict(self.auth_session.token)
