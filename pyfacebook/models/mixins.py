"""
    some common mixin for object
"""
from attr import attrs, attrib
from typing import Dict, Optional

from .comment import CommentSummary
from .likes import LikesSummary


@attrs
class LikesSummaryField(object):
    likes = attrib(default=None, type=Optional[Dict], repr=False)

    def __attrs_post_init__(self):
        if self.likes is not None and isinstance(self.likes, dict):
            likes_summary = self.likes.get("summary", {})
            self.likes = LikesSummary.new_from_json_dict(likes_summary)


@attrs
class CommentsSummaryField(object):
    comments = attrib(default=None, type=Optional[Dict], repr=False)

    def __attrs_post_init__(self):
        if self.comments is not None and isinstance(self.comments, dict):
            comment_summary = self.comments.get("summary", {})
            self.comments = CommentSummary.new_from_json_dict(comment_summary)


@attrs
class LikesAndCommentsSummaryField(LikesSummaryField, CommentsSummaryField):

    def __attrs_post_init__(self):
        if self.likes is not None and isinstance(self.likes, dict):
            likes_summary = self.likes.get("summary", {})
            self.likes = LikesSummary.new_from_json_dict(likes_summary)
        if self.comments is not None and isinstance(self.comments, dict):
            comment_summary = self.comments.get("summary", {})
            self.comments = CommentSummary.new_from_json_dict(comment_summary)
