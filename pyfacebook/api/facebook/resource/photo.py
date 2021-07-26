"""
    Apis for photo.
"""

from typing import Dict, Optional, Union

import pyfacebook.utils.constant as const
from pyfacebook.api.base_resource import BaseResource
from pyfacebook.models.photo import Photo
from pyfacebook.utils.params_utils import enf_comma_separated


class FacebookPhoto(BaseResource):
    def get_info(
        self,
        photo_id: Optional[str],
        fields: Optional[Union[str, list, tuple]] = None,
        return_json: bool = False,
    ) -> Union[Photo, dict]:
        """
        Get information about a Facebook Photo.

        :param photo_id: ID for the photo.
        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param return_json: Set to false will return a dataclass for Photo.
            Or return json data. Default is false.
        :return: Photo information.
        """

        if fields is None:
            fields = const.PHOTO_PUBLIC_FIELDS

        data = self.client.get_object(
            object_id=photo_id,
            fields=enf_comma_separated(field="fields", value=fields),
        )
        if return_json:
            return data
        else:
            return Photo.new_from_json_dict(data=data)

    def get_batch(
        self,
        ids: Optional[Union[str, list, tuple]],
        fields: Optional[Union[str, list, tuple]] = None,
        return_json: bool = False,
    ) -> Union[Dict[str, Photo], dict]:
        """
        Get batch photos information by ids.

        :param ids: IDs for the photos.
        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param return_json: Set to false will return a list of dataclass for Photo.
            Or return json data. Default is false.
        :return: Photos information.
        """

        ids = enf_comma_separated(field="ids", value=ids)

        if fields is None:
            fields = const.PHOTO_PUBLIC_FIELDS

        data = self.client.get_objects(
            ids=ids,
            fields=enf_comma_separated(field="fields", value=fields),
        )
        if return_json:
            return data
        else:
            return {
                photo_id: Photo.new_from_json_dict(item)
                for photo_id, item in data.items()
            }
