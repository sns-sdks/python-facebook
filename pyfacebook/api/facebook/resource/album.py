"""
    Apis for album.
"""

from typing import Dict, Optional, Union

import pyfacebook.utils.constant as const
from pyfacebook.api.base_resource import BaseResource
from pyfacebook.api.facebook.common_edges import PhotosEdge
from pyfacebook.models.album import Album
from pyfacebook.utils.params_utils import enf_comma_separated


class FacebookAlbum(BaseResource, PhotosEdge):
    def get_info(
        self,
        album_id: Optional[str],
        fields: Optional[Union[str, list, tuple]] = None,
        return_json: bool = False,
    ) -> Union[Album, dict]:
        """
        Get information about a Facebook Album.

        :param album_id: ID for the Album.
        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param return_json: Set to false will return a dataclass for Album.
            Or return json data. Default is false.
        :return: Album information.
        """

        if fields is None:
            fields = const.ALBUM_PUBLIC_FIELDS

        data = self.client.get_object(
            object_id=album_id,
            fields=enf_comma_separated(field="fields", value=fields),
        )
        if return_json:
            return data
        else:
            return Album.new_from_json_dict(data=data)

    def get_batch(
        self,
        ids: Optional[Union[str, list, tuple]],
        fields: Optional[Union[str, list, tuple]] = None,
        return_json: bool = False,
    ) -> Union[Dict[str, Album], dict]:
        """
        Get batch albums information by ids.

        :param ids: IDs for the albums.
        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param return_json: Set to false will return a dataclass for Album.
            Or return json data. Default is false.
        :return: Albums information.
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
                album_id: Album.new_from_json_dict(item)
                for album_id, item in data.items()
            }
