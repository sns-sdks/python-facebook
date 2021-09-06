"""
    Apis for business.
"""

from typing import Dict, Optional, Union

import pyfacebook.utils.constant as const
from pyfacebook.api.base_resource import BaseResource
from pyfacebook.models.business import Business
from pyfacebook.utils.params_utils import enf_comma_separated


class FacebookBusiness(BaseResource):
    def get_info(
        self,
        business_id: str,
        fields: Optional[Union[str, list, tuple]] = None,
        return_json: bool = False,
    ) -> Union[Business, dict]:
        """
        Get information about a Facebook business.

        :param business_id: ID for the business.
        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param return_json: Set to false will return a dataclass for Business.
            Or return json data. Default is false.
        :return: Business information.
        """
        if fields is None:
            fields = const.BUSINESS_PUBLIC_FIELDS

        data = self.client.get_object(
            object_id=business_id,
            fields=enf_comma_separated(field="fields", value=fields),
        )
        if return_json:
            return data
        else:
            return Business.new_from_json_dict(data=data)

    def get_batch(
        self,
        ids: Union[str, list, tuple],
        fields: Optional[Union[str, list, tuple]] = None,
        return_json: bool = False,
    ) -> Union[Dict[str, Business], dict]:
        """
        Get batch businesses information by ids.

        :param ids: IDs for the business.
        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param return_json: Set to false will return a list of dataclass for Businesses.
            Or return json data. Default is false.
        :return: Businesses information.
        """
        ids = enf_comma_separated(field="ids", value=ids)

        if fields is None:
            fields = const.BUSINESS_PUBLIC_FIELDS

        data = self.client.get_objects(
            ids=ids,
            fields=enf_comma_separated(field="fields", value=fields),
        )
        if return_json:
            return data
        else:
            return {
                business_id: Business.new_from_json_dict(item)
                for business_id, item in data.items()
            }
