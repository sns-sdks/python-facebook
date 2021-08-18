"""
    Videos connections for resource.
"""

from typing import List, Optional, Union, Tuple

import pyfacebook.utils.constant as const
from pyfacebook.models.video import Video
from pyfacebook.models.extensions import Paging
from pyfacebook.utils.params_utils import enf_comma_separated


class VideosMixin:
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
    ) -> Tuple[List[Union[Video, dict]], Union[Paging, dict]]:
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
        :return: Videos information and paging
        """

        if fields is None:
            fields = const.VIDEO_PUBLIC_FIELDS

        videos, paging = self.client.get_full_connections(
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
            return videos, paging
        else:
            return [
                Video.new_from_json_dict(v) for v in videos
            ], Paging.new_from_json_dict(paging)
