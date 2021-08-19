"""
    Model classes for instagram business.
"""

from dataclasses import dataclass
from typing import List, Optional, Union

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
class IgBusCommentResponse(BaseModel):
    """
    A class representing the comments response.

    Refer: https://developers.facebook.com/docs/instagram-api/reference/ig-media/comments
    """

    data: List[IgBusComment] = field(repr=True)
    paging: Optional[Paging] = field(repr=True)


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


@dataclass
class IgBusPublishLimitConfig(BaseModel):
    """
    A class representing the content publish limit config.
    """

    quota_total: Optional[int] = field(repr=True)
    quota_duration: Optional[int] = field()


@dataclass
class IgBusPublishLimit(BaseModel):
    """
    A class representing the content publish limit.

    Refer: https://developers.facebook.com/docs/instagram-api/reference/ig-user/content_publishing_limit
    """

    config: Optional[IgBusPublishLimitConfig] = field(repr=True)
    quota_usage: Optional[int] = field(repr=True)


@dataclass
class IgBusPublishLimitResponse(BaseModel):
    """
    A class representing the content publish limit response.

    Refer: https://developers.facebook.com/docs/instagram-api/reference/ig-user/content_publishing_limit
    """

    data: List[IgBusPublishLimit] = field(repr=True)


@dataclass
class IgBusInsightValue(BaseModel):
    """
    A class representing the Instagram insight value info.

    Refer: https://developers.facebook.com/docs/instagram-api/reference/ig-user/insights
    """

    value: Optional[Union[int, dict]] = field(repr=True)
    end_time: Optional[str] = field(repr=True)


@dataclass
class IgBusInsight(BaseModel):
    """
    A class representing the Instagram insight.

    Refer: https://developers.facebook.com/docs/instagram-api/reference/ig-user/insights
    """

    id: Optional[str] = field()
    name: Optional[str] = field(repr=True)
    period: Optional[str] = field(repr=True)
    title: Optional[str] = field()
    description: Optional[str] = field()
    values: Optional[List[IgBusInsightValue]] = field()


@dataclass
class IgBusInsightsResponse(BaseModel):
    """
    A class representing the Instagram insights response.

    Refer: https://developers.facebook.com/docs/instagram-api/reference/ig-user/insights
    """

    data: List[IgBusInsight] = field(repr=True)
    paging: Optional[Paging] = field()


@dataclass
class IgBusDiscoveryUserResponse(BaseModel):
    """
    A class representing the response for discovery user.

    Refer: https://developers.facebook.com/docs/instagram-api/reference/ig-user/business_discovery#sample-response
    """

    business_discovery: Optional[IgBusUser] = field(repr=True)
    id: Optional[str] = field(repr=True)


@dataclass
class IgBusDiscoveryUserMedia(BaseModel):
    media: Optional[IgBusMediaResponse] = field(repr=True)
    id: Optional[str] = field()


@dataclass
class IgBusDiscoveryUserMediaResponse(BaseModel):
    """
    A class representing the response for discovery user.

    Refer: https://developers.facebook.com/docs/instagram-api/reference/ig-user/business_discovery#sample-response
    """

    business_discovery: Optional[IgBusDiscoveryUserMedia] = field(repr=True)
    id: Optional[str] = field(repr=True)


@dataclass
class IgBusMentionedCommentResponse(BaseModel):
    """
    A class representing the response for mentioned comment.

    Refer: https://developers.facebook.com/docs/instagram-api/reference/ig-user/mentioned_comment
    """

    mentioned_comment: Optional[IgBusReply] = field(repr=True)
    id: Optional[str] = field(repr=True)


@dataclass
class IgBusMentionedMediaResponse(BaseModel):
    """
    A class representing the response for mentioned media.

    Refer: https://developers.facebook.com/docs/instagram-api/reference/ig-user/mentioned_media
    """

    mentioned_media: Optional[IgBusMedia] = field(repr=True)
    id: Optional[str] = field(repr=True)


@dataclass
class IgBusHashtagsResponse(BaseModel):
    """
    A class representing the hashtag.

    Refer: https://developers.facebook.com/docs/instagram-api/reference/ig-user/recently_searched_hashtags
    """

    data: List[IgBusHashtag] = field(repr=True)
    paging: Optional[Paging] = field(repr=True)
