"""
    Model class for Message.

    Refer: https://developers.facebook.com/docs/graph-api/reference/message
"""

from dataclasses import dataclass
from typing import List, Optional

from dataclasses_json import config

from pyfacebook.models.base import BaseModel, field


@dataclass
class Tag(BaseModel):
    """
    A class representing the tag in message.
    """

    name: Optional[str] = field(repr=True)


@dataclass
class MessageTags(BaseModel):
    """
    A class representing the tags in message.
    """

    data: Optional[List[Tag]] = field(repr=True)


@dataclass
class MsgUser(BaseModel):
    """
    A class representing the User in message.
    """

    id: Optional[str] = field(repr=True, compare=True)
    name: Optional[str] = field(repr=True)
    email: Optional[str] = field()


@dataclass
class MessageTo(BaseModel):
    """
    A class representing the to in message.
    """

    data: Optional[List[MsgUser]] = field(repr=True)


@dataclass
class MessageAttachmentImageData(BaseModel):
    """
    A class representing the image in attachment.
    """

    width: Optional[int] = field()
    height: Optional[int] = field()
    max_width: Optional[int] = field()
    max_height: Optional[int] = field()
    url: Optional[str] = field(repr=True)
    preview_url: Optional[str] = field()
    raw_gif_image: Optional[str] = field()
    raw_webp_image: Optional[str] = field()
    animated_gif_url: Optional[str] = field()
    animated_gif_preview_url: Optional[str] = field()
    animated_webp_url: Optional[str] = field()
    animated_webp_preview_url: Optional[str] = field()
    image_type: Optional[int] = field()
    render_as_sticker: Optional[bool] = field()


@dataclass
class MessageAttachmentVideoData(BaseModel):
    """
    A class representing the video in attachment.
    """

    width: Optional[int] = field()
    height: Optional[int] = field()
    length: Optional[int] = field()
    video_type: Optional[int] = field()
    url: Optional[str] = field(repr=True)
    preview_url: Optional[str] = field()
    rotation: Optional[int] = field()


@dataclass
class MessageAttachment(BaseModel):
    """
    A class representing the Attachment in message.

    Refer: https://developers.facebook.com/docs/graph-api/reference/v11.0/message/attachments
    """

    id: Optional[str] = field(repr=True, compare=True)
    mime_type: Optional[str] = field()
    name: Optional[str] = field()
    size: Optional[int] = field()
    file_url: Optional[str] = field()
    image_data: Optional[MessageAttachmentImageData] = field()
    video_data: Optional[MessageAttachmentVideoData] = field()


@dataclass
class MessageAttachments(BaseModel):
    """
    A class representing the attachments in message.
    """

    data: Optional[List[MessageAttachment]] = field(repr=True)


@dataclass
class Message(BaseModel):
    """
    A class representing the Message
    """

    id: Optional[str] = field(repr=True, compare=True)
    created_time: Optional[str] = field()
    _from: Optional[dict] = field(metadata=config(field_name="from"))
    message: Optional[str] = field()
    tags: Optional[MessageTags] = field()
    to: Optional[MessageTo] = field()
    sticker: Optional[str] = field()

    # common connections
    attachments: Optional[MessageAttachments] = field()
