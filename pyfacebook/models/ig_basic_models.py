"""
    Model classes for instagram basic display.
"""

from dataclasses import dataclass
from typing import List, Optional

from pyfacebook.models.base import BaseModel, field
from pyfacebook.models.extensions import Paging


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


@dataclass
class IgBasicMediaChild(BaseModel):
    """
    A class representing the Basic display media child.

    Refer: https://developers.facebook.com/docs/instagram-basic-display-api/reference/media#fields
    """

    id: Optional[str] = field(repr=True, compare=True)
    caption: Optional[str] = field()
    media_type: Optional[str] = field()
    media_url: Optional[str] = field(repr=True)
    permalink: Optional[str] = field()
    thumbnail_url: Optional[str] = field()
    timestamp: Optional[str] = field()


@dataclass
class IgBasicMediaChildren(BaseModel):
    """
    A class representing the Basic display media children data.

    Refer: https://developers.facebook.com/docs/instagram-basic-display-api/reference/media/children
    """

    data: Optional[List[IgBasicMediaChild]] = field(repr=True)
    paging: Optional[Paging] = field()


@dataclass
class IgBasicMedia(IgBasicMediaChild):
    """
    A class representing the Basic display media.

    Refer: https://developers.facebook.com/docs/instagram-basic-display-api/reference/media#fields
    """

    username: Optional[str] = field()


@dataclass
class IgBasicMediaResponse(IgBasicMediaChild):
    """
    A class representing the Basic display medias response.

    Refer: https://developers.facebook.com/docs/instagram-basic-display-api/reference/user/media
    """

    data: Optional[List[IgBasicMedia]] = field(repr=True, compare=True)
    paging: Optional[Paging] = field(repr=True)
