"""
    These are models for comment.
"""

from attr import attrs, attrib
from typing import Optional

from .base import BaseModel
from .common import StoryAttachment
from .._compat import str


@attrs
class CommentSummary(BaseModel):
    """
    A class representing the comment summary info.

    Refer: https://developers.facebook.com/docs/graph-api/reference/post/comments/
    """
    order = attrib(default=None, type=Optional[str], repr=False)
    total_count = attrib(default=None, type=Optional[int])
    can_comment = attrib(default=None, type=Optional[bool])


@attrs
class Comment(BaseModel):
    """
    A class representing the comment info.

    Refer: https://developers.facebook.com/docs/graph-api/reference/v4.0/comment
    """

    # base fields
    id = attrib(default=None, type=Optional[str])
    can_like = attrib(default=None, type=Optional[bool], repr=False)
    can_comment = attrib(default=None, type=Optional[bool], repr=False)
    comment_count = attrib(default=None, type=Optional[int])
    created_time = attrib(default=None, type=Optional[str], repr=False)
    like_count = attrib(default=None, type=Optional[int])
    message = attrib(default=None, type=Optional[str], repr=False)
    permalink_url = attrib(default=None, type=Optional[str], repr=False)

    # connections fields
    attachment = attrib(default=None, type=Optional[StoryAttachment], repr=False)
