"""
    Comments edge for resource.
"""

from typing import Optional, Union

import pyfacebook.utils.constant as const
from pyfacebook.models.comment import CommentsResponse
from pyfacebook.utils.params_utils import enf_comma_separated


class CommentsEdge:

    __slots__ = ()

    def get_comments(
        self,
        object_id: str,
        fields: Optional[Union[str, list, dict]] = None,
        filter_type: Optional[str] = None,
        summary: Optional[bool] = None,
        since: Optional[str] = None,
        until: Optional[str] = None,
        count: Optional[int] = 10,
        limit: Optional[int] = 10,
        return_json: bool = False,
        **kwargs,
    ) -> Union[CommentsResponse, dict]:
        """
        Get lists of comments on a Facebook object.

        :param object_id: ID for the facebook object.
        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param filter_type: This determines which comments are returned when comment replies are available.
            It can be either:
                - toplevel : Default, return all top-level comments
                - stream : All-level comments in chronological order.
        :param summary: Is return the aggregated information about the edge,
        :param since: A Unix timestamp or strtotime data value that points to the start of data.
        :param until: A Unix timestamp or strtotime data value that points to the end of data.
        :param count: The total count for you to get data.
        :param limit: Each request retrieve objects count.
            It should no more than 100. Default is None will use api default limit.
        :param return_json: Set to false will return a dataclass for Comment.
            Or return json data. Default is false.
        :param kwargs: Additional parameters for different object.
        :return: Comments response information
        """

        if fields is None:
            fields = const.COMMENT_PUBLIC_FIELDS

        data = self.client.get_full_connections(
            object_id=object_id,
            connection="comments",
            count=count,
            limit=limit,
            fields=enf_comma_separated(field="fields", value=fields),
            since=since,
            until=until,
            filter=filter_type,
            **kwargs,
        )

        if return_json:
            return data
        else:
            return CommentsResponse.new_from_json_dict(data)
