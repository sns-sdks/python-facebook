"""
    Apis for basic user
"""
from typing import Optional, Union

import pyfacebook.utils.constant as const
from pyfacebook.api.base_resource import BaseResource
from pyfacebook.models.ig_basic_models import IgBasicUser
from pyfacebook.utils.params_utils import enf_comma_separated


class IGBasicUser(BaseResource):
    def get_info(
        self,
        user_id: str,
        fields: Optional[Union[str, list, tuple]] = None,
        return_json: bool = False,
    ) -> Union[IgBasicUser, dict]:
        """
        Represents an Instagram user profile.

        :param user_id: ID for the user, matched the access token.
        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param return_json: Set to false will return a dataclass for Account.
            Or return json data. Default is false.
        :return: IG Basic User information.
        """
        if fields is None:
            fields = const.IG_BASIC_USER_FIELDS

        data = self.client.get_object(
            object_id=user_id,
            fields=enf_comma_separated(field="fields", value=fields),
        )
        if return_json:
            return data
        else:
            return IgBasicUser.new_from_json_dict(data=data)
