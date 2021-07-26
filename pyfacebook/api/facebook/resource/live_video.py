"""
    Apis for live video.
"""

from typing import Dict, Optional, Union

import pyfacebook.utils.constant as const
from pyfacebook.api.base_resource import BaseResource
from pyfacebook.models.live_video import LiveVideo
from pyfacebook.utils.params_utils import enf_comma_separated


class FacebookLiveVideo(BaseResource):
    def get_info(
        self,
        live_video_id: Optional[str],
        fields: Optional[Union[str, list, tuple]] = None,
        return_json: bool = False,
    ) -> Union[LiveVideo, dict]:
        """
        Get information about a Facebook Live Video.

        :param live_video_id: ID for the Live Video.
        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param return_json: Set to false will return a dataclass for Live Video.
            Or return json data. Default is false.
        :return: Live Video information.
        """

        if fields is None:
            fields = const.LIVE_VIDEO_PUBLIC_FIELDS

        data = self.client.get_object(
            object_id=live_video_id,
            fields=enf_comma_separated(field="fields", value=fields),
        )
        if return_json:
            return data
        else:
            return LiveVideo.new_from_json_dict(data=data)

    def get_batch(
        self,
        ids: Optional[Union[str, list, tuple]],
        fields: Optional[Union[str, list, tuple]] = None,
        return_json: bool = False,
    ) -> Union[Dict[str, LiveVideo], dict]:
        """
        Get batch live videos information by ids.

        :param ids: IDs for the live videos.
        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param return_json: Set to false will return a dataclass for Live Video.
            Or return json data. Default is false.
        :return: Live video information.
        """

        ids = enf_comma_separated(field="ids", value=ids)

        if fields is None:
            fields = const.LIVE_VIDEO_PUBLIC_FIELDS

        data = self.client.get_objects(
            ids=ids,
            fields=enf_comma_separated(field="fields", value=fields),
        )
        if return_json:
            return data
        else:
            return {
                live_video_id: LiveVideo.new_from_json_dict(item)
                for live_video_id, item in data.items()
            }
