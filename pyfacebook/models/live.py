"""
    models for live
"""

from typing import List, Optional
from attr import attrs, attrib

from .base import BaseModel
from .mixins import CommentsSummaryField
from .._compat import str


@attrs
class LiveVideStreamHealth(BaseModel):
    """
    A class representing the live video steam heath info.

    Refer:
    """
    video_bitrate = attrib(default=None, type=Optional[float], repr=False)
    video_framerate = attrib(default=None, type=Optional[float], repr=False)
    video_gop_size = attrib(default=None, type=Optional[int], repr=False)
    video_height = attrib(default=None, type=Optional[int], repr=False)
    video_width = attrib(default=None, type=Optional[int], repr=False)
    audio_bitrate = attrib(default=None, type=Optional[float], repr=False)


@attrs
class LiveVideoInputStream(BaseModel):
    """
    A class representing the live video ingest stream info.

    Refer: https://developers.facebook.com/docs/graph-api/reference/live-video-input-stream/
    """
    id = attrib(default=None, type=Optional[str])
    dash_ingest_url = attrib(default=None, type=Optional[str], repr=False)
    dash_preview_url = attrib(default=None, type=Optional[str], repr=False)
    is_master = attrib(default=None, type=Optional[bool], repr=False)
    # live_encoder
    secure_stream_url = attrib(default=None, type=Optional[str], repr=False)
    stream_health = attrib(default=None, type=Optional[LiveVideStreamHealth], repr=False)
    stream_id = attrib(default=None, type=Optional[str], repr=False)
    stream_url = attrib(default=None, type=Optional[str], repr=False)


@attrs
class LiveVideo(BaseModel, CommentsSummaryField):
    """
    A class representing the live video info.

    Refer: https://developers.facebook.com/docs/graph-api/reference/live-video/
    """

    id = attrib(default=None, type=Optional[str])
    broadcast_start_time = attrib(default=None, type=Optional[str], repr=False)
    creation_time = attrib(default=None, type=Optional[str], repr=False)
    dash_ingest_url = attrib(default=None, type=Optional[str], repr=False)
    dash_preview_url = attrib(default=None, type=Optional[str], repr=False)
    description = attrib(default=None, type=Optional[str], repr=False)
    embed_html = attrib(default=None, type=Optional[str], repr=False)
    # _from
    ingest_streams = attrib(default=None, type=Optional[List[LiveVideoInputStream]], repr=False)
    is_manual_mode = attrib(default=None, type=Optional[bool], repr=False)
    # live_encoders
    live_views = attrib(default=None, type=Optional[int], repr=False)
    overlay_url = attrib(default=None, type=Optional[str], repr=False)
    permalink_url = attrib(default=None, type=Optional[str])
    seconds_left = attrib(default=None, type=Optional[int], repr=False)
    secure_stream_url = attrib(default=None, type=Optional[str], repr=False)
    status = attrib(default=None, type=Optional[str], repr=False)
    stream_url = attrib(default=None, type=Optional[str], repr=False)
    title = attrib(default=None, type=Optional[str], repr=False)
