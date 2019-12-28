"""
   These some models for facebook picture entity.
"""
from attr import attrs, attrib
from typing import Optional

from .base import BaseModel
from .._compat import str


@attrs
class CoverPhoto(BaseModel):
    """
    A class representing the cover photo info.

    Refer: https://developers.facebook.com/docs/graph-api/reference/cover-photo/
    """
    id = attrib(default=None, type=Optional[str])
    cover_id = attrib(default=None, type=Optional[str], repr=False)
    offset_x = attrib(default=None, type=Optional[float], repr=False)
    offset_y = attrib(default=None, type=Optional[float], repr=False)
    source = attrib(default=None, type=Optional[str])


@attrs
class ProfilePictureSource(BaseModel):
    """
    A class representing the profile picture source info

    Refer: https://developers.facebook.com/docs/graph-api/reference/profile-picture-source/
    """

    cache_key = attrib(default=None, type=Optional[str], repr=False)
    url = attrib(default=None, type=Optional[str])
    height = attrib(default=None, type=Optional[int])
    width = attrib(default=None, type=Optional[int])
    is_silhouette = attrib(default=None, type=Optional[bool], repr=False)


@attrs
class ImageSource(BaseModel):
    """
    A class representing the image source info.

    Structure will be {"height": 10, "width": 10, "src": "https://xxxx"}
    """
    height = attrib(default=None, type=Optional[int], repr=False)
    width = attrib(default=None, type=Optional[int], repr=False)
    src = attrib(default=None, type=Optional[str])
