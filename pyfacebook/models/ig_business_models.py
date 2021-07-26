"""
    Model classes for instagram business.
"""

from dataclasses import dataclass
from typing import Optional

from pyfacebook.models.base import BaseModel, field


@dataclass
class IgBusUser(BaseModel):
    """
    A class representing the Business User.

    Refer: https://developers.facebook.com/docs/instagram-api/reference/ig-user/
    """

    id: Optional[str] = field(repr=True, compare=True)
    ig_id: Optional[str] = field()
    biography: Optional[str] = field()
    followers_count: Optional[int] = field()
    follows_count: Optional[int] = field()
    media_count: Optional[int] = field()
    name: Optional[int] = field()
    profile_picture_url: Optional[str] = field()
    username: Optional[str] = field(repr=True)
    website: Optional[str] = field()
