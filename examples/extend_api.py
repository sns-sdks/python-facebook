"""
    This show extend this api for support others methods.
"""
from typing import Dict, List, Optional, Union, Tuple, Set

from attr import attrs, attrib
from pyfacebook import Api, BaseModel
from pyfacebook.utils.param_validation import enf_comma_separated


@attrs
class People(BaseModel):
    """
    Refer: https://developers.facebook.com/docs/graph-api/reference/v6.0/conversation
    """
    id = attrib(default=None, type=Optional[str])
    name = attrib(default=None, type=Optional[str])
    email = attrib(default=None, type=Optional[str], repr=False)


@attrs
class PageConversation(BaseModel):
    """
    Refer: https://developers.facebook.com/docs/graph-api/reference/v6.0/conversation
    """

    id = attrib(default=None, type=Optional[str])
    link = attrib(default=None, type=Optional[str], repr=False)
    snippet = attrib(default=None, type=Optional[str], repr=False)
    updated_time = attrib(default=None, type=Optional[str])
    message_count = attrib(default=None, type=Optional[int])
    unread_count = attrib(default=None, type=Optional[int])
    participants = attrib(default=None, type=Optional[Union[Dict, List[People]]])
    senders = attrib(default=None, type=Optional[Union[Dict, List[People]]])
    can_reply = attrib(default=None, type=Optional[bool], repr=False)
    is_subscribed = attrib(default=None, type=Optional[bool], repr=False)

    def __attrs_post_init__(self):
        if self.participants is not None and isinstance(self.participants, dict):
            participants = self.participants.get("data", [])
            self.participants = [People.new_from_json_dict(par) for par in participants]
        if self.senders is not None and isinstance(self.senders, dict):
            senders = self.senders.get("data", [])
            self.senders = [People.new_from_json_dict(sender) for sender in senders]


class ExtApi(Api):
    DEFAULT_CONVERSATION_FIELDS = [
        "id", "link", "snippet", "updated_time", "message_count",
        "unread_count", "participants", "senders", "can_reply",
        "is_subscribed",
    ]

    def page_by_next(self,
                     target,  # type: str
                     resource,  # type: str
                     args,  # type: Dict
                     next_page,  # type: str
                     ):
        # type: (...) -> (str, Dict)
        """
        :param target: target id
        :param resource: target resource field
        :param args: fields for this resource
        :param next_page: next page url
        :return:
        """
        if next_page is not None:
            resp = self._request(
                path=next_page
            )
        else:
            resp = self._request(
                path="{version}/{target}/{resource}".format(
                    version=self.version, target=target, resource=resource
                ),
                args=args
            )
        next_page = None
        data = self._parse_response(resp)
        if "paging" in data:
            next_page = data["paging"].get("next")
        return next_page, data

    def get_page_conversations(self,
                               page_id,  # type: str
                               access_token,  # type: str
                               fields=None,  # type: Optional[Union[str, List, Tuple, Set]]
                               folder="inbox",  # type: str
                               count=10,  # type: Optional[int]
                               limit=200,  # type: int,
                               return_json=False  # type: bool
                               ):
        # type: (...) -> List[Union[Dict, PageConversation]]
        """
        Retrieve conversations for target page.

        Note:
            This is need page access token and with the scope `pages_messaging`.

        :param page_id: Target page id.
        :param access_token: Page access token
        :param fields: Fields for to get data. None will use default fields.
        :param folder: Folder for conversations. default is `inbox`.
        Accept value are:
            - inbox
            - other
            - page_done
            - pending
            - spam
        :param count: The count will retrieve for the conversation if it is possible. If set None will retrieve all.
        :param limit: Each request will retrieve count for conversation, should no more than 200.
        :param return_json: Set to false will return a list of PageConversation instances.
        Or return json data. Default is false.
        :return: Conversation data list.
        """
        if fields is None:
            fields = self.DEFAULT_CONVERSATION_FIELDS

        args = {
            "access_token": access_token,
            "fields": enf_comma_separated("fields", fields),
            "folder": folder,
            "limit": limit,
        }

        conversations = []
        next_page = None

        while True:
            next_page, data = self.page_by_next(
                target=page_id, resource="conversations",
                args=args, next_page=next_page
            )
            data = data.get("data", [])

            if return_json:
                conversations.extend(data)
            else:
                conversations.extend([PageConversation.new_from_json_dict(item) for item in data])

            if count is not None:
                conversations = conversations[:count]
                break
            if next_page is None:
                break
        return conversations


if __name__ == '__main__':
    api = ExtApi(long_term_token="long-term-token")

    con = api.get_page_conversations(
        page_id="2121008874780932",
        access_token="page access token",
        limit=10,
    )
    print(con)
