"""
    Apis for basic user
"""
from typing import Optional, Union

import pyfacebook.utils.constant as const
from pyfacebook.api.base_resource import BaseResource
from pyfacebook.models.ig_basic_models import IgBasicUser, IgBasicMediaResponse
from pyfacebook.utils.params_utils import enf_comma_separated


class IGBasicUser(BaseResource):
    def get_info(
        self,
        user_id: Optional[str] = "me",
        fields: Optional[Union[str, list, tuple]] = None,
        return_json: bool = False,
    ) -> Union[IgBasicUser, dict]:
        """
        Represents an Instagram user profile.

        :param user_id: ID for the user, matched the access token.
        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param return_json: Set to false will return a dataclass for Account.
            Or return json data. Default is false.
        :return: IG Basic User information.
        """
        if fields is None:
            fields = const.IG_BASIC_USER_FIELDS

        data = self.client.get_object(
            object_id=user_id,
            fields=enf_comma_separated(field="fields", value=fields),
        )
        if return_json:
            return data
        else:
            return IgBasicUser.new_from_json_dict(data=data)

    def get_media(
        self,
        user_id: Optional[str] = "me",
        fields: Optional[Union[str, list, tuple]] = None,
        since: Optional[str] = None,
        until: Optional[str] = None,
        count: Optional[int] = 10,
        limit: Optional[int] = 10,
        return_json=False,
    ) -> Union[IgBasicMediaResponse, dict]:
        """
        Represents a collection of Media on a User. Maximum of 10K of the most recently created media.

        :param user_id: ID for the user, matched the access token.
        :param fields:
        :param since: A Unix timestamp or strtotime data value that points to the start of data.
        :param until: A Unix timestamp or strtotime data value that points to the end of data.
        :param count: The total count for you to get data.
        :param limit: Each request retrieve objects count.
            It should no more than 100. Default is None will use api default limit.
        :param return_json: Set to false will return a dataclass for IgBasicMediaResponse.
            Or return json data. Default is false.
        :return: Media response information.
        """

        if fields is None:
            fields = const.IG_BASIC_MEDIA_FIELDS

        data = self.client.get_full_connections(
            object_id=user_id,
            connection="media",
            count=count,
            limit=limit,
            fields=enf_comma_separated(field="fields", value=fields),
            since=since,
            until=until,
        )
        if return_json:
            return data
        else:
            return IgBasicMediaResponse.new_from_json_dict(data)
