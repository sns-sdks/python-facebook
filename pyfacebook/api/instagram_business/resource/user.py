"""
    Apis for user.
"""

from typing import Optional, Union

import pyfacebook.utils.constant as const
from pyfacebook.api.base_resource import BaseResource
from pyfacebook.models.ig_business_models import (
    IgBusUser,
    IgBusMediaResponse,
    IgBusPublishLimit,
)
from pyfacebook.utils.params_utils import enf_comma_separated


class IGBusinessUser(BaseResource):
    def get_info(
        self,
        fields: Optional[Union[str, list, tuple]] = None,
        return_json: bool = False,
    ) -> Union[IgBusUser, dict]:
        """
        Get information about an Instagram Business Account or an Instagram Creator Account.

        Note:

            Now this can only get user info by user's access token.

        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param return_json: Set to false will return a dataclass for Account.
            Or return json data. Default is false.
        :return: IG Business User information.
        """
        if fields is None:
            fields = const.IG_BUSINESS_USER_PUBLIC_FIELDS

        data = self.client.get_object(
            object_id=self.client.instagram_business_id,
            fields=enf_comma_separated(field="fields", value=fields),
        )
        if return_json:
            return data
        else:
            return IgBusUser.new_from_json_dict(data=data)

    def discovery_user(
        self,
        username: str,
        fields: Optional[Union[str, list, tuple]] = None,
        return_json: bool = False,
    ) -> Union[IgBusUser, dict]:
        """
        Get other business account info by username.

        :param username: Username to get data.
        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param return_json: Set to false will return a dataclass for IgBusUser.
            Or return json data. Default is false.
        :return: IG Business User information.
        """

        if fields is None:
            fields = const.IG_BUSINESS_USER_PUBLIC_FIELDS

        metric = enf_comma_separated(field="fields", value=fields)

        data = self.client.get_object(
            object_id=self.client.instagram_business_id,
            fields=f"business_discovery.username({username}){{{metric}}}",
        )
        if return_json:
            return data["business_discovery"]
        else:
            return IgBusUser.new_from_json_dict(data=data["business_discovery"])

    def discovery_user_medias(
        self,
        username: str,
        fields: Optional[Union[str, list, tuple]] = None,
        limit: Optional[int] = None,
        after: Optional[str] = None,
        before: Optional[str] = None,
        return_json: bool = False,
    ) -> Union[IgBusMediaResponse, dict]:
        """
        Get other business account's media by username.

        :param username: Username to get data.
        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param limit: Each request retrieve objects count.
            It should no more than 100. Default is None will use api default limit.
        :param after: The cursor that points to the end of the page of data that has been returned.
        :param before: The cursor that points to the start of the page of data that has been returned.
        :param return_json: Set to false will return a dataclass for IgBusMediaResponse.
            Or return json data. Default is false.
        :return: Media response information.
        """

        if fields is None:
            fields = const.IG_BUSINESS_MEDIA_PUBLIC_FIELDS
        metric = enf_comma_separated(field="fields", value=fields)

        limit_str, after_str, before_str = "", "", ""
        if limit is not None:
            limit_str = f".limit({limit})"

        if after is not None:
            after_str = f".after({after})"

        if before is not None:
            before_str = f".before({before})"

        data = self.client.get_object(
            object_id=self.client.instagram_business_id,
            fields=f"business_discovery.username({username}){{media{after_str}{before_str}{limit_str}{{{metric}}}}}",
        )

        media = data["business_discovery"]["media"]
        if return_json:
            return media
        else:
            return IgBusMediaResponse.new_from_json_dict(media)

    def get_content_publishing_limit(
        self,
        fields: Optional[Union[str, list, tuple]] = None,
        return_json: bool = False,
    ) -> Union[IgBusPublishLimit, dict]:
        """
        Get user's current content publishing usage.

        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param return_json: Set to false will return a dataclass for PublishLimit.
            Or return json data. Default is false.
        :return: IG Business content publish limit information.
        """

        if fields is None:
            fields = const.IG_BUSINESS_CONTENT_PUBLISH_LIMIT_FIELDS

        data = self.client.get_connection(
            object_id=self.client.instagram_business_id,
            connection="content_publishing_limit",
            fields=enf_comma_separated(field="fields", value=fields),
        )
        if return_json:
            return data["data"][0]
        else:
            return IgBusPublishLimit.new_from_json_dict(data["data"][0])
