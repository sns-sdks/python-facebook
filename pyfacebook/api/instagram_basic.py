"""
    Instagram Basic display Api impl
"""
from typing import Dict, Optional, Union, List, Tuple, Set

from pyfacebook.api.base import BaseApi
from pyfacebook.error import PyFacebookException, ErrorCode, ErrorMessage
from pyfacebook.models import AuthAccessToken, IgBasicUser, IgBasicMedia, IgBasicMediaChildren
from pyfacebook.utils import constant
from pyfacebook.utils.param_validation import enf_comma_separated


class IgBasicApi(BaseApi):
    GRAPH_URL = "https://graph.instagram.com/"
    DEFAULT_AUTHORIZATION_URL = "https://api.instagram.com/oauth/authorize"
    DEFAULT_EXCHANGE_ACCESS_TOKEN_URL = "https://api.instagram.com/oauth/access_token"

    DEFAULT_SCOPE = ["user_profile", "user_media"]

    def __init__(self,
                 app_id=None,
                 app_secret=None,
                 short_token=None,
                 long_term_token=None,
                 initial_access_token=True,
                 timeout=None,  # type: Optional[int]
                 sleep_on_rate_limit=False,  # type: bool
                 sleep_seconds_mapping=None,  # type: Optional[Dict]
                 proxies=None,  # type: Optional[dict]
                 debug_http=False  # type: bool
                 ):
        BaseApi.__init__(self,
                         app_id=app_id,
                         app_secret=app_secret,
                         short_token=short_token,
                         long_term_token=long_term_token,
                         timeout=timeout,
                         initial_access_token=initial_access_token,
                         sleep_on_rate_limit=sleep_on_rate_limit,
                         sleep_seconds_mapping=sleep_seconds_mapping,
                         proxies=proxies,
                         debug_http=debug_http
                         )

    @staticmethod
    def _generate_secret_proof(secret, access_token):  # type: (str, str) -> Optional[str]
        return None

    def get_app_token(self, return_json=False):
        raise PyFacebookException(ErrorMessage(
            code=ErrorCode.NOT_SUPPORT_METHOD,
            message="Method not support by this api."
        ))

    def get_token_info(self, input_token=None, return_json=False):
        raise PyFacebookException(ErrorMessage(
            code=ErrorCode.NOT_SUPPORT_METHOD,
            message="Method not support by this api."
        ))

    def exchange_insights_token(self, page_id, access_token=None):
        raise PyFacebookException(ErrorMessage(
            code=ErrorCode.NOT_SUPPORT_METHOD,
            message="Method not support by this api."
        ))

    def get_long_token(self, short_token, app_id=None, app_secret=None, return_json=False):
        # type: (str, Optional[str], Optional[str], bool) -> Optional[Union[AuthAccessToken, Dict]]
        """
        Exchange a short-lived Instagram User Access Token for a long-lived Instagram User Access Token.

        :param short_token: short-lived Instagram User Access Token.
        :param app_id: Your Instagram app's id, this not necessary.
        :param app_secret: Your Instagram app's secret.
        :param return_json: Set to false will return instance of AuthAccessToken.
        Or return json data. Default is false.
        :return: Access token data.
        """
        if app_secret is None:
            app_secret = self.app_secret

        resp = self._request(
            path="access_token",
            args={
                "grant_type": "ig_exchange_token",
                "client_secret": app_secret,
                "access_token": short_token,
            },
            enforce_auth=False
        )
        data = self._parse_response(resp)

        if return_json:
            return data
        else:
            return AuthAccessToken.new_from_json_dict(data)

    def refresh_access_token(self, access_token=None, return_json=False):
        # type: (Optional[str], bool) -> Optional[Union[AuthAccessToken, Dict]]
        """
        :param access_token: long-lived token will be refreshed.
        :param return_json: Set to false will return instance of AuthAccessToken.
        Or return json data. Default is false.
        :return: New long-lived access token data
        """
        if access_token is None:
            access_token = self._access_token

        resp = self._request(
            path="refresh_access_token",
            args={
                "grant_type": "ig_refresh_token",
                "access_token": access_token
            }
        )
        data = self._parse_response(resp)

        if return_json:
            return data
        else:
            return AuthAccessToken.new_from_json_dict(data)

    def get_user_info(self, user_id=None, fields=None, return_json=False):
        # type: (str, Optional[Union[str, List, Tuple, Set]], bool) -> Union[IgBasicUser, Dict]
        """
        Retrieve user basic info for target user.
        :param user_id: The id for you want to get data. If not provide, will use access token belong user
        :param fields: Comma-separated id string for data fields which you want.
                You can also pass this with an id list, tuple, set.
        :param return_json: Set to false will return a list instance of IgBasicUser.
                Or return json data. Default is false.
        :return: User info data
        """

        if user_id is None:
            user_id = "me"

        if fields is None:
            fields = constant.INSTAGRAM_BASIC_USER_FIELD

        args = {
            "fields": enf_comma_separated(field="fields", value=fields)
        }

        resp = self._request(
            path="{}".format(user_id),
            args=args
        )
        data = self._parse_response(resp)

        if return_json:
            return data
        else:
            return IgBasicUser.new_from_json_dict(data)

    def paged_by_cursor(self,
                        target,  # type: str
                        resource,  # type: str
                        args,  # type: Dict
                        next_cursor=None  # type: Optional[str]
                        ):
        # type: (...) -> (Optional[str], Optional[str], Dict)
        """
        Paging data by cursor.

        :param target: Id for target object
        :param resource: resource type string.
        :param args: args dict.
        :param next_cursor: The paging cursor str. It will return from the api.
        :return: next cursor, previous cursor, data list
        """

        if next_cursor is not None:
            args["after"] = next_cursor

        resp = self._request(
            path="{0}/{1}".format(target, resource),
            args=args
        )

        next_cursor, previous_cursor = None, None
        data = self._parse_response(resp)

        if "paging" in data:
            paging = data["paging"]
            if "next" in paging:
                cursors = paging.get("cursors", {})
                next_cursor = cursors.get('after')
                previous_cursor = cursors.get('before')
        return next_cursor, previous_cursor, data

    def get_user_medias(self,
                        user_id=None,  # type: str
                        fields=None,  # type: Optional[Union[str, List, Tuple, Set]]
                        count=25,  # type: Optional[int]
                        limit=25,  # type: int
                        return_json=False,  # type: bool
                        ):
        # type: (...) -> List[Union[IgBasicMedia, Dict]]
        """
        Retrieve target user's medias.

        :param user_id: The id for you want to get data. If not provide, will use access token belong user.
        :param fields: Comma-separated id string for data fields which you want.
                You can also pass this with an id list, tuple, set.
        :param count: The count is you want to retrieve medias. Default is 25.
                If you want to get all data. Set it to None.
        :param limit: Each request retrieve posts count from api.
                For medias it may no more than 100. (Not verified.)
        :param return_json: Set to false will return a list instance of IgBasicMedia.
                Or return json data. Default is false.
        :return: Media data list
        """

        if user_id is None:
            user_id = "me"

        if fields is None:
            fields = constant.INSTAGRAM_BASIC_MEDIA_FIELD

        if count is not None:
            limit = min(count, limit)

        args = {
            "fields": enf_comma_separated(field="fields", value=fields),
            "limit": limit,
        }

        medias = []
        next_cursor = None

        while True:
            next_cursor, previous_cursor, data = self.paged_by_cursor(
                target=user_id,
                resource="media",
                args=args,
                next_cursor=next_cursor
            )
            data = data.get("data", [])

            if return_json:
                medias += data
            else:
                medias += [IgBasicMedia.new_from_json_dict(item) for item in data]

            if count is not None:
                if len(medias) >= count:
                    medias = medias[:count]
                    break
            if next_cursor is None:
                break

        return medias

    def get_media_info(self,
                       media_id,  # type: str
                       fields=None,  # type: Optional[Union[str, List, Tuple, Set]]
                       return_json=False,  # type: bool
                       ):
        # type: (...) -> Union[IgBasicMedia, Dict]
        """
        Retrieve media info for target media id.

        :param media_id: The id for target media id.
        :param fields: Comma-separated id string for data fields which you want.
                You can also pass this with an id list, tuple, set.
        :param return_json: Set to false will return an instance of IgBasicMedia.
                Or return json data. Default is false.
        :return: media data info.
        """

        if fields is None:
            fields = constant.INSTAGRAM_BASIC_MEDIA_FIELD

        args = {
            "fields": enf_comma_separated(field="fields", value=fields),
        }

        resp = self._request(
            path="{}".format(media_id),
            args=args
        )
        data = self._parse_response(resp)

        if return_json:
            return data
        else:
            return IgBasicMedia.new_from_json_dict(data)

    def get_media_children(self,
                           media_id,  # type: str
                           fields=None,  # type: Optional[Union[str, List, Tuple, Set]]
                           return_json=False,  # type: bool
                           ):
        # type: (...) -> List[Union[IgBasicMediaChildren, Dict]]
        """
        Retrieve media children data for target media.
        :param media_id: The id for target media.
        :param fields: Comma-separated id string for data fields which you want.
                You can also pass this with an id list, tuple, set.
        :param return_json: Set to false will return a list of instance of IgBasicMediaChildren.
                Or return json data. Default is false.
        :return: media children list
        """

        if fields is None:
            fields = constant.INSTAGRAM_BASIC_MEDIA_CHILDREN_FIELD

        args = {
            "fields": enf_comma_separated(field="fields", value=fields),
        }

        resp = self._request(
            path="{}/children".format(media_id),
            args=args
        )
        data = self._parse_response(resp)

        if return_json:
            return data["data"]
        else:
            return [IgBasicMediaChildren.new_from_json_dict(item) for item in data["data"]]
