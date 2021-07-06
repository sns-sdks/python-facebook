"""
    Apis for User.
"""
from typing import Optional, Union

import pyfacebook.utils.constant as const
from pyfacebook.api.facebook.resource.base import BaseResource
from pyfacebook.models.user import User
from pyfacebook.utils.params_utils import enf_comma_separated


class FacebookUser(BaseResource):
    def get_info(
        self,
        user_id: str,
        fields: Optional[Union[str, list, tuple]] = None,
        return_json: bool = False,
    ) -> Union[User, dict]:
        """
        Get information about a Facebook User.

        :param user_id: ID for user.
        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param return_json: Set to false will return a dataclass for user.
        Or return json data. Default is false.
        :return: User information.
        """
        if fields is None:
            fields = const.USER_PUBLIC_FIELDS

        data = self.client.get_object(
            object_id=user_id,
            fields=enf_comma_separated(field="fields", value=fields),
        )
        if return_json:
            return data
        else:
            return User.new_from_json_dict(data=data)
