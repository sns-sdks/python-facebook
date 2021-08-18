"""
    Apis for group.
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
from pyfacebook.models.group import Group
from pyfacebook.utils.params_utils import enf_comma_separated


class FacebookGroup(
    BaseResource, FeedEdge, AlbumsEdge, PhotosEdge, VideosEdge, LiveVideosEdge
):
    def get_info(
        self,
        group_id: str,
        fields: Optional[Union[str, list, tuple]] = None,
        return_json=False,
    ) -> Union[Group, dict]:
        """
        Get information about a Facebook Group.

        :param group_id: ID for the group.
        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param return_json: Set to false will return a dataclass for page.
            Or return json data. Default is false.
        :return: Group information.
        """
        if fields is None:
            fields = const.GROUP_PUBLIC_FIELDS
        data = self.client.get_object(
            object_id=group_id, fields=enf_comma_separated(field="fields", value=fields)
        )
        if return_json:
            return data
        else:
            return Group.new_from_json_dict(data=data)

    def get_batch(
        self,
        ids: Union[str, list, tuple],
        fields: Optional[Union[str, list, tuple]] = None,
        return_json: bool = False,
    ) -> Union[Dict[str, Group], dict]:
        """
        Get batch groups information by ids.

        :param ids: IDs for the groups.
        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param return_json: Set to false will return a dataclass for page.
            Or return json data. Default is false.
        :return: Groups information.
        """

        ids = enf_comma_separated(field="ids", value=ids)

        if fields is None:
            fields = const.GROUP_PUBLIC_FIELDS

        data = self.client.get_objects(
            ids=ids, fields=enf_comma_separated(field="fields", value=fields)
        )
        if return_json:
            return data
        else:
            return {
                gp_id: Group.new_from_json_dict(item) for gp_id, item in data.items()
            }
