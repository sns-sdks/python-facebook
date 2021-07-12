"""
    Models for Attachments

    Refer: https://developers.facebook.com/docs/graph-api/reference/post/attachments/
"""

from dataclasses import dataclass
from typing import List, Optional

from pyfacebook.models.base import BaseModel, field
from pyfacebook.models.extensions import Paging
from pyfacebook.models.image import ImageSource


@dataclass
class EntityAtTextRange(BaseModel):
    """
    A class representing the Entity At Text Range.

    Refer: https://developers.facebook.com/docs/graph-api/reference/entity-at-text-range/
    """

    id: Optional[str] = field(repr=True, compare=True)
    length: Optional[int] = field()
    name: Optional[str] = field(repr=True)
    object: Optional[dict] = field()  # TODO
    offset: Optional[int] = field()
    type: Optional[str] = field()


@dataclass
class StoryAttachmentMedia(BaseModel):
    """
    A class representing the Story Attachment Media.

    Refer: https://developers.facebook.com/docs/graph-api/reference/story-attachment-media/
    """

    image: Optional[ImageSource] = field()
    source: Optional[str] = field(repr=True)


@dataclass
class StoryAttachmentTarget(BaseModel):
    """
    A class representing the Story Attachment Target.

    Refer: https://developers.facebook.com/docs/graph-api/reference/story-attachment-target/
    """

    id: Optional[str] = field(repr=True)
    unshimmed_url: Optional[str] = field()
    url: Optional[str] = field()


@dataclass
class StoryAttachmentSubattachments(BaseModel):
    """
    A class representing the Story Attachment Subattachments.

    Refer: https://developers.facebook.com/docs/graph-api/reference/story-attachment/subattachments/
    """

    data: Optional[List["StoryAttachment"]] = field(repr=True)
    paging: Optional[Paging] = field()


@dataclass
class StoryAttachment(BaseModel):
    """
    A class representing the Story Attachment

    Refer: https://developers.facebook.com/docs/graph-api/reference/story-attachment/
    """

    description: Optional[str] = field()
    description_tags: Optional[List[EntityAtTextRange]] = field()
    media: Optional[StoryAttachmentMedia] = field()
    media_type: Optional[str] = field(repr=True)
    target: Optional[StoryAttachmentTarget] = field()
    title: Optional[str] = field()
    type: Optional[str] = field(repr=True)
    unshimmed_url: Optional[str] = field()
    url: Optional[str] = field()

    # common connections
    subattachments: Optional[StoryAttachmentSubattachments] = field()


@dataclass
class Attachments(BaseModel):
    """
    A class representing the Attachments connection.

    Refer: https://developers.facebook.com/docs/graph-api/reference/post/attachments/
    """

    data: Optional[List[StoryAttachment]] = field(repr=True)
    paging: Optional[Paging] = field()
