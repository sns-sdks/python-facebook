"""
    Live videos connection for resource
"""

from typing import List, Optional, Union, Tuple

import pyfacebook.utils.constant as const
from pyfacebook.models.live_video import LiveVideo
from pyfacebook.models.extensions import Paging
from pyfacebook.utils.params_utils import enf_comma_separated


class LiveVideosMixin:
    __slots__ = ()

    def get_live_videos(
        self,
        object_id: str,
        fields: Optional[Union[str, list, dict]] = None,
        since: Optional[str] = None,
        until: Optional[str] = None,
        count: Optional[int] = 10,
        limit: Optional[int] = 10,
        return_json: bool = False,
        **kwargs,
    ) -> Tuple[List[Union[LiveVideo, dict]], Union[Paging, dict]]:
        """
        Get lists of live videos on a facebook object.

        :param object_id: ID for the facebook object.
        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param since: A Unix timestamp or strtotime data value that points to the start of data.
        :param until: A Unix timestamp or strtotime data value that points to the end of data.
        :param count: The total count for you to get data.
        :param limit: Each request retrieve objects count.
            It should no more than 100. Default is None will use api default limit.
        :param return_json: Set to false will return a dataclass for LiveVideo.
            Or return json data. Default is false.
        :param kwargs: Additional parameters for different object.
        :return: live videos information and paging
        """

        if fields is None:
            fields = const.LIVE_VIDEO_PUBLIC_FIELDS

        live_videos, paging = self.client.get_full_connections(
            object_id=object_id,
            connection="live_videos",
            count=count,
            limit=limit,
            fields=enf_comma_separated(field="fields", value=fields),
            since=since,
            until=until,
            **kwargs,
        )
        if return_json:
            return live_videos, paging
        else:
            return [
                LiveVideo.new_from_json_dict(v) for v in live_videos
            ], Paging.new_from_json_dict(paging)
