"""
    These are models for video entity.

    Refer: https://developers.facebook.com/docs/graph-api/reference/video
"""

from attr import attrs, attrib
from typing import List, Optional

from .base import BaseModel
from .common import Privacy, Place
from .mixins import LikesAndCommentsSummaryField
from .._compat import str


@attrs
class VideoFormat(BaseModel):
    embed_html = attrib(default=None, type=Optional[str], repr=False)
    filter = attrib(default=None, type=Optional[str], repr=False)
    height = attrib(default=None, type=Optional[int], repr=False)
    picture = attrib(default=None, type=Optional[str])
    width = attrib(default=None, type=Optional[int], repr=False)


# TODO
# @attrs
# class VideoFrom(BaseModel):
#     id = attrib(default=None, type=Optional[str])
#     name = attrib(default=None, type=Optional[str])

@attrs
class VideoPlace(Place):
    pass


@attrs
class VideoStatus(BaseModel):
    processing_progress = attrib(default=None, type=Optional[str], repr=False)
    video_status = attrib(default=None, type=Optional[str])


@attrs
class Video(BaseModel, LikesAndCommentsSummaryField):
    """
    A class representing the video info.
    """

    id = attrib(default=None, type=Optional[str])
    ad_breaks = attrib(default=None, type=Optional[List[int]], repr=False)
    backdated_time = attrib(default=None, type=Optional[str], repr=False)
    backdated_time_granularity = attrib(default=None, type=Optional[str], repr=False)
    content_category = attrib(default=None, type=Optional[str], repr=False)
    content_tags = attrib(default=None, type=Optional[List[str]], repr=False)
    created_time = attrib(default=None, type=Optional[str])
    custom_labels = attrib(default=None, type=Optional[List[str]], repr=False)
    description = attrib(default=None, type=Optional[str])
    embed_html = attrib(default=None, type=Optional[str], repr=False)
    embeddable = attrib(default=None, type=Optional[bool], repr=False)
    format = attrib(default=None, type=Optional[List[VideoFormat]], repr=False)
    # TODO now cattr not allow rename
    # from
    icon = attrib(default=None, type=Optional[str], repr=False)
    is_crosspost_video = attrib(default=None, type=Optional[bool], repr=False)
    is_crossposting_eligible = attrib(default=None, type=Optional[bool], repr=False)
    is_instagram_eligible = attrib(default=None, type=Optional[bool], repr=False)
    length = attrib(default=None, type=Optional[float], repr=False)
    live_status = attrib(default=None, type=Optional[str], repr=False)
    permalink_url = attrib(default=None, type=Optional[str], repr=False)
    place = attrib(default=None, type=Optional[VideoPlace], repr=False)
    premiere_living_room_status = attrib(default=None, type=Optional[str], repr=False)
    privacy = attrib(default=None, type=Optional[Privacy], repr=False)
    published = attrib(default=None, type=Optional[bool], repr=False)
    scheduled_publish_time = attrib(default=None, type=Optional[str], repr=False)
    source = attrib(default=None, type=Optional[str], repr=False)
    status = attrib(default=None, type=Optional[VideoStatus], repr=False)
    title = attrib(default=None, type=Optional[str], repr=False)
    universal_video_id = attrib(default=None, type=Optional[str], repr=False)
    updated_time = attrib(default=None, type=Optional[str], repr=False)


@attrs
class VideoCaption(BaseModel):
    """
    A class representing the video caption info.
    """

    create_time = attrib(default=None, type=Optional[str])
    is_auto_generated = attrib(default=None, type=Optional[bool], repr=False)
    is_default = attrib(default=None, type=Optional[bool], repr=False)
    locale = attrib(default=None, type=Optional[str], repr=False)
    locale_name = attrib(default=None, type=Optional[str], repr=False)
    uri = attrib(default=None, type=Optional[str], repr=False)
