"""
    Model classes for instagram business.
"""

from dataclasses import dataclass
from typing import List, Optional

from pyfacebook.models.base import BaseModel, field
from pyfacebook.models.extensions import Paging


@dataclass
class IgBusUser(BaseModel):
    """
    A class representing the Business User.

    Refer: https://developers.facebook.com/docs/instagram-api/reference/ig-user/
    """

    id: Optional[str] = field(repr=True, compare=True)
    ig_id: Optional[str] = field()
    biography: Optional[str] = field()
    followers_count: Optional[int] = field()
    follows_count: Optional[int] = field()
    media_count: Optional[int] = field()
    name: Optional[int] = field()
    profile_picture_url: Optional[str] = field()
    username: Optional[str] = field(repr=True)
    website: Optional[str] = field()


@dataclass
class IgBusMediaChild(BaseModel):
    """
    A class representing the child for media children.
    """

    id: Optional[str] = field(repr=True, compare=True)
    ig_id: Optional[str] = field()
    media_type: Optional[str] = field()
    media_url: Optional[str] = field(repr=True)
    owner: Optional[IgBusUser] = field()
    permalink: Optional[str] = field()
    shortcode: Optional[str] = field()
    thumbnail_url: Optional[str] = field()
    timestamp: Optional[str] = field()
    username: Optional[str] = field()


@dataclass
class IgBusMediaChildren(BaseModel):
    """
    A class representing the Children for the media.

    Refer: https://developers.facebook.com/docs/instagram-api/reference/ig-media/children
    """

    data: Optional[List[IgBusMediaChild]] = field()


@dataclass
class IgBusMedia(BaseModel):
    """
    A class representing the Business Media.

    Refer: https://developers.facebook.com/docs/instagram-api/reference/ig-media/
    """

    id: Optional[str] = field(repr=True, compare=True)
    ig_id: Optional[str] = field()
    caption: Optional[str] = field()
    children: Optional[IgBusMediaChildren] = field()
    comments_count: Optional[int] = field()
    is_comment_enabled: Optional[bool] = field()
    like_count: Optional[int] = field()
    media_product_type: Optional[str] = field()
    media_type: Optional[str] = field()
    media_url: Optional[str] = field(repr=True)
    owner: Optional[IgBusUser] = field()
    permalink: Optional[str] = field()
    shortcode: Optional[str] = field()
    thumbnail_url: Optional[str] = field()
    timestamp: Optional[str] = field()
    username: Optional[str] = field()
    video_title: Optional[str] = field()


@dataclass
class IgBusMediaResponse(BaseModel):
    """
    A class representing the Business Medias response.

    Refer: https://developers.facebook.com/docs/instagram-api/reference/ig-user/media
    """

    data: List[IgBusMedia] = field(repr=True, compare=True)
    paging: Optional[Paging] = field(repr=True)


@dataclass
class IgBusReply(BaseModel):
    """
    A class representing the Reply.
    Like a Comment.
    """

    id: Optional[str] = field(repr=True, compare=True)
    like_count: Optional[int] = field()
    media: Optional[IgBusMedia] = field()
    text: Optional[str] = field(repr=True)
    timestamp: Optional[str] = field()
    user: Optional[IgBusUser] = field()
    username: Optional[str] = field()


@dataclass
class IgBusReplies(BaseModel):
    """
    A class representing the Replies for comment.

    Refer: https://developers.facebook.com/docs/instagram-api/reference/ig-comment/replies
    """

    data: Optional[List[IgBusReply]] = field()


@dataclass
class IgBusComment(IgBusReply):
    """
    A class representing the Business Comment.

    Refer: https://developers.facebook.com/docs/instagram-api/reference/ig-comment/
    """

    replies: Optional[IgBusReplies] = field()


@dataclass
class IgBusHashtag(BaseModel):
    """
    A class representing the hashtag.

    Refer: https://developers.facebook.com/docs/instagram-api/reference/ig-hashtag/
    """

    id: Optional[str] = field(repr=True, compare=True)
    name: Optional[str] = field(repr=True)


@dataclass
class IgBusContainer(BaseModel):
    """
    A class representing the media container.

    Refer: https://developers.facebook.com/docs/instagram-api/reference/ig-container
    """

    id: Optional[str] = field(repr=True, compare=True)
    status: Optional[str] = field()
    status_code: Optional[str] = field()
