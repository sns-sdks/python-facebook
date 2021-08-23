"""
    Apis for basic media
"""

from typing import Dict, Optional, Union

import pyfacebook.utils.constant as const
from pyfacebook.api.base_resource import BaseResource
from pyfacebook.models.ig_basic_models import IgBasicMedia, IgBasicMediaChildren
from pyfacebook.utils.params_utils import enf_comma_separated


class IGBasicMedia(BaseResource):
    def get_info(
        self,
        media_id: str,
        fields: Optional[Union[str, list, tuple]] = None,
        return_json: bool = False,
    ) -> Union[IgBasicMedia, dict]:
        """
        Represents an image, video, or album media data.

        :param media_id: ID for Media.
        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param return_json: Set to false will return a dataclass for IgBasicMedia.
            Or return json data. Default is false.
        :return: Basic media information.
        """

        if fields is None:
            fields = const.IG_BASIC_MEDIA_FIELDS

        data = self.client.get_object(
            object_id=media_id,
            fields=enf_comma_separated(field="fields", value=fields),
        )

        if return_json:
            return data
        else:
            return IgBasicMedia.new_from_json_dict(data)

    def get_batch(
        self,
        ids: Optional[Union[str, list, tuple]],
        fields: Optional[Union[str, list, tuple]] = None,
        return_json: bool = False,
    ) -> Union[Dict[str, IgBasicMedia], dict]:
        """
        Get batch basic media information by ids

        :param ids: IDs for the medias.
        :param fields Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param return_json: Set to false will return a dataclass for IgBasicMedia.
            Or return json data. Default is false.
        :return: Basic medias information.
        """

        ids = enf_comma_separated(field="ids", value=ids)
        if fields is None:
            fields = const.IG_BUSINESS_MEDIA_PUBLIC_FIELDS
        data = self.client.get_objects(
            ids=ids, fields=enf_comma_separated(field="fields", value=fields)
        )
        if return_json:
            return data
        else:
            return {
                media_id: IgBasicMedia.new_from_json_dict(item)
                for media_id, item in data.items()
            }

    def get_children(
        self,
        media_id: str,
        fields: Optional[Union[str, list, tuple]] = None,
        return_json: bool = False,
    ) -> Union[IgBasicMediaChildren, dict]:
        """
        Get a collection of image and video Media on an album Media.

        :param media_id: ID for the album media.
        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param return_json: Set to false will return a dataclass for IgBasicMediaChildren.
            Or return json data. Default is false.
        :return: Media children response information.
        """

        if fields is None:
            fields = const.IG_BASIC_MEDIA_CHILDREN_FIELDS

        data = self.client.get_connection(
            object_id=media_id,
            connection="children",
            fields=enf_comma_separated(field="fields", value=fields),
        )
        if return_json:
            return data
        else:
            return IgBasicMediaChildren.new_from_json_dict(data)
