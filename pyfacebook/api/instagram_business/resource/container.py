"""
    Apis for container.
"""

from typing import Dict, Optional, Union

import pyfacebook.utils.constant as const
from pyfacebook.api.base_resource import BaseResource
from pyfacebook.models.ig_business_models import IgBusContainer
from pyfacebook.utils.params_utils import enf_comma_separated


class IGBusinessContainer(BaseResource):
    def get_info(
        self,
        container_id: str,
        fields: Optional[Union[str, list, tuple]] = None,
        return_json: bool = False,
    ) -> Union[IgBusContainer, dict]:
        """
        Get information about a Business Media Container.

        :param container_id: ID for Container.
        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param return_json: Set to false will return a dataclass for IgBusContainer.
            Or return json data. Default is false.
        :return: Business Container information.
        """
        if fields is None:
            fields = const.IG_BUSINESS_CONTAINER_PUBLIC_FIELDS

        data = self.client.get_object(
            object_id=container_id,
            fields=enf_comma_separated(field="fields", value=fields),
        )
        if return_json:
            return data
        else:
            return IgBusContainer.new_from_json_dict(data=data)

    def get_batch(
        self,
        ids: Optional[Union[str, list, tuple]],
        fields: Optional[Union[str, list, tuple]] = None,
        return_json: bool = False,
    ) -> Union[Dict[str, IgBusContainer], dict]:
        """
        Get batch business media containers information by ids

        :param ids: IDs for the containers.
        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param return_json: Set to false will return a dataclass for IgBusContainer.
            Or return json data. Default is false.
        :return: Business containers information.
        """
        ids = enf_comma_separated(field="ids", value=ids)

        if fields is None:
            fields = const.IG_BUSINESS_CONTAINER_PUBLIC_FIELDS

        data = self.client.get_objects(
            ids=ids, fields=enf_comma_separated(field="fields", value=fields)
        )
        if return_json:
            return data
        else:
            return {
                ct_id: IgBusContainer.new_from_json_dict(item)
                for ct_id, item in data.items()
            }
