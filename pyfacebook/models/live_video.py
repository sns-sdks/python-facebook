"""
    Models for live video.

    Refer: https://developers.facebook.com/docs/graph-api/reference/live-video/
"""
from dataclasses import dataclass
from typing import List, Optional

from dataclasses_json import config

from pyfacebook.models.base import BaseModel, field
from pyfacebook.models.extensions import Paging


@dataclass
class VideoCopyrightRule(BaseModel):
    """
    A class representing Video Copyright Rule.

    Refer: https://developers.facebook.com/docs/graph-api/reference/video-copyright-rule/
    """

    id: Optional[str] = field(repr=True, compare=True)
    condition_groups: Optional[List[dict]] = field()  # TODO
    copyrights: Optional[List[str]] = field()
    created_date: Optional[str] = field()
    creator: Optional[
        dict
    ] = (
        field()
    )  # TODO Refer: https://developers.facebook.com/docs/graph-api/reference/user/
    is_in_migration: Optional[bool] = field()
    name: Optional[str] = field(repr=True)


@dataclass
class VideoCopyright(BaseModel):
    """
    A class representing the Video Copyright.

    Refer: https://developers.facebook.com/docs/graph-api/reference/video-copyright/
    """

    id: Optional[str] = field(repr=True, compare=True)
    content_category: Optional[str] = field()
    copyright_content_id: Optional[str] = field()
    creator: Optional[
        dict
    ] = (
        field()
    )  # TODO Refer: https://developers.facebook.com/docs/graph-api/reference/user/
    excluded_ownership_segments: Optional[List[dict]] = field()  # TODO
    in_conflict: Optional[bool] = field()
    monitoring_status: Optional[str] = field()
    monitoring_type: Optional[str] = field()
    ownership_countries: Optional[dict] = field()
    reference_file: Optional[dict] = field()
    reference_file_disabled: Optional[bool] = field()
    reference_file_disabled_by_ops: Optional[bool] = field()
    reference_owner_id: Optional[str] = field()
    rule_ids: Optional[List[VideoCopyrightRule]] = field()
    tags: Optional[List[str]] = field()
    whitelisted_ids: Optional[List[str]] = field()


@dataclass
class LiveEncoder(BaseModel):
    """
    A class representing the Live Encoder.

    Refer: https://developers.facebook.com/docs/graph-api/reference/live-encoder/
    """

    id: Optional[str] = field(repr=True, compare=True)
    brand: Optional[str] = field()
    creation_time: Optional[str] = field()
    current_broadcast: Optional["LiveVideo"] = field()
    current_input_stream: Optional["LiveVideoInputStream"] = field()
    device_id: Optional[str] = field()
    last_heartbeat_time: Optional[str] = field()
    model: Optional[str] = field()
    name: Optional[str] = field()
    status: Optional[str] = field()
    version: Optional[str] = field()


@dataclass
class LiveVideoInputStream(BaseModel):
    """
    A class representing the Live Video Input Stream.

    Refer: https://developers.facebook.com/docs/graph-api/reference/live-video-input-stream/
    """

    id: Optional[str] = field(repr=True, compare=True)
    dash_ingest_url: Optional[str] = field()
    dash_preview_url: Optional[str] = field()
    is_master: Optional[bool] = field()
    live_encoder: Optional[LiveEncoder] = field()
    secure_stream_url: Optional[str] = field()
    stream_health: Optional[dict] = field()  # TODO
    stream_id: Optional[str] = field()
    stream_url: Optional[str] = field()


@dataclass
class LiveVideo(BaseModel):
    """
    A class representing the Live Video.
    """

    id: Optional[str] = field(repr=True, compare=True)
    ad_break_config: Optional[dict] = field()
    ad_break_failure_reason: Optional[str] = field()
    broadcast_start_time: Optional[str] = field()
    copyright: Optional[VideoCopyright] = field()
    creation_time: Optional[str] = field()
    dash_ingest_url: Optional[str] = field()
    dash_preview_url: Optional[str] = field()
    description: Optional[str] = field()
    embed_html: Optional[str] = field()
    _from: Optional[dict] = field(metadata=config(field_name="from"))
    ingest_streams: Optional[List[LiveVideoInputStream]] = field()
    is_manual_mode: Optional[bool] = field()
    is_reference_only: Optional[bool] = field()
    live_encoders: Optional[List[LiveEncoder]] = field()
    live_views: Optional[int] = field()
    overlay_url: Optional[str] = field()
    permalink_url: Optional[str] = field()
    planned_start_time: Optional[str] = field()
    seconds_left: Optional[int] = field()
    secure_stream_url: Optional[str] = field()
    status: Optional[str] = field()
    stream_url: Optional[str] = field()
    targeting: Optional[dict] = field()  # TODO
    title: Optional[str] = field(repr=True)
    video: Optional[
        dict
    ] = (
        field()
    )  # TODO Refer: https://developers.facebook.com/docs/graph-api/reference/video/


@dataclass
class LiveVideosResponse(BaseModel):
    """
    A class representing the result for live videos edge.

    Refer: https://developers.facebook.com/docs/graph-api/reference/page/live_videos
    """

    data: List[LiveVideo] = field(repr=True, compare=True)
    paging: Optional[Paging] = field()
