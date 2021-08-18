"""
    Feed connections for resource.
"""

from typing import List, Optional, Tuple, Union

import pyfacebook.utils.constant as const
from pyfacebook.models.post import Post
from pyfacebook.utils.params_utils import enf_comma_separated


class FeedMixin:
    """
    Base resource for object with feed
    """

    __slots__ = ()

    def _get_feed(
        self,
        object_id: str,
        fields: Optional[Union[str, list, dict]] = None,
        since: Optional[str] = None,
        until: Optional[str] = None,
        count: Optional[int] = 10,
        limit: Optional[int] = 10,
        source: Optional[str] = "feed",
        return_json: bool = False,
        **kwargs,
    ) -> Tuple[List[Union[Post, dict]], dict]:
        """
        Get feed of a Facebook object.

        :param object_id: ID for object to get feeds.
        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param since: A Unix timestamp or strtotime data value that points to the start of data.
        :param until: A Unix timestamp or strtotime data value that points to the end of data.
        :param count: The total count for you to get data.
        :param limit: Each request retrieve objects count.
            It should no more than 100. Default is None will use api default limit.
        :param source: Resource type. Valid values maybe feed/posts/tagged/published_posts depend on object type.
        :param return_json: Set to false will return a dataclass for post.
            Or return json data. Default is false.
        :param kwargs: Additional parameters for different object.
        :return: Posts information and paging
        """

        if fields is None:
            fields = const.POST_PUBLIC_FIELDS + const.POST_CONNECTIONS_SUMMERY_FIELDS

        feeds, paging = self.client.get_full_connections(
            object_id=object_id,
            connection=source,
            count=count,
            limit=limit,
            fields=enf_comma_separated(field="fields", value=fields),
            since=since,
            until=until,
            **kwargs,
        )
        if return_json:
            return feeds, paging
        else:
            return [Post.new_from_json_dict(fd) for fd in feeds], paging

    def get_feed(
        self,
        object_id: str,
        fields: Optional[Union[str, list, dict]] = None,
        since: Optional[str] = None,
        until: Optional[str] = None,
        count: Optional[int] = 10,
        limit: Optional[int] = 10,
        return_json: bool = False,
        **kwargs,
    ) -> Tuple[List[Union[Post, dict]], dict]:
        """
        Get feed of a Facebook Page including posts and links published by this Page, or by visitors to this Page.

        :param object_id: ID for page to get feeds.
        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param since: A Unix timestamp or strtotime data value that points to the start of data.
        :param until: A Unix timestamp or strtotime data value that points to the end of data.
        :param count: The total count for you to get data.
        :param limit: Each request retrieve objects count.
            It should no more than 100. Default is None will use api default limit.
        :param return_json: Set to false will return a dataclass for post.
            Or return json data. Default is false.
        :param kwargs: Additional parameters for different object.
        :return: Posts information and paging
        """
        return self._get_feed(
            object_id=object_id,
            fields=fields,
            since=since,
            until=until,
            count=count,
            limit=limit,
            return_json=return_json,
            **kwargs,
        )
