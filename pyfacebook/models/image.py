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
