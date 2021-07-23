"""
    Model class for Conversation.

    Refer: https://developers.facebook.com/docs/graph-api/reference/conversation
"""
from dataclasses import dataclass
from typing import List, Optional

from pyfacebook.models.base import BaseModel, field


@dataclass
class CvUser(BaseModel):
    """
    A class representing the User in conversation.
    """

    id: Optional[str] = field(repr=True, compare=True)
    name: Optional[str] = field(repr=True)
    email: Optional[str] = field()


@dataclass
class Participants(BaseModel):
    """
    A class representing the Participant.
    """

    data: Optional[List[CvUser]] = field(repr=True)


@dataclass
class Senders(BaseModel):
    """
    A class representing the Sender.
    """

    data: Optional[List[CvUser]] = field(repr=True)


@dataclass
class Conversation(BaseModel):
    """
    A class representing the Conversation.
    """

    id: Optional[str] = field(repr=True, compare=True)
    link: Optional[str] = field()
    snippet: Optional[str] = field()
    scoped_thread_key: Optional[str] = field()
    updated_time: Optional[str] = field(repr=True)
    message_count: Optional[int] = field()
    unread_count: Optional[int] = field()
    participants: Optional[Participants] = field()
    senders: Optional[Senders] = field()
    can_reply: Optional[bool] = field()
    is_subscribed: Optional[bool] = field()
