"""
    Apis for media.
"""
from typing import Dict, Optional, Union

import pyfacebook.utils.constant as const
from pyfacebook.api.base_resource import BaseResource
from pyfacebook.models.ig_business_models import IgBusMedia
from pyfacebook.utils.params_utils import enf_comma_separated


class IGBusinessMedia(BaseResource):
    def get_info(
        self,
        media_id: str,
        fields: Optional[Union[str, list, tuple]] = None,
        return_json: bool = False,
    ) -> Union[IgBusMedia, dict]:
        """
        Get information about a Facebook User.

        :param media_id: ID for Media.
        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param return_json: Set to false will return a dataclass for IgBusMedia.
            Or return json data. Default is false.
        :return: Business media information.
        """
        if fields is None:
            fields = const.IG_BUSINESS_MEDIA_PUBLIC_FIELDS

        data = self.client.get_object(
            object_id=media_id,
            fields=enf_comma_separated(field="fields", value=fields),
        )
        if return_json:
            return data
        else:
            return IgBusMedia.new_from_json_dict(data=data)

    def get_batch(
        self,
        ids: Optional[Union[str, list, tuple]],
        fields: Optional[Union[str, list, tuple]] = None,
        return_json: bool = False,
    ) -> Union[Dict[str, IgBusMedia], dict]:
        """
        Get batch business media information by ids

        :param ids: IDs for the medias.
        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param return_json: Set to false will return a dataclass for IgBusMedia.
            Or return json data. Default is false.
        :return: Business medias information.
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
                media_id: IgBusMedia.new_from_json_dict(item)
                for media_id, item in data.items()
            }
