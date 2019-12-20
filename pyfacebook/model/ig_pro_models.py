"""
    models for instagram platform
"""

from attr import attrs, attrib
from typing import Dict, List, Optional

from .base import BaseModel


@attrs
class IgProUser(BaseModel):
    """
    A class representing the Instagram user info.

    Refer: https://developers.facebook.com/docs/instagram-api/reference/user
    """
    biography = attrib(default=None, type=Optional[str], repr=False)
    id = attrib(default=None, type=Optional[str])
    ig_id = attrib(default=None, type=Optional[int], repr=False)
    followers_count = attrib(default=None, type=Optional[int], repr=False)
    follows_count = attrib(default=None, type=Optional[int], repr=False)
    media_count = attrib(default=None, type=Optional[int], repr=False)
    name = attrib(default=None, type=Optional[str])
    username = attrib(default=None, type=Optional[str])
    profile_picture_url = attrib(default=None, type=Optional[str], repr=False)
    website = attrib(default=None, type=Optional[str], repr=False)


@attrs
class IgProMediaChildren(BaseModel):
    """
    A class representing the Instagram media children info. This is subset for media

    Refer: https://developers.facebook.com/docs/instagram-api/reference/media
    """
    id = attrib(default=None, type=Optional[str])
    ig_id = attrib(default=None, type=Optional[int], repr=False)
    media_type = attrib(default=None, type=Optional[str], repr=False)
    media_url = attrib(default=None, type=Optional[str], repr=False)
    owner = attrib(default=None, type=Optional[IgProUser], repr=False)
    permalink = attrib(default=None, type=Optional[str])
    shortcode = attrib(default=None, type=Optional[str], repr=False)
    thumbnail_url = attrib(default=None, type=Optional[str], repr=False)
    timestamp = attrib(default=None, type=Optional[str], repr=False)
    username = attrib(default=None, type=Optional[str], repr=False)


@attrs
class IgProBaseComment(BaseModel):
    """
    A class representing the Instagram comment info. Base fields.

    Refer: https://developers.facebook.com/docs/instagram-api/reference/comment
    """
    hidden = attrib(default=None, type=Optional[bool], repr=False)
    id = attrib(default=None, type=Optional[str])
    like_count = attrib(default=None, type=Optional[int], repr=False)
    media = attrib(default=None, type=Optional[Dict], repr=False)
    text = attrib(default=None, type=Optional[str], repr=False)
    timestamp = attrib(default=None, type=Optional[str])
    user = attrib(default=None, type=Optional[IgProUser], repr=False)
    username = attrib(default=None, type=Optional[str], repr=False)


@attrs
class IgProReply(IgProBaseComment):
    """
    A class representing the Instagram replay info. This is similar to comment but have no replies.

    Refer: https://developers.facebook.com/docs/instagram-api/reference/comment
    """


@attrs
class IgProComment(IgProBaseComment):
    """
    A class representing the Instagram comment info.

    Refer: https://developers.facebook.com/docs/instagram-api/reference/comment
    """
    replies = attrib(default=None, type=Optional[List[IgProReply]], repr=False)


@attrs
class IgProMedia(BaseModel):
    """
    A class representing the Instagram media info.

    Refer: https://developers.facebook.com/docs/instagram-api/reference/media
    """
    caption = attrib(default=None, type=Optional[str], repr=False)
    children = attrib(default=None, type=Optional[List[IgProMediaChildren]], repr=False)
    comments = attrib(default=None, type=Optional[List[IgProComment]])
    comments_count = attrib(default=None, type=Optional[int], repr=False)
    id = attrib(default=None, type=Optional[str])
    ig_id = attrib(default=None, type=Optional[int], repr=False)
    is_comment_enabled = attrib(default=None, type=Optional[bool], repr=False)
    like_count = attrib(default=None, type=Optional[int], repr=False)
    media_type = attrib(default=None, type=Optional[str], repr=False)
    media_url = attrib(default=None, type=Optional[str], repr=False)
    owner = attrib(default=None, type=Optional[IgProUser], repr=False)
    permalink = attrib(default=None, type=Optional[str])
    shortcode = attrib(default=None, type=Optional[str], repr=False)
    thumbnail_url = attrib(default=None, type=Optional[str], repr=False)
    timestamp = attrib(default=None, type=Optional[str], repr=False)
    username = attrib(default=None, type=Optional[str], repr=False)


@attrs
class IgProHashtag(BaseModel):
    """
    A class representing the Instagram hashtag info.

    Refer: https://developers.facebook.com/docs/instagram-api/reference/hashtag
    """
    id = attrib(default=None, type=Optional[str])
    name = attrib(default=None, type=Optional[str])
