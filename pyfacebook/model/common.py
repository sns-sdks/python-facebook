"""
    some models for common.
"""
from attr import attrib, attrs
from typing import Optional, List

from .base import BaseModel
from .picture import ImageSource


@attrs
class EntityAtTextRange(BaseModel):
    """
    A class representing the entity at text range info.

    Refer: https://developers.facebook.com/docs/graph-api/reference/entity-at-text-range/
    """
    id = attrib(default=None, type=Optional[str])
    length = attrib(default=None, type=Optional[int], repr=False)
    name = attrib(default=None, type=Optional[str])
    offset = attrib(default=None, type=Optional[int], repr=False)
    type = attrib(default=None, type=Optional[str])


@attrs
class StoryAttachmentMedia(BaseModel):
    """
    A class representing the post attachment media info.

    Refer: https://developers.facebook.com/docs/graph-api/reference/story-attachment-media/
    """
    image = attrib(default=None, type=Optional[ImageSource])
    source = attrib(default=None, type=Optional[str], repr=False)


@attrs
class StoryAttachmentTarget(BaseModel):
    """
    A class representing the post attachment target info.

    Refer: https://developers.facebook.com/docs/graph-api/reference/story-attachment-target/
    """
    id = attrib(default=None, type=Optional[str])
    unshimmed_url = attrib(default=None, type=Optional[str], repr=False)
    url = attrib(default=None, type=Optional[str], repr=False)


@attrs
class StoryAttachment(BaseModel):
    """
    A class representing the post attachment info.

    Refer: https://developers.facebook.com/docs/graph-api/reference/story-attachment/
    """
    description = attrib(default=None, type=Optional[str])
    description_tags = attrib(default=None, type=Optional[List[EntityAtTextRange]], repr=False)
    media = attrib(default=None, type=Optional[StoryAttachmentMedia], repr=False)
    media_type = attrib(default=None, type=Optional[str])
    target = attrib(default=None, type=Optional[StoryAttachmentTarget], repr=False)
    title = attrib(default=None, type=Optional[str], repr=False)
    type = attrib(default=None, type=Optional[str])
    unshimmed_url = attrib(default=None, type=Optional[str], repr=False)
    url = attrib(default=None, type=Optional[str], repr=False)