"""
    models for instagram basic api.
"""
from attr import attrs, attrib
from typing import Dict, Optional

from .base import BaseModel
from .._compat import str


@attrs
class IgBasicUser(BaseModel):
    """
    A class representing the instagram basic user info.

    Refer: https://developers.facebook.com/docs/instagram-basic-display-api/reference/user
    """
    account_type = attrib(default=None, type=Optional[str], repr=False)
    id = attrib(default=None, type=Optional[str])
    media_count = attrib(default=None, type=Optional[int], repr=False)
    username = attrib(default=None, type=Optional[str])


@attrs
class IgBasicMediaChildren(BaseModel):
    """
    A class representing the instagram basic media children media info.

    Refer: https://developers.facebook.com/docs/instagram-basic-display-api/reference/media/
    """
    id = attrib(default=None, type=Optional[str])
    media_type = attrib(default=None, type=Optional[str])
    media_url = attrib(default=None, type=Optional[str], repr=False)
    permalink = attrib(default=None, type=Optional[str])
    thumbnail_url = attrib(default=None, type=Optional[str], repr=False)
    timestamp = attrib(default=None, type=Optional[str], repr=False)
    username = attrib(default=None, type=Optional[str], repr=False)


@attrs
class IgBasicMedia(BaseModel):
    """
    A class representing the instagram basic media info.

    Refer: https://developers.facebook.com/docs/instagram-basic-display-api/reference/media/
    """
    caption = attrib(default=None, type=Optional[str], repr=False)
    id = attrib(default=None, type=Optional[str])
    media_type = attrib(default=None, type=Optional[str])
    media_url = attrib(default=None, type=Optional[str], repr=False)
    permalink = attrib(default=None, type=Optional[str])
    thumbnail_url = attrib(default=None, type=Optional[str], repr=False)
    timestamp = attrib(default=None, type=Optional[str], repr=False)
    username = attrib(default=None, type=Optional[str], repr=False)
    children = attrib(default=None, type=Optional[Dict], repr=False)

    def __attrs_post_init__(self):
        if self.children is not None and isinstance(self.children, dict):
            children = self.children.get("data", [])
            self.children = [IgBasicMediaChildren.new_from_json_dict(item) for item in children]
