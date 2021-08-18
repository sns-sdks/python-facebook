"""
    Models for comment.

    Refer: https://developers.facebook.com/docs/graph-api/reference/comment
"""

from dataclasses import dataclass
from typing import List, Optional

from dataclasses_json import config

from pyfacebook.models.base import BaseModel, field
from pyfacebook.models.extensions import Paging
from pyfacebook.models.attachment import StoryAttachment


@dataclass
class MessageTag(BaseModel):
    """
    A class representing the Message Tag.
    """

    id: Optional[str] = field(repr=True, compare=True)
    name: Optional[str] = field(repr=True)
    type: Optional[str] = field()
    offset: Optional[int] = field()
    length: Optional[int] = field()


@dataclass
class Comment(BaseModel):
    """
    A class representing the Comment.
    """

    id: Optional[str] = field(repr=True, compare=True)
    attachment: Optional[StoryAttachment] = field()
    can_comment: Optional[bool] = field()
    can_remove: Optional[bool] = field()
    can_hide: Optional[bool] = field()
    can_like: Optional[bool] = field()
    can_reply_privately: Optional[bool] = field()
    comment_count: Optional[int] = field()
    created_time: Optional[str] = field()
    _from: Optional[dict] = field(metadata=config(field_name="from"))
    like_count: Optional[int] = field()
    message: Optional[str] = field()
    message_tags: Optional[List[MessageTag]] = field()
    object: Optional[dict] = field()  # TODO
    parent: Optional["Comment"] = field()
    permalink_url: Optional[str] = field()
    private_reply_conversation: Optional[
        dict
    ] = (
        field()
    )  # TODO Refer: https://developers.facebook.com/docs/graph-api/reference/conversation
    user_likes: Optional[bool] = field()


@dataclass
class CommentsSummary(BaseModel):
    """
    A class representing the summary for comments.

    Refer: https://developers.facebook.com/docs/graph-api/reference/object/comments
    """

    order: Optional[str] = field(repr=True)
    total_count: Optional[int] = field(repr=True)
    can_comment: Optional[bool] = field()


@dataclass
class CommentsResponse(BaseModel):
    """
    A class representing the result for comments edge.

    Refer: https://developers.facebook.com/docs/graph-api/reference/object/comments
    """

    data: List[Comment] = field(repr=True, compare=True)
    paging: Optional[Paging] = field()
    summary: Optional[CommentsSummary] = field(repr=True)
