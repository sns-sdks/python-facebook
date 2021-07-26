"""
    Apis for conversion.
"""

from typing import Dict, Optional, Union

import pyfacebook.utils.constant as const
from pyfacebook.api.base_resource import BaseResource
from pyfacebook.models.conversation import Conversation
from pyfacebook.utils.params_utils import enf_comma_separated


class FacebookConversation(BaseResource):
    def get_info(
        self,
        conversation_id: Optional[str],
        fields: Optional[Union[str, list, tuple]] = None,
        return_json: bool = False,
    ) -> Union[Conversation, dict]:
        """
        Get information about a Facebook Conversation.

        :param conversation_id: ID for the Conversation.
        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param return_json: Set to false will return a dataclass for Conversation.
            Or return json data. Default is false.
        :return: Conversation information.
        """

        if fields is None:
            fields = const.CONVERSATION_FIELDS

        data = self.client.get_object(
            object_id=conversation_id,
            fields=enf_comma_separated(field="fields", value=fields),
        )
        if return_json:
            return data
        else:
            return Conversation.new_from_json_dict(data=data)

    def get_batch(
        self,
        ids: Optional[Union[str, list, tuple]],
        fields: Optional[Union[str, list, tuple]] = None,
        return_json: bool = False,
    ) -> Union[Dict[str, Conversation], dict]:
        """
        Get batch Conversations information by ids.

        :param ids: IDs for the Conversations.
        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param return_json: Set to false will return a dataclass for Conversations.
            Or return json data. Default is false.
        :return: Conversations information.
        """

        ids = enf_comma_separated(field="ids", value=ids)

        if fields is None:
            fields = const.CONVERSATION_FIELDS

        data = self.client.get_objects(
            ids=ids,
            fields=enf_comma_separated(field="fields", value=fields),
        )
        if return_json:
            return data
        else:
            return {
                cvs_id: Conversation.new_from_json_dict(item)
                for cvs_id, item in data.items()
            }
