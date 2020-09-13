"""
    These are models for album entity.

    Refer: https://developers.facebook.com/docs/graph-api/reference/album
"""

from attr import attrs, attrib
from typing import Dict, Optional

from .base import BaseModel
from .common import Place
from .mixins import LikesAndCommentsSummaryField
from .._compat import str


@attrs
class Album(BaseModel, LikesAndCommentsSummaryField):
    """
    A class representing the album info.
    """

    id = attrib(default=None, type=Optional[str])
    backdated_time = attrib(default=None, type=Optional[str], repr=False)
    backdated_time_granularity = attrib(default=None, type=Optional[str], repr=False)
    can_upload = attrib(default=None, type=Optional[bool], repr=False)
    count = attrib(default=None, type=Optional[int], repr=False)
    cover_photo = attrib(default=None, type=Optional[Dict], repr=False)
    created_time = attrib(default=None, type=Optional[str])
    description = attrib(default=None, type=Optional[str], repr=False)
    # event = None
    # TODO now cattr not allow rename
    # from
    link = attrib(default=None, type=Optional[str], repr=False)
    location = attrib(default=None, type=Optional[str], repr=False)
    name = attrib(default=None, type=Optional[str])
    place = attrib(default=None, type=Optional[Place], repr=False)
    privacy = attrib(default=None, type=Optional[str], repr=False)
    type = attrib(default=None, type=Optional[str], repr=False)
    updated_time = attrib(default=None, type=Optional[str], repr=False)

    def __attrs_post_init__(self):
        super(Album, self).__attrs_post_init__()
        if self.cover_photo is not None:
            from .photo import Photo
            self.cover_photo = Photo.new_from_json_dict(self.cover_photo)
