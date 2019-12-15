"""
    These are models for post entity.
"""

from attr import attrs, attrib
from typing import Optional, List, Union

from .base import BaseModel
from .picture import ImageSource


@attrs
class PostShares(BaseModel):
    """
    A class representing the page post shares info.

    structure is {"count": 12}
    """
    count = attrib(default=None, type=Optional[int])


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
class ReactionsSummary(BaseModel):
    """
    A class representing the page post reaction summary info.

    Refer: https://developers.facebook.com/docs/graph-api/reference/page-post/reactions/
    """
    total_count = attrib(default=None, type=Optional[int])
    viewer_reaction = attrib(default=None, type=Optional[str])


@attrs
class Post(BaseModel):
    """
    A class representing the post info.

    Refer: https://developers.facebook.com/docs/graph-api/reference/post
    """

    # base fields
    id = attrib(default=None, type=Optional[str])
    backdated_time = attrib(default=None, type=Optional[str], repr=False)
    created_time = attrib(default=None, type=Optional[str], repr=False)
    description = attrib(default=None, type=Optional[str], repr=False)
    full_picture = attrib(default=None, type=Optional[str], repr=False)
    icon = attrib(default=None, type=Optional[str], repr=False)
    message = attrib(default=None, type=Optional[str], repr=False)
    permalink_url = attrib(default=None, type=Optional[str])
    shares = attrib(default=None, type=Optional[PostShares], repr=False)
    status_type = attrib(default=None, type=Optional[str], repr=False)
    story = attrib(default=None, type=Optional[str], repr=False)
    updated_time = attrib(default=None, type=Optional[str], repr=False)
    # connections fields
    attachments = attrib(default=None, type=Optional[Union[dict, List[StoryAttachment]]], repr=False)
    comments = attrib(default=None, type=Optional[Union[dict, CommentSummary]], repr=False)
    reactions = attrib(default=None, type=Optional[Union[dict, ReactionsSummary]], repr=False)
    like = attrib(default=None, type=Optional[Union[dict, ReactionsSummary]], repr=False)
    love = attrib(default=None, type=Optional[Union[dict, ReactionsSummary]], repr=False)
    wow = attrib(default=None, type=Optional[Union[dict, ReactionsSummary]], repr=False)
    sad = attrib(default=None, type=Optional[Union[dict, ReactionsSummary]], repr=False)
    angry = attrib(default=None, type=Optional[Union[dict, ReactionsSummary]], repr=False)
    thankful = attrib(default=None, type=Optional[Union[dict, ReactionsSummary]], repr=False)

    def __attrs_post_init__(self):
        if self.attachments is not None and isinstance(self.attachments, dict):
            attachments = self.attachments.get("data", [])
            self.attachments = [StoryAttachment.new_from_json_dict(item) for item in attachments]
        if self.comments is not None and isinstance(self.comments, dict):
            comment_summary = self.comments.get("summary", {})
            self.comments = CommentSummary.new_from_json_dict(comment_summary)
        # handle the reaction items
        self.reactions_handler("reactions", init_type=False)
        self.reactions_handler("like")
        self.reactions_handler("love")
        self.reactions_handler("wow")
        self.reactions_handler("sad")
        self.reactions_handler("angry")
        self.reactions_handler("thankful")

    def reactions_handler(self, field_name, init_type=True):
        field_value = getattr(self, field_name)
        if field_value is not None and isinstance(field_value, dict):
            field_summary = field_value.get("summary", {})
            if init_type:
                if field_summary.get("viewer_reaction") is None:
                    field_summary["viewer_reaction"] = field_name
            field_value = ReactionsSummary.new_from_json_dict(field_summary)
            setattr(self, field_name, field_value)
