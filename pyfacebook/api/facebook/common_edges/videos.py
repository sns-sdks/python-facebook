"""
    Videos edge for resource.
"""

from typing import Optional, Union

import pyfacebook.utils.constant as const
from pyfacebook.models.video import VideosResponse
from pyfacebook.utils.params_utils import enf_comma_separated


class VideosEdge:
    __slots__ = ()

    def get_videos(
        self,
        object_id: str,
        fields: Optional[Union[str, list, dict]] = None,
        since: Optional[str] = None,
        until: Optional[str] = None,
        count: Optional[int] = 10,
        limit: Optional[int] = 10,
        return_json: bool = False,
        **kwargs,
    ) -> Union[VideosResponse, dict]:
        """
        Get a list of videos on a Facebook object.

        :param object_id: ID for object(page,user,group)
        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param since: A Unix timestamp or strtotime data value that points to the start of data.
        :param until: A Unix timestamp or strtotime data value that points to the end of data.
        :param count: The total count for you to get data.
        :param limit: Each request retrieve objects count.
            It should no more than 100. Default is None will use api default limit.
        :param return_json: Set to false will return a list dataclass for Videos.
            Or return json data. Default is false.
        :param kwargs: Additional parameters for different object.
        :return: Videos response information
        """

        if fields is None:
            fields = const.VIDEO_PUBLIC_FIELDS

        data = self.client.get_full_connections(
            object_id=object_id,
            connection="videos",
            count=count,
            limit=limit,
            fields=enf_comma_separated(field="fields", value=fields),
            since=since,
            until=until,
            **kwargs,
        )

        if return_json:
            return data
        else:
            return VideosResponse.new_from_json_dict(data)
