"""
    Base Graph API impl
"""
import hashlib
import hmac
import logging
import re
import time
from urllib.parse import parse_qsl, urlparse
from typing import Dict, List, Optional, Tuple

import requests
from requests import Response
from requests_oauthlib.oauth2_session import OAuth2Session
from requests_oauthlib.compliance_fixes.facebook import facebook_compliance_fix

from pyfacebook import RateLimit, PercentSecond, FacebookError, LibraryError

logger = logging.getLogger(__name__)


class GraphAPI:
    VALID_API_VERSIONS = [
        "v3.3",
        "v4.0",
        "v5.0",
        "v6.0",
        "v7.0",
        "v8.0",
        "v9.0",
        "v10.0",
        "v11.0",
    ]
    GRAPH_URL = "https://graph.facebook.com/"
    AUTHORIZATION_URL = "https://www.facebook.com/dialog/oauth"
    EXCHANGE_ACCESS_TOKEN_URL = "https://graph.facebook.com/oauth/access_token"
    DEFAULT_REDIRECT_URI = "https://localhost/"
    DEFAULT_SCOPE = ["public_profile"]
    STATE = "PyFacebook"

    def __init__(
        self,
        app_id: Optional[str] = None,
        app_secret: Optional[str] = None,
        access_token: Optional[str] = None,
        application_only_auth: bool = False,
        oauth_flow: bool = False,
        version: Optional[str] = None,
        sleep_on_rate_limit: bool = True,
        sleep_seconds_mapping: Optional[Dict[int, int]] = None,
        base_url: Optional[str] = None,
        timeout: Optional[int] = None,
        proxies: Optional[dict] = None,
        instagram_business_id: Optional[str] = None,
    ):
        self.app_id = app_id
        self.app_secret = app_secret
        self.access_token = access_token

        self.session = requests.Session()
        self.__timeout = timeout
        self.proxies = proxies
        self.sleep_on_rate_limit = sleep_on_rate_limit
        self.sleep_seconds_mapping = sleep_seconds_mapping
        self.rate_limit = RateLimit()
        self.instagram_business_id = instagram_business_id

        # if provide url override
        self.base_url = self.GRAPH_URL
        if base_url is not None:
            self.base_url = base_url

        # version check
        if version is None:
            # default version is last new.
            self.version = self.VALID_API_VERSIONS[-1]
        else:
            version = str(version)
            if not version.startswith("v"):
                version = "v" + version
            version_regex = re.compile(r"^v\d*.\d{1,2}$")
            match = version_regex.search(str(version))
            if match is not None:
                if version not in self.VALID_API_VERSIONS:
                    raise LibraryError(
                        {
                            "message": f"Valid API version are {','.join(self.VALID_API_VERSIONS)}"
                        }
                    )
                else:
                    self.version = version
            else:
                raise LibraryError(
                    {
                        "message": f"Invalid version {version}. You can provide with like: 5.0 or v5.0"
                    }
                )

        # Token
        if access_token:
            self.access_token = access_token
        elif application_only_auth and all([self.app_id, self.app_secret]):
            data = self.get_app_token()
            self.access_token = data["access_token"]
        elif oauth_flow and all([self.app_id, self.app_secret]):
            pass
        else:
            raise LibraryError({"message": "Need access token"})

    @staticmethod
    def _build_sleep_seconds_resource(
        sleep_seconds_mapping: Optional[Dict[int, int]]
    ) -> Optional[List[PercentSecond]]:
        """
        Sort and convert data
        :param sleep_seconds_mapping: mapping for sleep.
        :return:
        """
        if sleep_seconds_mapping is None:
            return None
        mapping_list = [
            PercentSecond(percent=p, seconds=s)
            for p, s in sleep_seconds_mapping.items()
        ]
        return sorted(mapping_list, key=lambda ps: ps.percent)

    @staticmethod
    def _generate_secret_proof(
        access_token: str, secret: Optional[str] = None
    ) -> Optional[str]:
        """
        :param access_token:
        :param secret: App secret
        :return:
        """
        if secret is None:
            logger.debug(
                "Calls from a server can be better secured by adding a parameter called appsecret_proof. "
                "And need your app secret."
            )
            return None
        return hmac.new(
            secret.encode("utf-8"),
            msg=access_token.encode("utf-8"),
            digestmod=hashlib.sha256,
        ).hexdigest()

    def _append_token(self, args: Optional[dict]) -> dict:
        """
        Append access token and secret_proof parameter of parameters.
        :param args: Original parameters.
        :return: New parameters.
        """
        args = {} if args is None else args
        if "access_token" not in args:
            args["access_token"] = self.access_token
        # Begin with v5.0, appsecret_proof parameter can improve requests secure.
        # Refer: https://developers.facebook.com/docs/graph-api/securing-requests/
        secret_proof = self._generate_secret_proof(
            args["access_token"], self.app_secret
        )
        args["appsecret_proof"] = secret_proof
        return args

    def _request(
        self,
        url: str,
        args: Optional[dict] = None,
        post_args: Optional[dict] = None,
        verb: str = "GET",
        auth_need: bool = True,
    ) -> Response:
        """
        :param url: Resource url for Graph.
        :param args: Query parameters.
        :param post_args: Form parameters.
        :param verb: HTTP method
        :param auth_need: Whether need access token.
        :return:
        """
        if auth_need:
            if verb == "GET" or verb == "DELETE":
                args = self._append_token(args=args)
            elif verb == "POST":
                post_args = self._append_token(args=post_args)

        if not url.startswith("http"):
            url = self.base_url + url

        try:
            response = self.session.request(
                method=verb,
                url=url,
                timeout=self.__timeout,
                params=args,
                data=post_args,
                proxies=self.proxies,
            )
        except requests.HTTPError as ex:
            raise LibraryError({"message": ex.args})

        # check headers
        headers = response.headers
        self.rate_limit.set_limit(headers)
        if self.sleep_on_rate_limit:
            sleep_seconds = self.rate_limit.get_sleep_seconds(
                sleep_data=self.sleep_seconds_mapping
            )
            time.sleep(sleep_seconds)
        return response

    def _parse_response(self, response: Response) -> dict:
        """
        :param response: Response from graph api.
        :return: json data
        """
        content_type = response.headers["Content-Type"]
        if "json" in content_type:
            data = response.json()
            self._check_graph_error(data=data)
            return data
        elif "image/" in content_type:
            data = {
                "data": response.content,
                "content-type": content_type,
                "url": response.url,
            }
            return data
        else:
            raise LibraryError({"message": "Wrong response, not json or image"})

    @staticmethod
    def _check_graph_error(data: dict):
        """
        :param data: Data from response
        """
        if "error" in data:
            error_data = data["error"]
            raise FacebookError(error_data)

    def get(self, path, args):
        """
        Send GET request.

        :param path: path for resource.
        :param args: args for request.
        :return: Response data
        """
        resp = self._request(
            url=f"{self.version}/{path}",
            args=args,
        )
        data = self._parse_response(resp)
        return data

    def get_object(self, object_id: str, fields: str = "", **kwargs) -> dict:
        """
        Get object information by object id.

        :param object_id: ID for object(user,page,event...).
        :param fields: Comma-separated string for object fields which you want.
        :param kwargs: Additional parameters for object.
        :return: Response data
        """
        args = {"fields": fields}
        if kwargs:
            args.update(kwargs)

        resp = self._request(
            url=f"{self.version}/{object_id}",
            args=args,
        )
        data = self._parse_response(resp)
        return data

    def get_objects(self, ids: str, fields: str = "", **kwargs) -> dict:
        """
        Get objects information by multi object ids.

        :param ids: Comma-separated string for object ids which you want.
        :param fields: Comma-separated string for object fields which you want.
        :param kwargs: Additional parameters for object.
        :return: Response data
        """
        args = {"ids": ids, "fields": fields}
        if kwargs:
            args.update(kwargs)

        resp = self._request(url=f"{self.version}", args=args)
        data = self._parse_response(resp)
        return data

    def get_connection(
        self,
        object_id: str,
        connection: str,
        **kwargs,
    ) -> dict:
        """
        Get connections objects for object by id. Like get page medias by page id.

        :param object_id: ID for object(user,page,event...).
        :param connection: Connection name for object, Like(posts,comments...).
        :param kwargs: Additional parameters for different connections.
        :return: Response data
        """
        resp = self._request(
            url=f"{self.version}/{object_id}/{connection}", args=kwargs
        )
        data = self._parse_response(resp)
        return data

    def get_full_connections(
        self,
        object_id: str,
        connection: str,
        count: Optional[int] = 10,
        limit: Optional[int] = None,
        **kwargs,
    ) -> dict:
        """
        Get connections objects for object by id. Like get page medias by page id.

        :param object_id: ID for object(user,page,event...).
        :param connection: Connection name for object, Like(posts,comments...).
        :param count: The count will retrieve objects. Default is None will get all data.
        :param limit: Each request retrieve objects count.
            For most connections should no more than 100. Default is None will use api default limit.
        :param kwargs: Additional parameters for different connections.
        :return: Combined Response data
        """

        data, data_set, paging = {}, [], None
        while True:
            # sometimes may not return limit.
            if limit is not None:
                kwargs["limit"] = limit

            data = self.get_connection(
                object_id=object_id,
                connection=connection,
                **kwargs,
            )
            # Append this request data
            data_set.extend(data["data"])
            if count is not None and len(data_set) > count:
                data_set = data_set[:count]
                break

            # check next pagination
            paging, _next = data.get("paging"), None
            if paging is not None:
                _next = paging.get("next")
            if not _next:
                break
            # parse next url args as new args
            kwargs = dict(parse_qsl(urlparse(_next).query))

        # Replace the data list in data.
        data["data"] = data_set
        return data

    def _get_oauth_session(
        self,
        redirect_uri: Optional[str] = None,
        scope: Optional[List[str]] = None,
        **kwargs,
    ) -> OAuth2Session:
        """
        :param redirect_uri: The URL that you want to redirect the person logging in back to.
        :param scope: A list of permission string to request from the person using your app.
        :param kwargs: Additional parameters for oauth.
        :return: OAuth Session
        """
        # check app credentials
        if not all([self.app_id, self.app_secret]):
            raise LibraryError({"message": "OAuth need your app credentials"})

        if redirect_uri is None:
            redirect_uri = self.DEFAULT_REDIRECT_URI
        if scope is None:
            scope = self.DEFAULT_SCOPE

        session = OAuth2Session(
            client_id=self.app_id,
            scope=scope,
            redirect_uri=redirect_uri,
            state=self.STATE,
            **kwargs,
        )
        session = facebook_compliance_fix(session)
        return session

    def get_authorization_url(
        self,
        redirect_uri: Optional[str] = None,
        scope: Optional[List[str]] = None,
        **kwargs,
    ) -> Tuple[str, str]:
        """
        Build authorization url to do oauth.
        Refer: https://developers.facebook.com/docs/facebook-login/manually-build-a-login-flow

        :param redirect_uri: The URL that you want to redirect the person logging in back to.
            Note: Your redirect uri need be set to `Valid OAuth redirect URIs` items in App Dashboard.
        :param scope: A list of permission string to request from the person using your app.
        :param kwargs: Additional parameters for oauth.
        :return: URL to do oauth and state
        """
        session = self._get_oauth_session(
            redirect_uri=redirect_uri, scope=scope, **kwargs
        )
        authorization_url, state = session.authorization_url(url=self.AUTHORIZATION_URL)
        return authorization_url, state

    def exchange_user_access_token(
        self, response: str, redirect_uri: Optional[str] = None
    ) -> dict:
        """
        :param response: The redirect response url for authorize redirect
        :param redirect_uri: Url for your redirect.
        :return:
        """
        session = self._get_oauth_session(redirect_uri=redirect_uri)

        session.fetch_token(
            self.EXCHANGE_ACCESS_TOKEN_URL,
            client_secret=self.app_secret,
            authorization_response=response,
        )
        self.access_token = session.access_token

        return session.token

    def exchange_page_access_token(
        self, page_id: str, access_token: Optional[str] = None
    ) -> str:
        """
        Get page access token by page administrator's user access token.

        Refer:
            1. https://developers.facebook.com/docs/pages/access-tokens
            2. https://developers.facebook.com/docs/facebook-login/access-tokens

        :param page_id: ID for page.
        :param access_token: Access token for user.
        :return: Page access token
        """
        if access_token is None:
            access_token = self.access_token

        resp = self._request(
            url=f"{self.version}/{page_id}",
            args={"fields": "access_token", "access_token": access_token},
            auth_need=False,
        )

        data = self._parse_response(resp)
        if "access_token" not in data:
            raise LibraryError(
                {
                    "message": "Can not get page access token. Reason maybe: \n"
                    "1. Your user access token has `page_show_list` or `manage_pages` permission.\n"
                    "2. You have the target page's manage permission."
                }
            )
        return data["access_token"]

    def exchange_long_lived_user_access_token(self, access_token=None) -> dict:
        """
        Generate long-lived token by short-lived token, Long-lived token generally lasts about 60 days.

        :param access_token: Short-lived user access token
        :return: Long-lived user access token info.
        """
        if access_token is None:
            access_token = self.access_token
        args = {
            "grant_type": "fb_exchange_token",
            "client_id": self.app_id,
            "client_secret": self.app_secret,
            "fb_exchange_token": access_token,
        }

        resp = self._request(
            url=f"{self.version}/oauth/access_token",
            args=args,
            auth_need=False,
        )
        data = self._parse_response(resp)
        return data

    def exchange_long_lived_page_access_token(
        self, user_id: str, access_token: Optional[str] = None
    ) -> dict:
        """
        Generate long-lived page access token by long-lived user access token.

        :param user_id: ID for the token user.
        :param access_token: Long-lived user token.
        :return: Data for Long-lived page token
        """

        data = self.get_connection(
            object_id=user_id,
            connection="accounts",
            access_token=access_token,
        )
        return data

    def get_app_token(
        self, app_id: Optional[str] = None, app_secret: Optional[str] = None
    ) -> dict:
        """
        Generate
        :param app_id: ID for app
        :param app_secret:  Secret for app
        :return: app access token
        """
        if app_id is None:
            app_id = self.app_id
        if app_secret is None:
            app_secret = self.app_secret

        resp = self._request(
            url=f"{self.version}/oauth/access_token",
            args={
                "grant_type": "client_credentials",
                "client_id": app_id,
                "client_secret": app_secret,
            },
            auth_need=False,
        )
        data = self._parse_response(resp)
        return data

    def debug_token(self, input_token: str, access_token: Optional[str] = None) -> dict:
        """
        Get input token info by issued app administrator's access token
        :param input_token: Access token to debug.
        :param access_token:
        :return: Issued app administrator's access token
        """
        if access_token is None:
            access_token = self.access_token

        resp = self._request(
            url=f"{self.version}/debug_token",
            args={"input_token": input_token, "access_token": access_token},
            auth_need=False,
        )
        data = self._parse_response(resp)
        return data


class BasicDisplayAPI(GraphAPI):
    GRAPH_URL = "https://graph.instagram.com/"
    AUTHORIZATION_URL = "https://api.instagram.com/oauth/authorize"
    EXCHANGE_ACCESS_TOKEN_URL = "https://api.instagram.com/oauth/access_token"

    DEFAULT_SCOPE = ["user_profile", "user_media"]

    def __init__(
        self,
        app_id: Optional[str] = None,
        app_secret: Optional[str] = None,
        access_token: Optional[str] = None,
        oauth_flow: bool = False,
        version: Optional[str] = None,
        sleep_on_rate_limit: bool = True,
        sleep_seconds_mapping: Optional[Dict[int, int]] = None,
        timeout: Optional[int] = None,
        proxies: Optional[dict] = None,
    ):
        super().__init__(
            app_id=app_id,
            app_secret=app_secret,
            access_token=access_token,
            oauth_flow=oauth_flow,
            version=version,
            sleep_on_rate_limit=sleep_on_rate_limit,
            sleep_seconds_mapping=sleep_seconds_mapping,
            timeout=timeout,
            proxies=proxies,
        )

    @staticmethod
    def _generate_secret_proof(
        access_token: str, secret: Optional[str] = None
    ) -> Optional[str]:
        """
        :param access_token: Access token
        :param secret: App secret
        :return:
        """
        return None

    def exchange_user_access_token(
        self, response: str, redirect_uri: Optional[str] = None
    ) -> dict:
        """
        :param response: The redirect response url for authorize redirect
        :param redirect_uri: Url for your redirect.
        :return:
        """
        session = self._get_oauth_session(redirect_uri=redirect_uri)

        session.fetch_token(
            self.EXCHANGE_ACCESS_TOKEN_URL,
            client_secret=self.app_secret,
            authorization_response=response,
            include_client_id=True,
        )
        self.access_token = session.access_token

        return session.token

    def exchange_long_lived_user_access_token(self, access_token=None) -> dict:
        """
        Exchange short-lived Instagram User Access Tokens for long-lived Instagram User Access Tokens.
        :param access_token: short-lived user token.
        :return: Long-lived user access token info.
        """
        if access_token is None:
            access_token = self.access_token

        args = {
            "grant_type": "ig_exchange_token",
            "client_secret": self.app_secret,
            "access_token": access_token,
        }
        resp = self._request(
            url=f"access_token",
            args=args,
            auth_need=False,
        )
        data = self._parse_response(resp)
        return data

    def refresh_access_token(self, access_token: str):
        """
        :param access_token: The valid (unexpired) long-lived Instagram User Access Token that you want to refresh.
        :return: New access token.
        """
        args = {"grant_type": "ig_refresh_token", "access_token": access_token}
        resp = self._request(
            url="refresh_access_token",
            args=args,
        )
        data = self._parse_response(resp)
        return data

    def exchange_page_access_token(
        self, page_id: str, access_token: Optional[str] = None
    ) -> str:
        raise LibraryError({"message": "Method not support"})

    def exchange_long_lived_page_access_token(
        self, user_id: str, access_token: Optional[str] = None
    ) -> dict:
        raise LibraryError({"message": "Method not support"})

    def get_app_token(
        self, app_id: Optional[str] = None, app_secret: Optional[str] = None
    ) -> dict:
        raise LibraryError({"message": "Method not support"})

    def debug_token(self, input_token: str, access_token: Optional[str] = None) -> dict:
        raise LibraryError({"message": "Method not support"})
