"""
    Apis for comment.
"""

from typing import Dict, Optional, Union

import pyfacebook.utils.constant as const
from pyfacebook.api.base_resource import BaseResource
from pyfacebook.models.comment import Comment
from pyfacebook.utils.params_utils import enf_comma_separated


class FacebookComment(BaseResource):
    def get_info(
        self,
        comment_id: Optional[str],
        fields: Optional[Union[str, list, tuple]] = None,
        return_json: bool = False,
    ) -> Union[Comment, dict]:
        """
        Get information about a Facebook Comment.

        :param comment_id: ID for the comment.
        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param return_json: Set to false will return a dataclass for Comment.
            Or return json data. Default is false.
        :return: Comment information.
        """

        if fields is None:
            fields = const.COMMENT_PUBLIC_FIELDS

        data = self.client.get_object(
            object_id=comment_id,
            fields=enf_comma_separated(field="fields", value=fields),
        )
        if return_json:
            return data
        else:
            return Comment.new_from_json_dict(data=data)

    def get_batch(
        self,
        ids: Optional[Union[str, list, tuple]],
        fields: Optional[Union[str, list, tuple]] = None,
        return_json: bool = False,
    ) -> Union[Dict[str, Comment], dict]:
        """
        Get batch comments information by ids.

        :param ids: IDs for the comments.
        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param return_json: Set to false will return a dataclass for Comment.
            Or return json data. Default is false.
        :return: Comments information.
        """

        ids = enf_comma_separated(field="ids", value=ids)

        if fields is None:
            fields = const.COMMENT_PUBLIC_FIELDS

        data = self.client.get_objects(
            ids=ids,
            fields=enf_comma_separated(field="fields", value=fields),
        )
        if return_json:
            return data
        else:
            return {
                comment_id: Comment.new_from_json_dict(item)
                for comment_id, item in data.items()
            }
