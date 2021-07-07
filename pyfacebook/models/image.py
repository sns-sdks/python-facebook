"""
    Extension models for graph api
"""

from dataclasses import dataclass
from typing import Optional

from pyfacebook.models.base import BaseModel, field


@dataclass
class ProfilePicture(BaseModel):
    """
    A class representing Profile Picture

    Refer: https://developers.facebook.com/docs/graph-api/reference/profile-picture-source/
    """

    cache_key: Optional[str] = field()
    height: Optional[int] = field()
    is_silhouette: Optional[bool] = field()
    url: Optional[str] = field(repr=True)
    width: Optional[int] = field()


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
