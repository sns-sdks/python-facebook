"""
    These are models for post entity.
"""

from attr import attrs, attrib
from typing import Optional, Dict

from .base import BaseModel
from .common import StoryAttachment
from .mixins import CommentsSummaryField
from .._compat import str


@attrs
class PostShares(BaseModel):
    """
    A class representing the page post shares info.

    structure is {"count": 12}
    """
    count = attrib(default=None, type=Optional[int])


@attrs
class ReactionsSummary(BaseModel):
    """
    A class representing the page post reaction summary info.

    Refer: https://developers.facebook.com/docs/graph-api/reference/page-post/reactions/
    """
    total_count = attrib(default=None, type=Optional[int])
    viewer_reaction = attrib(default=None, type=Optional[str])


@attrs
class Post(BaseModel, CommentsSummaryField):
    """
    A class representing the post info.

    Refer: https://developers.facebook.com/docs/graph-api/reference/post
    """

    # base fields
    id = attrib(default=None, type=Optional[str])
    backdated_time = attrib(default=None, type=Optional[str], repr=False)
    created_time = attrib(default=None, type=Optional[str], repr=False)
    full_picture = attrib(default=None, type=Optional[str], repr=False)
    icon = attrib(default=None, type=Optional[str], repr=False)
    message = attrib(default=None, type=Optional[str], repr=False)
    permalink_url = attrib(default=None, type=Optional[str])
    shares = attrib(default=None, type=Optional[PostShares], repr=False)
    status_type = attrib(default=None, type=Optional[str], repr=False)
    story = attrib(default=None, type=Optional[str], repr=False)
    updated_time = attrib(default=None, type=Optional[str], repr=False)
    tagged_time = attrib(default=None, type=Optional[str], repr=False)  # This only for the tagged endpoint.
    # connections fields
    attachments = attrib(default=None, type=Optional[Dict], repr=False)
    comments = attrib(default=None, type=Optional[Dict], repr=False)
    reactions = attrib(default=None, type=Optional[Dict], repr=False)
    like = attrib(default=None, type=Optional[Dict], repr=False)
    love = attrib(default=None, type=Optional[Dict], repr=False)
    wow = attrib(default=None, type=Optional[Dict], repr=False)
    haha = attrib(default=None, type=Optional[Dict], repr=False)
    sad = attrib(default=None, type=Optional[Dict], repr=False)
    angry = attrib(default=None, type=Optional[Dict], repr=False)
    thankful = attrib(default=None, type=Optional[Dict], repr=False)

    def __attrs_post_init__(self):
        super(Post, self).__attrs_post_init__()

        if self.attachments is not None and isinstance(self.attachments, dict):
            attachments = self.attachments.get("data", [])
            self.attachments = [StoryAttachment.new_from_json_dict(item) for item in attachments]
        # handle the reaction items
        self.reactions_handler("reactions", init_type=False)
        self.reactions_handler("like")
        self.reactions_handler("love")
        self.reactions_handler("wow")
        self.reactions_handler("haha")
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
