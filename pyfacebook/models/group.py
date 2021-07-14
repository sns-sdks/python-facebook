"""
    Models for group.

    Refer: https://developers.facebook.com/docs/graph-api/reference/group
"""

from dataclasses import dataclass
from typing import List, Optional

from pyfacebook.models.base import BaseModel, field
from pyfacebook.models.image import CoverPhoto, Picture


@dataclass
class Group(BaseModel):
    """
    A class representing the group.

    Refer: https://developers.facebook.com/docs/graph-api/reference/group
    """

    id: Optional[str] = field(repr=True, compare=True)
    cover: Optional[CoverPhoto] = field()
    created_time: Optional[str] = field()
    description: Optional[str] = field()
    email: Optional[str] = field()
    icon: Optional[str] = field()
    member_count: Optional[int] = field()
    member_request_count: Optional[int] = field()
    membership_state: Optional[str] = field()
    name: Optional[str] = field()
    parent: Optional[dict] = field()  # TODO
    permissions: Optional[List[str]] = field()
    privacy: Optional[str] = field()
    updated_time: Optional[str] = field()

    # common connection
    picture: Optional[Picture] = field()
