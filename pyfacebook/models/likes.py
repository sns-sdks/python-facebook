"""
    These are models for likes.
"""
from attr import attrs, attrib
from typing import Optional

from .base import BaseModel


@attrs
class LikesSummary(BaseModel):
    """
    A class representing the likes summary info.

    Refer: https://developers.facebook.com/docs/graph-api/reference/video/likes/
    """
    total_count = attrib(default=None, type=Optional[int])
    can_like = attrib(default=None, type=Optional[bool], repr=False)
    has_liked = attrib(default=None, type=Optional[bool], repr=False)
