"""
    Apis for application.
"""

from typing import Dict, Optional, Union

import pyfacebook.utils.constant as const
from pyfacebook.api.base_resource import BaseResource
from pyfacebook.models.application import Application, ApplicationAccountsResponse
from pyfacebook.utils.params_utils import enf_comma_separated


class FacebookApplication(BaseResource):
    def get_info(
        self,
        fields: Optional[Union[str, list, tuple]] = None,
        return_json: bool = False,
    ) -> Union[Application, dict]:
        """
        Get information for current facebook Application. Need app token.

        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param return_json: Set to false will return a dataclass for Application.
            Or return json data. Default is false.
        :return: Application information.
        """
        if fields is None:
            fields = const.APPLICATION_PUBLIC_FIELDS

        data = self.client.get_object(
            object_id=self.client.app_id,
            fields=enf_comma_separated(field="fields", value=fields),
        )
        if return_json:
            return data
        else:
            return Application.new_from_json_dict(data=data)

    def get_accounts(
        self,
        fields: Optional[Union[str, list, dict]] = None,
        count: Optional[int] = 10,
        limit: Optional[int] = 10,
        return_json: bool = False,
    ) -> Union[ApplicationAccountsResponse, dict]:
        """
        Represents a collection of test users on an app.

        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param count: The total count for you to get data.
        :param limit: Each request retrieve objects count.
            It should no more than 100. Default is None will use api default limit.
        :param return_json: Set to false will return a dataclass for post.
            Or return json data. Default is false.
        :return: Application accounts information.
        """

        if fields is None:
            fields = const.APPLICATION_ACCOUNT_PUBLIC_FIELDS

        data = self.client.get_full_connections(
            object_id=self.client.app_id,
            connection="accounts",
            count=count,
            limit=limit,
            fields=enf_comma_separated(field="fields", value=fields),
        )
        if return_json:
            return data
        else:
            return ApplicationAccountsResponse.new_from_json_dict(data)
