"""
    Apis for User.
"""
from typing import Dict, Optional, Union

import pyfacebook.utils.constant as const
from pyfacebook.api.base_resource import BaseResource
from pyfacebook.api.facebook.common_edges import (
    FeedEdge,
    AlbumsEdge,
    PhotosEdge,
    VideosEdge,
    LiveVideosEdge,
)
from pyfacebook.models.user import User
from pyfacebook.models.page import PagesResponse
from pyfacebook.models.post import FeedResponse
from pyfacebook.models.business import BusinessResponse
from pyfacebook.utils.params_utils import enf_comma_separated


class FacebookUser(
    BaseResource, FeedEdge, AlbumsEdge, PhotosEdge, VideosEdge, LiveVideosEdge
):
    def get_info(
        self,
        user_id: str,
        fields: Optional[Union[str, list, tuple]] = None,
        return_json: bool = False,
    ) -> Union[User, dict]:
        """
        Get information about a Facebook User.

        :param user_id: ID for user.
        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param return_json: Set to false will return a dataclass for user.
        Or return json data. Default is false.
        :return: User information.
        """
        if fields is None:
            fields = const.USER_PUBLIC_FIELDS

        data = self.client.get_object(
            object_id=user_id,
            fields=enf_comma_separated(field="fields", value=fields),
        )
        if return_json:
            return data
        else:
            return User.new_from_json_dict(data=data)

    def get_batch(
        self,
        ids: Optional[Union[str, list, tuple]],
        fields: Optional[Union[str, list, tuple]] = None,
        return_json: bool = False,
    ) -> Union[Dict[str, User], dict]:
        """
        Get batch users information by ids

        :param ids: IDs for the users.
        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param return_json: Set to false will return a dataclass for user.
            Or return json data. Default is false.
        :return: Users information.
        """
        ids = enf_comma_separated(field="ids", value=ids)

        if fields is None:
            fields = const.USER_PUBLIC_FIELDS

        data = self.client.get_objects(
            ids=ids, fields=enf_comma_separated(field="fields", value=fields)
        )
        if return_json:
            return data
        else:
            return {
                user_id: User.new_from_json_dict(item) for user_id, item in data.items()
            }

    def get_accounts(
        self,
        user_id: str,
        fields: Optional[Union[str, list, tuple]] = None,
        is_place: Optional[bool] = None,
        is_promotable: Optional[bool] = None,
        summary: Optional[bool] = None,
        count: Optional[int] = 10,
        limit: Optional[int] = 10,
        return_json: bool = False,
    ) -> Union[PagesResponse, dict]:
        """
        Get the Facebook Pages that a person owns or is able to perform tasks on.

        :param user_id: ID for the user.
        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param is_place: If specified,filter pages based on whetherthey are places or not.
        :param is_promotable: If specified, filter pages based on whether they can be promoted or not.
        :param summary: Whether aggregated information about the edge, such as counts.
        :param count: The total count for you to get data.
        :param limit: Each request retrieve objects count.
            It should no more than 100. Default is None will use api default limit.
        :param return_json: Set to false will return a dataclass for Page.
            Or return json data. Default is false.
        :return: Pages information and paging
        """
        if fields is None:
            fields = const.PAGE_PUBLIC_FIELDS

        data = self.client.get_full_connections(
            object_id=user_id,
            connection="accounts",
            count=count,
            limit=limit,
            fields=enf_comma_separated(field="fields", value=fields),
            is_place=is_place,
            is_promotable=is_promotable,
            summary=summary,
        )
        if return_json:
            return data
        else:
            return PagesResponse.new_from_json_dict(data)

    def get_posts(
        self,
        object_id: str,
        fields: Optional[Union[str, list, dict]] = None,
        since: Optional[str] = None,
        until: Optional[str] = None,
        count: Optional[int] = 10,
        limit: Optional[int] = 10,
        return_json: bool = False,
    ) -> Union[FeedResponse, dict]:
        """
        Get the posts published by the person themselves.

        :param object_id: ID for the user.
        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param since: A Unix timestamp or strtotime data value that points to the start of data.
        :param until: A Unix timestamp or strtotime data value that points to the end of data.
        :param count: The total count for you to get data.
        :param limit: Each request retrieve objects count.
            It should no more than 100. Default is None will use api default limit.
        :param return_json: Set to false will return a dataclass for post.
            Or return json data. Default is false.
        :return: Posts information and paging
        """
        return self._get_feed(
            object_id=object_id,
            fields=fields,
            since=since,
            until=until,
            count=count,
            limit=limit,
            source="posts",
            return_json=return_json,
        )

    def get_businesses(
        self,
        user_id: str,
        fields: Optional[Union[str, list, dict]] = None,
        count: Optional[int] = 10,
        limit: Optional[int] = 10,
        return_json: bool = False,
    ) -> Union[BusinessResponse, dict]:
        """
        Get the businesses for the user.

        :param user_id: ID for the user.
        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param count: The total count for you to get data.
        :param limit: Each request retrieve objects count.
            It should no more than 100. Default is None will use api default limit.
        :param return_json: Set to false will return a list of dataclass for Businesses.
            Or return json data. Default is false.
        :return: Response for the user businesses.
        """

        if fields is None:
            fields = const.BUSINESS_PUBLIC_FIELDS

        data = self.client.get_full_connections(
            object_id=user_id,
            connection="businesses",
            count=count,
            limit=limit,
            fields=enf_comma_separated(field="fields", value=fields),
        )
        if return_json:
            return data
        else:
            return BusinessResponse.new_from_json_dict(data)
