"""
    Model classes for instagram basic display.
"""

from dataclasses import dataclass
from typing import Optional

from pyfacebook.models.base import BaseModel, field


@dataclass
class IgBasicUser(BaseModel):
    """
    A class representing the Basic display user.

    Refer: https://developers.facebook.com/docs/instagram-basic-display-api/reference/user#fields
    """

    id: Optional[str] = field(repr=True, compare=True)
    account_type: Optional[str] = field(repr=True)
    media_count: Optional[int] = field()
    username: Optional[str] = field(repr=True)
