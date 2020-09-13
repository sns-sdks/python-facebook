"""
    some models for common.
"""
from attr import attrib, attrs
from typing import Dict, List, Optional

from .base import BaseModel
from .picture import ImageSource
from .._compat import str


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
    subattachments = attrib(default=None, type=Optional[Dict], repr=False)

    def __attrs_post_init__(self):
        if self.subattachments is not None and isinstance(self.subattachments, dict):
            subattachments = self.subattachments.get("data", [])
            self.subattachments = [StoryAttachment.new_from_json_dict(item) for item in subattachments]


@attrs
class Privacy(BaseModel):
    """
    A class representing the privacy info.

    Refer: https://developers.facebook.com/docs/graph-api/reference/privacy/
    """
    allow = attrib(default=None, type=Optional[str], repr=False)
    deny = attrib(default=None, type=Optional[str], repr=False)
    description = attrib(default=None, type=Optional[str])
    friends = attrib(default=None, type=Optional[str], repr=False)
    networks = attrib(default=None, type=Optional[str], repr=False)
    value = attrib(default=None, type=Optional[str])


@attrs
class Location(BaseModel):
    """
    A class representing the location info.

    Refer: https://developers.facebook.com/docs/graph-api/reference/location/
    """
    city = attrib(default=None, type=Optional[str])
    country = attrib(default=None, type=Optional[str], repr=False)
    latitude = attrib(default=None, type=Optional[float], repr=False)
    located_in = attrib(default=None, type=Optional[str], repr=False)
    longitude = attrib(default=None, type=Optional[float], repr=False)
    state = attrib(default=None, type=Optional[str], repr=False)
    street = attrib(default=None, type=Optional[str], repr=False)
    zip = attrib(default=None, type=Optional[str], repr=False)


@attrs
class Place(BaseModel):
    id = attrib(default=None, type=Optional[str])
    name = attrib(default=None, type=Optional[str])
    location = attrib(default=None, type=Optional[Location], repr=False)
    overall_rating = attrib(default=None, type=Optional[float], repr=False)
