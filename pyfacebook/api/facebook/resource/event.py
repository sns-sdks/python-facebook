"""
    Apis for event.
"""

from typing import Dict, Optional, Union

import pyfacebook.utils.constant as const
from pyfacebook.api.base_resource import BaseResource
from pyfacebook.api.facebook.common_edges import PhotosEdge, LiveVideosEdge
from pyfacebook.models.event import Event
from pyfacebook.utils.params_utils import enf_comma_separated


class FacebookEvent(BaseResource, PhotosEdge, LiveVideosEdge):
    def get_info(
        self,
        event_id: Optional[str],
        fields: Optional[Union[str, list, tuple]] = None,
        return_json: bool = False,
    ) -> Union[Event, dict]:
        """
        Get information about a Facebook Event.

        :param event_id: ID for the Event.
        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param return_json: Set to false will return a dataclass for Event.
            Or return json data. Default is false.
        :return: Event information.
        """

        if fields is None:
            fields = const.EVENT_PUBLIC_FIELDS

        data = self.client.get_object(
            object_id=event_id,
            fields=enf_comma_separated(field="fields", value=fields),
        )
        if return_json:
            return data
        else:
            return Event.new_from_json_dict(data=data)

    def get_batch(
        self,
        ids: Optional[Union[str, list, tuple]],
        fields: Optional[Union[str, list, tuple]] = None,
        return_json: bool = False,
    ) -> Union[Dict[str, Event], dict]:
        """
        Get batch Events information by ids.

        :param ids: IDs for the Events.
        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param return_json: Set to false will return a list of dataclass for Events.
            Or return json data. Default is false.
        :return: Events information.
        """

        ids = enf_comma_separated(field="ids", value=ids)

        if fields is None:
            fields = const.EVENT_PUBLIC_FIELDS

        data = self.client.get_objects(
            ids=ids,
            fields=enf_comma_separated(field="fields", value=fields),
        )
        if return_json:
            return data
        else:
            return {
                event_id: Event.new_from_json_dict(item)
                for event_id, item in data.items()
            }
