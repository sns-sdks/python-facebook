"""
    Apis for video
"""

from typing import Dict, Optional, Union

import pyfacebook.utils.constant as const
from pyfacebook.api.base_resource import BaseResource
from pyfacebook.models.video import Video
from pyfacebook.utils.params_utils import enf_comma_separated


class FacebookVideo(BaseResource):
    def get_info(
        self,
        video_id: Optional[str],
        fields: Optional[Union[str, list, tuple]] = None,
        return_json: bool = False,
    ) -> Union[Video, dict]:
        """
        Get information about a Facebook Video.

        :param video_id: ID for the video.
        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param return_json: Set to false will return a dataclass for Video.
            Or return json data. Default is false.
        :return: Video information.
        """
        if fields is None:
            fields = const.VIDEO_PUBLIC_FIELDS
        data = self.client.get_object(
            object_id=video_id,
            fields=enf_comma_separated(field="fields", value=fields),
        )
        if return_json:
            return data
        else:
            return Video.new_from_json_dict(data=data)

    def get_batch(
        self,
        ids: Optional[Union[str, list, tuple]],
        fields: Optional[Union[str, list, tuple]] = None,
        return_json: bool = False,
    ) -> Union[Dict[str, Video], dict]:
        """
        Get batch photos information by ids.

        :param ids: IDs for the photos.
        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param return_json: Set to false will return a dataclass for Photo.
            Or return json data. Default is false.
        :return: Photos information.
        """

        ids = enf_comma_separated(field="ids", value=ids)

        if fields is None:
            fields = const.VIDEO_PUBLIC_FIELDS

        data = self.client.get_objects(
            ids=ids,
            fields=enf_comma_separated(field="fields", value=fields),
        )
        if return_json:
            return data
        else:
            return {
                video_id: Video.new_from_json_dict(item)
                for video_id, item in data.items()
            }
