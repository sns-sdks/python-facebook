"""
    Models for post.

    Refer: https://developers.facebook.com/docs/graph-api/reference/post/
"""

from dataclasses import dataclass
from typing import List, Optional

from dataclasses_json import config

from pyfacebook.models.base import BaseModel, field
from pyfacebook.models.extensions import Paging, Privacy, Reactions
from pyfacebook.models.attachment import Attachments
from pyfacebook.models.place import Place


@dataclass
class PostAction(BaseModel):
    """
    A class representing the post action
    """

    name: Optional[str] = field(repr=True)
    link: Optional[str] = field()


@dataclass
class PostTag(BaseModel):
    """
    A class representing the post tag.
    """

    id: Optional[str] = field(repr=True, compare=True)
    name: Optional[str] = field(repr=True)
    type: Optional[str] = field()
    offset: Optional[int] = field()
    length: Optional[int] = field()


@dataclass
class PostShare(BaseModel):
    """
    A class representing the post share
    """

    count: Optional[int] = field(repr=True)


@dataclass
class Post(BaseModel):
    """
    A class representing the post.
    """

    id: Optional[str] = field(repr=True, compare=True)
    actions: Optional[List[PostAction]] = field()
    admin_creator: Optional[dict] = field()  # TODO
    allowed_advertising_objectives: Optional[List[str]] = field()
    application: Optional[
        dict
    ] = (
        field()
    )  # TODO https://developers.facebook.com/docs/graph-api/reference/application/
    backdated_time: Optional[str] = field()
    call_to_action: Optional[dict] = field()
    can_reply_privately: Optional[bool] = field()
    child_attachments: Optional[List[dict]] = field()  # TODO
    comments_mirroring_domain: Optional[str] = field()
    coordinates: Optional[List[dict]] = field()  # TODO
    created_time: Optional[str] = field()
    event: Optional[
        dict
    ] = field()  # TODO https://developers.facebook.com/docs/graph-api/reference/event/
    expanded_height: Optional[int] = field()
    expanded_width: Optional[int] = field()
    feed_targeting: Optional[dict] = field()  # TODO
    _from: Optional[dict] = field(metadata=config(field_name="from"))
    full_picture: Optional[str] = field()
    height: Optional[int] = field()
    icon: Optional[str] = field()
    instagram_eligibility: Optional[str] = field()
    is_app_share: Optional[bool] = field()
    is_eligible_for_promotion: Optional[bool] = field()
    is_expired: Optional[bool] = field()
    is_hidden: Optional[bool] = field()
    is_inline_created: Optional[bool] = field()
    is_instagram_eligible: Optional[bool] = field()
    is_popular: Optional[bool] = field()
    is_published: Optional[bool] = field()
    is_spherical: Optional[bool] = field()
    message: Optional[str] = field(repr=True)
    message_tags: Optional[List[PostTag]] = field()
    multi_share_end_card: Optional[bool] = field()
    multi_share_optimized: Optional[bool] = field()
    parent_id: Optional[str] = field()
    permalink_url: Optional[str] = field()
    picture: Optional[str] = field()
    place: Optional[Place] = field()
    privacy: Optional[Privacy] = field()
    promotable_id: Optional[str] = field()
    properties: Optional[List[dict]] = field()  # TODO
    scheduled_publish_time: Optional[float] = field()
    shares: Optional[PostShare] = field()
    status_type: Optional[str] = field()
    story: Optional[str] = field()
    story_tags: Optional[List[PostTag]] = field()
    subscribed: Optional[bool] = field()
    target: Optional[dict] = field()
    targeting: Optional[dict] = field()  # TODO
    tagged_time: Optional[str] = field()  # Only for tagged posts.
    timeline_visibility: Optional[str] = field()
    updated_time: Optional[str] = field()
    via: Optional[dict] = field()
    video_buying_eligibility: Optional[List[str]] = field()
    width: Optional[int] = field()

    # common connections
    attachments: Optional[Attachments] = field()
    comments: Optional[dict] = field()  # TODO
    reactions: Optional[Reactions] = field()
    like: Optional[Reactions] = field()
    love: Optional[Reactions] = field()
    wow: Optional[Reactions] = field()
    haha: Optional[Reactions] = field()
    sad: Optional[Reactions] = field()
    angry: Optional[Reactions] = field()

    def __repr__(self):
        # Message shorten
        message = f"{self.message[:30]}..."
        return f"Post(id={self.id},message={message})"


@dataclass
class FeedResponse(BaseModel):
    """
    A class representing the post response.

    Refer: https://developers.facebook.com/docs/graph-api/reference/page/feed/#read
    """

    data: List[Post] = field(repr=True, compare=True)
    paging: Optional[Paging] = field()
