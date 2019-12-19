"""
    models for instagram platform
"""

from attr import attrs, attrib
from typing import Optional

from .base import BaseModel


class IgUser(BaseModel):
    """
    A class representing the Instagram user info.

    Refer: https://developers.facebook.com/docs/instagram-api/reference/user
    """
    biography = attrib(default=None, type=Optional[str], repr=False)
    id = attrib(default=None, type=Optional[str])
    ig_id = attrib(default=None, type=Optional[int], repr=False)
    followers_count = attrib(default=None, type=Optional[int], repr=False)
    follows_count = attrib(default=None, type=Optional[int], repr=False)
    media_count = attrib(default=None, type=Optional[int], repr=False)
    name = attrib(default=None, type=Optional[str])
    username = attrib(default=None, type=Optional[str])
    profile_picture_url = attrib(default=None, type=Optional[str], repr=False)
    website = attrib(default=None, type=Optional[str], repr=False)
