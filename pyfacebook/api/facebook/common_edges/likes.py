"""
    Likes edge for resource.

    Refer: https://developers.facebook.com/docs/graph-api/reference/object/likes
"""

from typing import Optional, Union

import pyfacebook.utils.constant as const
from pyfacebook.models.user import LikesResponse


class LikesEdge:
    __slots__ = ()

    def get_likes(
        self,
        object_id: str,
        fields: Optional[Union[str, list, dict]] = None,
        limit: Optional[int] = 10,
        return_json: bool = True,
        **kwargs,
    ) -> Union[LikesResponse, dict]:
        """"""
        if fields is None:
            fields = const.LIKES_FIELDS

        data = self.client.get_connection(
            object_id=object_id,
            connection="likes",
            limit=limit,
            **kwargs,
        )
        if return_json:
            return data
        else:
            return LikesResponse.new_from_json_dict(data)
