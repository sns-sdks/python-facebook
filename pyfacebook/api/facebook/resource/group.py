"""
    Apis for group.
"""

from typing import Dict, List, Optional, Tuple, Union

import pyfacebook.utils.constant as const
from pyfacebook.api.facebook.resource.base import BaseFeedResource
from pyfacebook.models.group import Group
from pyfacebook.models.post import Post
from pyfacebook.utils.params_utils import enf_comma_separated


class FacebookGroup(BaseFeedResource):
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

    def get_feed(
        self,
        group_id: str,
        fields: Optional[Union[str, list, dict]] = None,
        since: Optional[str] = None,
        until: Optional[str] = None,
        count: Optional[int] = 10,
        limit: Optional[int] = 10,
        return_json: bool = False,
    ) -> Tuple[List[Union[Post, dict]], dict]:
        """
        Get Feed of Posts owned by the Group.

        :param group_id: ID for the group to get feeds.
        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param since: A Unix timestamp or strtotime data value that points to the start of data.
        :param until: A Unix timestamp or strtotime data value that points to the end of data.
        :param count: The total count for you to get data.
        :param limit: Each request retrieve objects count.
            It should no more than 100. Default is None will use api default limit.
        :param return_json: Set to false will return a dataclass for post.
            Or return json data. Default is false.
        :return: Posts information and paging
        """

        return self._get_feed(
            object_id=group_id,
            fields=fields,
            since=since,
            until=until,
            count=count,
            limit=limit,
            return_json=return_json,
        )
