"""
    Apis for hashtag.
"""

from typing import Dict, Optional, Union

import pyfacebook.utils.constant as const
from pyfacebook.api.base_resource import BaseResource
from pyfacebook.models.ig_business_models import IgBusHashtag
from pyfacebook.utils.params_utils import enf_comma_separated


class IGBusinessHashtag(BaseResource):
    def get_info(
        self,
        hashtag_id: str,
        fields: Optional[Union[str, list, tuple]] = None,
        return_json: bool = False,
    ) -> Union[IgBusHashtag, dict]:
        """
        Get information about a Business hashtag.

        :param hashtag_id: ID for Hashtag.
        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param return_json: Set to false will return a dataclass for IgBusHashtag.
            Or return json data. Default is false.
        :return: Business hashtag information.
        """
        if fields is None:
            fields = const.IG_BUSINESS_HASHTAG_PUBLIC_FIELDS

        data = self.client.get_object(
            object_id=hashtag_id,
            fields=enf_comma_separated(field="fields", value=fields),
        )
        if return_json:
            return data
        else:
            return IgBusHashtag.new_from_json_dict(data=data)

    def get_batch(
        self,
        ids: Optional[Union[str, list, tuple]],
        fields: Optional[Union[str, list, tuple]] = None,
        return_json: bool = False,
    ) -> Union[Dict[str, IgBusHashtag], dict]:
        """
        Get batch business hashtags information by ids

        :param ids: IDs for the hashtags.
        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param return_json: Set to false will return a dataclass for IgBusHashtag.
            Or return json data. Default is false.
        :return: Business hashtags information.
        """
        ids = enf_comma_separated(field="ids", value=ids)

        if fields is None:
            fields = const.IG_BUSINESS_HASHTAG_PUBLIC_FIELDS

        data = self.client.get_objects(
            ids=ids, fields=enf_comma_separated(field="fields", value=fields)
        )
        if return_json:
            return data
        else:
            return {
                tag_id: IgBusHashtag.new_from_json_dict(item)
                for tag_id, item in data.items()
            }
