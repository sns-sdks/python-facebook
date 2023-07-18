"""
    Apis for comment.
"""

from typing import Dict, Optional, Union

import pyfacebook.utils.constant as const
from pyfacebook.api.base_resource import BaseResource
from pyfacebook.api.facebook.common_edges import LikesEdge
from pyfacebook.models.comment import Comment
from pyfacebook.utils.params_utils import enf_comma_separated


class FacebookComment(BaseResource, LikesEdge):
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

    def create(
        self,
        object_id: str,
        attachment_id: Optional[str] = None,
        attachment_share_url: Optional[str] = None,
        attachment_url: Optional[str] = None,
        files: Optional[dict] = None,
        message: Optional[str] = None,
        fields: Optional[Union[str, list, dict]] = None,
        return_json: bool = False,
        **kwargs,
    ) -> Union[Comment, dict]:
        """
        :param object_id: Object ID to create comment.
        :param attachment_id: An optional ID of an unpublished photo.
        :param attachment_share_url: The URL of a GIF to include as an animated GIF comment
        :param attachment_url: The URL of an image to include as a photo comment.
        :param files: A photo file, encoded as form data, to use as a photo comment.
        :param message: The comment text.
        :param fields: Fields for comment which created.
        :param return_json: Set to false will return a dataclass for Photo.
            Or return json data. Default is false.
        :param kwargs: Additional parameters for different object
        :return: Created comment.
        """
        params = (
            {"fields": enf_comma_separated(field="fields", value=fields)}
            if fields
            else None
        )
        data = {}
        if attachment_id is not None:
            data["attachment_id"] = attachment_id
        elif attachment_share_url is not None:
            data["attachment_share_url"] = attachment_share_url
        elif attachment_url is not None:
            data["attachment_url"] = attachment_url

        if message is not None:
            data["message"] = message

        data = self.client.post_object(
            object_id=object_id,
            connection="comments",
            params=params,
            data=data,
            files=files,
            **kwargs,
        )
        if return_json:
            return data
        else:
            return Comment.new_from_json_dict(data=data)

    def update(
        self,
        comment_id: str,
        attachment_id: Optional[str] = None,
        attachment_share_url: Optional[str] = None,
        attachment_url: Optional[str] = None,
        files: Optional[dict] = None,
        message: Optional[str] = None,
        is_hidden: Optional[bool] = None,
        fields: Optional[Union[str, list, dict]] = None,
        return_json: bool = False,
        **kwargs,
    ) -> Union[Comment, dict]:
        """
        :param comment_id: ID for comment which to update.
        :param attachment_id: An optional ID of an unpublished photo.
        :param attachment_share_url: The URL of a GIF to include as an animated GIF comment
        :param attachment_url: The URL of an image to include as a photo comment.
        :param files: A photo file, encoded as form data, to use as a photo comment.
        :param message: The comment text.
        :param is_hidden: Comment hidden status.
        :param fields: Fields for comment which created.
        :param return_json: Set to false will return a dataclass for Photo.
            Or return json data. Default is false.
        :param kwargs: Additional parameters for different object
        :return:
        """
        # If not point fields to read will return status data.
        if fields:
            params = {"fields": enf_comma_separated(field="fields", value=fields)}
        else:
            params, return_json = None, True

        data = {}
        if attachment_id is not None:
            data["attachment_id"] = attachment_id
        elif attachment_share_url is not None:
            data["attachment_share_url"] = attachment_share_url
        elif attachment_url is not None:
            data["attachment_url"] = attachment_url

        if message is not None:
            data["message"] = message
        if is_hidden is not None:
            data["is_hidden"] = is_hidden

        data = self.client.post_object(
            object_id=comment_id,
            params=params,
            data=data,
            files=files,
            **kwargs,
        )
        if return_json:
            return data
        else:
            return Comment.new_from_json_dict(data=data)

    def delete(self, comment_id: str):
        """
        Delete a comment by using this endpoint

        :param comment_id: ID for the comment.
        :return: status for delete comment.
        """
        data = self.client.delete_object(object_id=comment_id)
        return data
