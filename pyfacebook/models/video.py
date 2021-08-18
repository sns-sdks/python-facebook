"""
    Model for video.

    Refer: https://developers.facebook.com/docs/graph-api/reference/video/
"""

from dataclasses import dataclass
from typing import List, Optional

from dataclasses_json import config

from pyfacebook.models.base import BaseModel, field
from pyfacebook.models.extensions import Paging, Privacy


@dataclass
class VideoFormat(BaseModel):
    """
    A class representing the Video Format.

    Refer: https://developers.facebook.com/docs/graph-api/reference/video-format/
    """

    embed_html: Optional[str] = field()
    filter: Optional[str] = field(repr=True)
    height: Optional[int] = field()
    picture: Optional[str] = field()
    width: Optional[int] = field()


@dataclass
class VideoStatus(BaseModel):
    """
    A class representing the Video Status.

    Refer: https://developers.facebook.com/docs/graph-api/reference/video-status/
    """

    processing_progress: Optional[int] = field(repr=True)
    video_status: Optional[str] = field(repr=True)


@dataclass
class Video(BaseModel):
    """
    A class representing the Video.
    """

    id: Optional[str] = field(repr=True, compare=True)
    ad_breaks: Optional[List[int]] = field()
    backdated_time: Optional[str] = field()
    backdated_time_granularity: Optional[str] = field()
    content_category: Optional[str] = field()
    content_tags: Optional[List[int]] = field()
    created_time: Optional[str] = field()
    custom_labels: Optional[List[str]] = field()
    description: Optional[str] = field(repr=True)
    embed_html: Optional[str] = field()
    embeddable: Optional[bool] = field()
    event: Optional[
        dict
    ] = (
        field()
    )  # TODO Refer: https://developers.facebook.com/docs/graph-api/reference/event/
    format: Optional[List[VideoFormat]] = field()
    _from: Optional[dict] = field(metadata=config(field_name="from"))
    icon: Optional[str] = field()
    is_crosspost_video: Optional[bool] = field()
    is_crossposting_eligible: Optional[bool] = field()
    is_episode: Optional[bool] = field()
    is_instagram_eligible: Optional[bool] = field()
    is_reference_only: Optional[bool] = field()
    length: Optional[float] = field()
    live_status: Optional[str] = field()
    music_video_copyright: Optional[dict] = field()  # TODO
    permalink_url: Optional[str] = field()
    place: Optional[
        dict
    ] = (
        field()
    )  # TODO Refer: https://developers.facebook.com/docs/graph-api/reference/place/
    premiere_living_room_status: Optional[str] = field()
    privacy: Optional[Privacy] = field()
    published: Optional[bool] = field()
    scheduled_publish_time: Optional[str] = field()
    source: Optional[str] = field()
    status: Optional[VideoStatus] = field()
    title: Optional[str] = field()
    universal_video_id: Optional[str] = field()
    updated_time: Optional[str] = field()


@dataclass
class VideosResponse(BaseModel):
    """
    A class represent the result for videos edge.

    Refer: https://developers.facebook.com/docs/graph-api/reference/page/videos
    """

    data: List[Video] = field(repr=True, compare=True)
    paging: Optional[Paging] = field()
