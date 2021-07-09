"""
    Extension models for graph api
"""

from dataclasses import dataclass
from typing import List, Optional

from pyfacebook.models.base import BaseModel, field
from pyfacebook.models.extensions import Paging


@dataclass
class ProfilePictureSource(BaseModel):
    """
    A class representing Profile Picture Source

    Refer: https://developers.facebook.com/docs/graph-api/reference/profile-picture-source/
    """

    cache_key: Optional[str] = field()
    height: Optional[int] = field()
    is_silhouette: Optional[bool] = field()
    url: Optional[str] = field(repr=True)
    width: Optional[int] = field()


@dataclass
class Picture(BaseModel):
    """
    A class representing the Picture connection.

    Refer: https://developers.facebook.com/docs/graph-api/reference/page/picture
    """

    data: Optional[ProfilePictureSource] = field(repr=True)
    paging: Optional[Paging] = field()


@dataclass
class CoverPhoto(BaseModel):
    """
    A class representing Cover Photo

    Refer: https://developers.facebook.com/docs/graph-api/reference/cover-photo/
    """

    id: Optional[str] = field(repr=True, compare=True)
    offset_x: Optional[float] = field()
    offset_y: Optional[float] = field()
    source: Optional[str] = field(repr=True)


@dataclass
class ImageSource(BaseModel):
    """
    A class representing the Image Source.
    """

    height: Optional[int] = field()
    width: Optional[int] = field()
    src: Optional[str] = field(repr=True)
