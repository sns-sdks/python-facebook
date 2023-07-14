"""
    Likes edge for resource.

    Refer: https://developers.facebook.com/docs/graph-api/reference/object/likes
"""

from typing import Optional, Union

import pyfacebook.utils.constant as const
from pyfacebook.models.user import LikesResponse
from pyfacebook.utils.params_utils import enf_comma_separated


class LikesEdge:
    __slots__ = ()

    def get_likes(
        self,
        object_id: str,
        fields: Optional[Union[str, list, dict]] = None,
        limit: Optional[int] = 10,
        return_json: bool = False,
        **kwargs,
    ) -> Union[LikesResponse, dict]:
        """
        Returns the list of people who liked this object.
        When reading likes on a Page or User object, this endpoint returns a list of pages liked by that Page or User.

        :param object_id: ID the facebook object.
        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param limit: Each request retrieve objects count.
            It should no more than 100. Default is None will use api default limit.
        :param return_json: Set to false will return a dataclass for Photo.
            Or return json data. Default is false.
        :param kwargs: Additional parameters for different object. like pagination.
        :return: Likes response information
        """
        if fields is None:
            fields = const.LIKES_FIELDS

        data = self.client.get_connection(
            object_id=object_id,
            connection="likes",
            fields=enf_comma_separated(field="fields", value=fields),
            limit=limit,
            **kwargs,
        )
        if return_json:
            return data
        else:
            return LikesResponse.new_from_json_dict(data)

    def creat_like(self, object_id: str) -> dict:
        """
        Like an object.

        :param object_id: ID the facebook object.
        :return: status for the operation.
        """
        data = self.client.post_object(
            object_id=object_id,
            connection="likes",
        )
        return data

    def delete_like(self, object_id: str) -> dict:
        """
        Delete likes on object using this endpoint.

        :param object_id: ID the facebook object.
        :return: status for the operation.
        """
        data = self.client.delete_object(
            object_id=object_id,
            connection="likes",
        )
        return data
