"""
    Apis for message.
"""

from typing import Dict, Optional, Union

import pyfacebook.utils.constant as const
from pyfacebook.api.base_resource import BaseResource
from pyfacebook.models.message import Message
from pyfacebook.utils.params_utils import enf_comma_separated


class FacebookMessage(BaseResource):
    def get_info(
        self,
        message_id: Optional[str],
        fields: Optional[Union[str, list, tuple]] = None,
        return_json: bool = False,
    ) -> Union[Message, dict]:
        """
        Get information about a Facebook Message.

        :param message_id: ID for the Message.
        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param return_json: Set to false will return a dataclass for Message.
            Or return json data. Default is false.
        :return: Message information.
        """

        if fields is None:
            fields = const.MESSAGE_FIELDS

        data = self.client.get_object(
            object_id=message_id,
            fields=enf_comma_separated(field="fields", value=fields),
        )
        if return_json:
            return data
        else:
            return Message.new_from_json_dict(data=data)

    def get_batch(
        self,
        ids: Optional[Union[str, list, tuple]],
        fields: Optional[Union[str, list, tuple]] = None,
        return_json: bool = False,
    ) -> Union[Dict[str, Message], dict]:
        """
        Get batch Messages information by ids.

        :param ids: IDs for the Messages.
        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param return_json: Set to false will return a list dataclass for Messages.
            Or return json data. Default is false.
        :return: Messages information.
        """

        ids = enf_comma_separated(field="ids", value=ids)

        if fields is None:
            fields = const.MESSAGE_FIELDS

        data = self.client.get_objects(
            ids=ids,
            fields=enf_comma_separated(field="fields", value=fields),
        )
        if return_json:
            return data
        else:
            return {
                msg_id: Message.new_from_json_dict(item)
                for msg_id, item in data.items()
            }
