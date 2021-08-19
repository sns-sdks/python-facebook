"""
    Apis for user.
"""

from typing import Optional, Union

import pyfacebook.utils.constant as const
from pyfacebook.api.base_resource import BaseResource
from pyfacebook.models.ig_business_models import (
    IgBusUser,
    IgBusMediaResponse,
    IgBusDiscoveryUserResponse,
    IgBusDiscoveryUserMediaResponse,
    IgBusPublishLimitResponse,
    IgBusInsightsResponse,
    IgBusMentionedCommentResponse,
    IgBusMentionedMediaResponse,
    IgBusHashtagsResponse,
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
    ) -> Union[IgBusDiscoveryUserResponse, dict]:
        """
        Get other business account info by username.

        :param username: Username to get data.
        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param return_json: Set to false will return a dataclass for IgBusDiscoveryUserResponse.
            Or return json data. Default is false.
        :return: Business discovery user response information.
        """

        if fields is None:
            fields = const.IG_BUSINESS_USER_PUBLIC_FIELDS

        metric = enf_comma_separated(field="fields", value=fields)

        data = self.client.get_object(
            object_id=self.client.instagram_business_id,
            fields=f"business_discovery.username({username}){{{metric}}}",
        )
        if return_json:
            return data
        else:
            return IgBusDiscoveryUserResponse.new_from_json_dict(data=data)

    def discovery_user_medias(
        self,
        username: str,
        fields: Optional[Union[str, list, tuple]] = None,
        limit: Optional[int] = None,
        after: Optional[str] = None,
        before: Optional[str] = None,
        return_json: bool = False,
    ) -> Union[IgBusDiscoveryUserMediaResponse, dict]:
        """
        Get other business account's media by username.

        :param username: Username to get data.
        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param limit: Each request retrieve objects count.
            It should no more than 100. Default is None will use api default limit.
        :param after: The cursor that points to the end of the page of data that has been returned.
        :param before: The cursor that points to the start of the page of data that has been returned.
        :param return_json: Set to false will return a dataclass for IgBusDiscoveryUserMediaResponse.
            Or return json data. Default is false.
        :return: Business discovery media response information.
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

        if return_json:
            return data
        else:
            return IgBusDiscoveryUserMediaResponse.new_from_json_dict(data)

    def get_content_publishing_limit(
        self,
        fields: Optional[Union[str, list, tuple]] = None,
        return_json: bool = False,
    ) -> Union[IgBusPublishLimitResponse, dict]:
        """
        Get user's current content publishing usage.

        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param return_json: Set to false will return a dataclass for IgBusPublishLimitResponse.
            Or return json data. Default is false.
        :return: Business content publish limit response information.
        """

        if fields is None:
            fields = const.IG_BUSINESS_CONTENT_PUBLISH_LIMIT_FIELDS

        data = self.client.get_connection(
            object_id=self.client.instagram_business_id,
            connection="content_publishing_limit",
            fields=enf_comma_separated(field="fields", value=fields),
        )
        if return_json:
            return data
        else:
            return IgBusPublishLimitResponse.new_from_json_dict(data)

    def get_insights(
        self,
        metric: Union[str, list, tuple],
        period: str,
        since: Optional[str] = None,
        until: Optional[str] = None,
        user_id: Optional[str] = None,
        access_token: Optional[str] = None,
        return_json: bool = False,
    ) -> Union[IgBusInsightsResponse, dict]:
        """
        Get social interaction metrics on an IG User.

        :param metric: Comma-separated id string for insights metrics which you want.
            You can also pass this with an id list, tuple.
        :param period: Period to aggregation data.
            Accepted parameters: lifetime,day,week,days_28
        :param since: Lower bound of the time range to fetch data. Need Unix timestamps.
        :param until: Upper bound of the time range to fetch data. Need Unix timestamps.
            Notice: time range may not more than 30 days.
        :param user_id: ID for business user to get insights.
        :param access_token: Access token with permissions for user_id.
        :param return_json: Set to false will return a dataclass for Insights.
            Or return json data. Default is false.
        :return: Business user insights response information.
        """

        if user_id is None:
            user_id = self.client.instagram_business_id

        args = {
            "metric": enf_comma_separated(field="metric", value=metric),
            "period": period,
            "since": since,
            "until": until,
        }
        if access_token:
            args["access_token"] = access_token

        data = self.client.get_connection(
            object_id=user_id,
            connection="insights",
            **args,
        )
        if return_json:
            return data
        else:
            return IgBusInsightsResponse.new_from_json_dict(data)

    def get_media(
        self,
        fields: Optional[Union[str, list, tuple]] = None,
        since: Optional[str] = None,
        until: Optional[str] = None,
        count: Optional[int] = 10,
        limit: Optional[int] = 10,
        return_json=False,
    ) -> Union[IgBusMediaResponse, dict]:
        """
        Get user's media. This only can return max 10k medias.

        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param since: A Unix timestamp or strtotime data value that points to the start of data.
        :param until: A Unix timestamp or strtotime data value that points to the end of data.
        :param count: The total count for you to get data.
        :param limit: Each request retrieve objects count.
            It should no more than 100. Default is None will use api default limit.
        :param return_json: Set to false will return a dataclass for IgBusMediaResponse.
            Or return json data. Default is false.
        :return: Media response information.
        """

        if fields is None:
            fields = const.IG_BUSINESS_MEDIA_PUBLIC_FIELDS

        data = self.client.get_full_connections(
            object_id=self.client.instagram_business_id,
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
            return IgBusMediaResponse.new_from_json_dict(data)

    def get_mentioned_comment(
        self,
        comment_id: str,
        fields: Optional[Union[str, list, tuple]] = None,
        return_json=False,
    ) -> Union[IgBusMentionedCommentResponse, dict]:
        """
        Get data on an IG Comment in which user has been @mentioned by another Instagram user

        :param comment_id: ID for comment which the user has been @mentioned.
        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param return_json: Set to false will return a dataclass for IgBusMentionedCommentResponse.
            Or return json data. Default is false.
        :return: Mentioned comment response.
        """

        if fields is None:
            fields = const.IG_BUSINESS_COMMENT_PUBLIC_FIELDS
        fields_inline = enf_comma_separated(field="fields", value=fields)

        data = self.client.get_object(
            object_id=self.client.instagram_business_id,
            fields=f"mentioned_comment.comment_id({comment_id}){{{fields_inline}}}",
        )

        if return_json:
            return data
        else:
            return IgBusMentionedCommentResponse.new_from_json_dict(data)

    def get_mentioned_media(
        self,
        media_id: str,
        fields: Optional[Union[str, list, tuple]] = None,
        return_json=False,
    ) -> Union[IgBusMentionedMediaResponse, dict]:
        """
        Get data on an IG Media in which user has been @mentioned in a caption by another Instagram user.

        :param media_id: ID for media which the user has been @mentioned in a caption
        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param return_json: Set to false will return a dataclass for IgBusMentionedMediaResponse.
            Or return json data. Default is false.
        :return: Mentioned media response.
        """

        if fields is None:
            fields = const.IG_BUSINESS_MENTION_MEDIA_FIELDS
        fields_inline = enf_comma_separated(field="fields", value=fields)

        data = self.client.get_object(
            object_id=self.client.instagram_business_id,
            fields=f"mentioned_media.media_id({media_id}){{{fields_inline}}}",
        )
        if return_json:
            return data
        else:
            return IgBusMentionedMediaResponse.new_from_json_dict(data)

    def get_hashtag_search(
        self,
        q: str,
        return_json=False,
    ) -> Union[IgBusHashtagsResponse, dict]:
        """
        Get ID for hashtag.

        :param q: The hashtag name to query.
        :param return_json: Set to false will return a dataclass for IgBusHashtagsResponse.
            Or return json data. Default is false.
        :return: User stories response information.
        """
        data = self.client.get(
            path="ig_hashtag_search",
            args={
                "fields": "id,name",
                "user_id": self.client.instagram_business_id,
                "q": q,
            },
        )
        if return_json:
            return data
        else:
            return IgBusHashtagsResponse.new_from_json_dict(data)

    def get_recently_searched_hashtags(
        self,
        fields: Optional[Union[str, list, tuple]] = None,
        count: Optional[int] = 25,
        limit: Optional[int] = 25,
        return_json=False,
    ) -> Union[IgBusHashtagsResponse, dict]:
        """
        Get the IG Hashtags that user has searched for within the last 7 days.

        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param count: The total count for you to get data. Maximum is 30.
        :param limit: Each request retrieve objects count. Up to 30.
        :param return_json: Set to false will return a dataclass for IgBusHashtagsResponse.
            Or return json data. Default is false.
        :return: Recently searched hashtags response information.
        """

        if fields is None:
            fields = const.IG_BUSINESS_HASHTAG_PUBLIC_FIELDS

        data = self.client.get_full_connections(
            object_id=self.client.instagram_business_id,
            connection="recently_searched_hashtags",
            fields=enf_comma_separated(field="fields", value=fields),
            count=count,
            limit=limit,
        )
        if return_json:
            return data
        else:
            return IgBusHashtagsResponse.new_from_json_dict(data)

    def get_stories(
        self,
        fields: Optional[Union[str, list, tuple]] = None,
        count: Optional[int] = 10,
        limit: Optional[int] = 10,
        return_json=False,
    ) -> Union[IgBusMediaResponse, dict]:
        """
        Get list of story IG Media objects on user.

        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param count: The total count for you to get data.
        :param limit: Each request retrieve objects count.
            It should no more than 100. Default is None will use api default limit.
        :param return_json: Set to false will return a dataclass for IgBusMediaResponse.
            Or return json data. Default is false.
        :return: User stories response information.
        """

        if fields is None:
            fields = const.IG_BUSINESS_MEDIA_PUBLIC_FIELDS

        data = self.client.get_full_connections(
            object_id=self.client.instagram_business_id,
            connection="stories",
            count=count,
            limit=limit,
            fields=enf_comma_separated(field="fields", value=fields),
        )
        if return_json:
            return data
        else:
            return IgBusMediaResponse.new_from_json_dict(data)

    def get_tagged_media(
        self,
        fields: Optional[Union[str, list, tuple]] = None,
        count: Optional[int] = 25,
        limit: Optional[int] = 25,
        return_json=False,
    ) -> Union[IgBusMediaResponse, dict]:
        """
        Get list of Media objects in which user has been tagged by another Instagram user.

        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param count: The total count for you to get data.
        :param limit: Each request retrieve objects count.
            It should no more than 100. Default is None will use api default limit.
        :param return_json: Set to false will return a dataclass for IgBusMediaResponse.
            Or return json data. Default is false.
        :return: Tagged user medias response information.
        """

        if fields is None:
            fields = const.IG_BUSINESS_MEDIA_PUBLIC_FIELDS

        data = self.client.get_full_connections(
            object_id=self.client.instagram_business_id,
            connection="tags",
            count=count,
            limit=limit,
            fields=enf_comma_separated(field="fields", value=fields),
        )
        if return_json:
            return data
        else:
            return IgBusMediaResponse.new_from_json_dict(data)
