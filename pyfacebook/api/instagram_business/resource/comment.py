"""
    Apis for comment.
"""
from typing import Dict, Optional, Union

import pyfacebook.utils.constant as const
from pyfacebook.api.base_resource import BaseResource
from pyfacebook.models.ig_business_models import IgBusComment, IgBusReply, IgBusReplies
from pyfacebook.utils.params_utils import enf_comma_separated


class IGBusinessComment(BaseResource):
    def get_info(
        self,
        comment_id: str,
        fields: Optional[Union[str, list, tuple]] = None,
        return_json: bool = False,
    ) -> Union[IgBusComment, dict]:
        """
        Get information about a Business comment.

        :param comment_id: ID for Comment.
        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param return_json: Set to false will return a dataclass for IgBusComment.
            Or return json data. Default is false.
        :return: Business comment information.
        """
        if fields is None:
            fields = const.IG_BUSINESS_MEDIA_PUBLIC_FIELDS

        data = self.client.get_object(
            object_id=comment_id,
            fields=enf_comma_separated(field="fields", value=fields),
        )
        if return_json:
            return data
        else:
            return IgBusComment.new_from_json_dict(data=data)

    def get_batch(
        self,
        ids: Optional[Union[str, list, tuple]],
        fields: Optional[Union[str, list, tuple]] = None,
        return_json: bool = False,
    ) -> Union[Dict[str, IgBusComment], dict]:
        """
        Get batch business comment information by ids

        :param ids: IDs for the comments.
        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param return_json: Set to false will return a dict of dataclass for IgBusComment.
            Or return json data. Default is false.
        :return: Business medias information.
        """
        ids = enf_comma_separated(field="ids", value=ids)

        if fields is None:
            fields = const.IG_BUSINESS_COMMENT_PUBLIC_FIELDS

        data = self.client.get_objects(
            ids=ids, fields=enf_comma_separated(field="fields", value=fields)
        )
        if return_json:
            return data
        else:
            return {
                comment_id: IgBusComment.new_from_json_dict(item)
                for comment_id, item in data.items()
            }

    def get_replies(
        self,
        comment_id: str,
        fields: Optional[Union[str, list, tuple]] = None,
        count: Optional[int] = 10,
        limit: Optional[int] = 10,
        return_json: bool = False,
    ) -> Union[IgBusReplies, dict]:
        """
        Getting All Replies (Comments) on a Comment

        :param comment_id: ID for the comment.
        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param count: The total count for you to get data.
        :param limit: Each request retrieve objects count.
            It should no more than 100. Default is None will use api default limit.
        :param return_json: Set to false will return a dataclass for IgBusReplies.
            Or return json data. Default is false.
        :return: Comment replies response information.
        """

        if fields is None:
            fields = const.IG_BUSINESS_REPLY_PUBLIC_FIELDS

        data = self.client.get_full_connections(
            object_id=comment_id,
            connection="replies",
            fields=enf_comma_separated(field="fields", value=fields),
            count=count,
            limit=limit,
        )
        if return_json:
            return data
        else:
            return IgBusReplies.new_from_json_dict(data)


class IGBusinessReply(BaseResource):
    def get_info(
        self,
        reply_id: str,
        fields: Optional[Union[str, list, tuple]] = None,
        return_json: bool = False,
    ) -> Union[IgBusReply, dict]:
        """
        Get information about a Business reply.

        :param reply_id: ID for reply.
        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param return_json: Set to false will return a dataclass for IgBusReply.
            Or return json data. Default is false.
        :return: Business reply information.
        """
        if fields is None:
            fields = const.IG_BUSINESS_REPLY_PUBLIC_FIELDS

        data = self.client.get_object(
            object_id=reply_id,
            fields=enf_comma_separated(field="fields", value=fields),
        )
        if return_json:
            return data
        else:
            return IgBusComment.new_from_json_dict(data=data)

    def get_batch(
        self,
        ids: Optional[Union[str, list, tuple]],
        fields: Optional[Union[str, list, tuple]] = None,
        return_json: bool = False,
    ) -> Union[Dict[str, IgBusReply], dict]:
        """
        Get batch business replies information by ids

        :param ids: IDs for the replies.
        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param return_json: Set to false will return a dict of dataclass for IgBusReply.
            Or return json data. Default is false.
        :return: Business replies information.
        """
        ids = enf_comma_separated(field="ids", value=ids)

        if fields is None:
            fields = const.IG_BUSINESS_REPLY_PUBLIC_FIELDS

        data = self.client.get_objects(
            ids=ids, fields=enf_comma_separated(field="fields", value=fields)
        )
        if return_json:
            return data
        else:
            return {
                reply_id: IgBusReply.new_from_json_dict(item)
                for reply_id, item in data.items()
            }
