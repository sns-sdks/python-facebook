"""
    Base
"""
from typing import List, Optional, Union, Tuple

import pyfacebook.utils.constant as const
from pyfacebook.api.graph import GraphAPI
from pyfacebook.models.post import Post
from pyfacebook.utils.params_utils import enf_comma_separated


class BaseResource:
    """Facebook Resource base class"""

    def __init__(self, client=None):
        self._client: GraphAPI = client

    @property
    def access_token(self):
        return self._client.access_token

    @property
    def app_id(self):
        return self._client.app_id

    @property
    def app_secret(self):
        return self._client.app_secret

    @property
    def client(self):
        return self._client


class BaseFeedResource(BaseResource):
    """
    Base resource for object with feed
    """

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
        )
        if return_json:
            return feeds, paging
        else:
            return [Post.new_from_json_dict(fd) for fd in feeds], paging
