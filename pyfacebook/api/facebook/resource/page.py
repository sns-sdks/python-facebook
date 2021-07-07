"""
    Apis for page.
"""
from typing import Optional, Union

import pyfacebook.utils.constant as const
from pyfacebook.api.facebook.resource.base import BaseResource
from pyfacebook.exceptions import LibraryError
from pyfacebook.models.page import Page
from pyfacebook.utils.params_utils import enf_comma_separated


class FacebookPage(BaseResource):
    def get_info(
        self,
        page_id: Optional[str] = None,
        username: Optional[str] = None,
        fields: Optional[Union[str, list, tuple]] = None,
        return_json=False,
    ) -> Union[Page, dict]:
        """
        Get information about a Facebook Page.

        :param page_id: ID for the page.
        :param username: Username for the page.
        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param return_json: Set to false will return a dataclass for page.
            Or return json data. Default is false.
        :return: Page information.
        """
        if page_id:
            target = page_id
        elif username:
            target = username
        else:
            raise LibraryError(
                {"message": "Specify at least one of page_id or username"}
            )

        if fields is None:
            fields = const.PAGE_PUBLIC_FIELDS

        data = self.client.get_object(
            object_id=target,
            fields=enf_comma_separated(field="fields", value=fields),
        )
        if return_json:
            return data
        else:
            return Page.new_from_json_dict(data=data)
