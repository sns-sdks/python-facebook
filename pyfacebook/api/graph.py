"""
    Base Graph API impl
"""
import hashlib
import hmac
import logging
import re
import time
from typing import Dict, List, Optional, Tuple

import requests
from requests import Response

from pyfacebook.ratelimit import RateLimit, PercentSecond


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
        debug: bool = False,
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
                    raise Exception(
                        f"Valid API version are {','.join(self.VALID_API_VERSIONS)}"
                    )
                else:
                    self.version = version
            else:
                raise Exception(
                    f"Version string {version} is invalid. You can provide with like: 5.0 or v5.0"
                )

        # Token
        if access_token:
            self._access_token = access_token
        elif application_only_auth and all([self.app_id, self.app_secret]):
            pass
        elif oauth_flow and all([self.app_id, self.app_secret]):
            pass
        else:
            raise Exception("Need access token")

    @staticmethod
    def _build_sleep_seconds_resource(
        sleep_seconds_mapping: Dict[int, int]
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
            logging.debug(
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
            args["access_token"] = self._access_token
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
            raise Exception(ex.args)

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
            raise Exception("Wrong response")

    @staticmethod
    def _check_graph_error(data: dict):
        """
        :param data: Data from response
        """
        if "error" in data:
            error_data = data["error"]
            raise Exception(error_data)

    def get_object(self, object_id: str, fields: str, **kwargs) -> dict:
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

    def get_objects(self, ids: str, fields: str, **kwargs) -> dict:
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
    ) -> Tuple[List[dict], Optional[dict]]:
        """
        Get connections objects for object by id. Like get page medias by page id.

        :param object_id: ID for object(user,page,event...).
        :param connection: Connection name for object, Like(posts,comments...).
        :param count: The count will retrieve objects. Default is None will get all data.
        :param limit: Each request retrieve objects count.
            For most connections should no more than 100. Default is None will use api default limit.
        :param kwargs: Additional parameters for different connections.
        :return: Response data and latest paging info.
        """

        if limit is not None:
            kwargs["limit"] = limit

        data_set, paging = [], None
        while True:
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

        return data_set, paging