"""

"""
from typing import List, Optional

from pyfacebook.api.facebook.resource.base import BaseResource
from pyfacebook.models.user import User


class FacebookUser(BaseResource):
    def get_info(
        self, user_id: str, field: Optional[List] = None, return_json: bool = False
    ):
        """
        :param user_id:
        :param field:
        :param return_json: Set to false will return a dict of instances.
        Or return json data. Default is false.
        :return:
        """
        data = self.client.get_object(
            object_id=user_id,
            fields=field,
        )
        if return_json:
            return data
        else:
            return User.new_from_json_dict(data=data)
