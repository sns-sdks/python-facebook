"""
    Apis for user.
"""

from typing import Optional, Union

import pyfacebook.utils.constant as const
from pyfacebook.api.base_resource import BaseResource
from pyfacebook.models.ig_business_models import IgBusUser
from pyfacebook.utils.params_utils import enf_comma_separated


class IGBusinessUser(BaseResource):
    def get_info(
        self,
        user_id: str,
        fields: Optional[Union[str, list, tuple]] = None,
        return_json: bool = False,
    ) -> Union[IgBusUser, dict]:
        """
        Get information about an Instagram Business Account or an Instagram Creator Account.

        :param user_id: ID for Account.
        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param return_json: Set to false will return a dataclass for Account.
            Or return json data. Default is false.
        :return: IG Business User information.
        """
        if fields is None:
            fields = const.IG_BUSINESS_USER_PUBLIC_FIELDS

        data = self.client.get_object(
            object_id=user_id,
            fields=enf_comma_separated(field="fields", value=fields),
        )
        if return_json:
            return data
        else:
            return IgBusUser.new_from_json_dict(data=data)
