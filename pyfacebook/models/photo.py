"""
    These are models for photo entity.

    Refer: https://developers.facebook.com/docs/graph-api/reference/photo
"""

from attr import attrs, attrib
from typing import Dict, List, Optional

from .base import BaseModel
from .common import Place, EntityAtTextRange
from .mixins import LikesSummaryField
from .._compat import str


@attrs
class PlatformImageSource(BaseModel):
    height = attrib(default=None, type=Optional[int], repr=False)
    source = attrib(default=None, type=Optional[str], repr=False)
    width = attrib(default=None, type=Optional[int], repr=False)


@attrs
class Photo(BaseModel, LikesSummaryField):
    """
    A class representing the photo info.
    """

    id = attrib(default=None, type=Optional[str])
    album = attrib(default=None, type=Optional[Dict], repr=False)
    alt_text = attrib(default=None, type=Optional[str], repr=False)
    alt_text_custom = attrib(default=None, type=Optional[str], repr=False)
    backdated_time = attrib(default=None, type=Optional[str], repr=False)
    backdated_time_granularity = attrib(default=None, type=Optional[str], repr=False)
    can_backdate = attrib(default=None, type=Optional[bool], repr=False)
    can_delete = attrib(default=None, type=Optional[bool], repr=False)
    can_tag = attrib(default=None, type=Optional[bool], repr=False)
    created_time = attrib(default=None, type=Optional[str])
    # event = None
    # TODO now cattr not allow rename
    # from
    height = attrib(default=None, type=Optional[int], repr=False)
    icon = attrib(default=None, type=Optional[str], repr=False)
    images = attrib(default=None, type=Optional[List[PlatformImageSource]], repr=False)
    link = attrib(default=None, type=Optional[str], repr=False)
    name = attrib(default=None, type=Optional[str])
    name_tags = attrib(default=None, type=Optional[List[EntityAtTextRange]], repr=False)
    page_story_id = attrib(default=None, type=Optional[str], repr=False)
    place = attrib(default=None, type=Optional[Place], repr=False)
    updated_time = attrib(default=None, type=Optional[str], repr=False)
    webp_images = attrib(default=None, type=Optional[List[PlatformImageSource]], repr=False)
    width = attrib(default=None, type=Optional[int], repr=False)

    def __attrs_post_init__(self):
        super(Photo, self).__attrs_post_init__()
        if self.album is not None:
            from .album import Album
            self.album = Album.new_from_json_dict(self.album)
