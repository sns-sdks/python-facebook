"""
    models for instagram platform
"""

from attr import attrs, attrib
from typing import Dict, List, Optional, Any

from .base import BaseModel
from .._compat import str


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

    def __attrs_post_init__(self):
        if self.media is not None and isinstance(self.media, dict):
            self.media = IgProMedia.new_from_json_dict(self.media)


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
    replies = attrib(default=None, type=Optional[Dict], repr=False)

    def __attrs_post_init__(self):
        IgProBaseComment.__attrs_post_init__(self)
        if self.replies is not None and isinstance(self.replies, dict):
            replies = self.replies.get("data", [])
            self.replies = [IgProReply.new_from_json_dict(item) for item in replies]


@attrs
class MediaCommon(BaseModel):
    """
    Some common fields for media or story
    """
    id = attrib(default=None, type=Optional[str])
    ig_id = attrib(default=None, type=Optional[int], repr=False)
    caption = attrib(default=None, type=Optional[str], repr=False)
    comments_count = attrib(default=None, type=Optional[int], repr=False)
    like_count = attrib(default=None, type=Optional[int], repr=False)
    media_product_type = attrib(default=None, type=Optional[str], repr=False)
    media_type = attrib(default=None, type=Optional[str], repr=False)
    media_url = attrib(default=None, type=Optional[str], repr=False)
    owner = attrib(default=None, type=Optional[IgProUser], repr=False)
    permalink = attrib(default=None, type=Optional[str])
    shortcode = attrib(default=None, type=Optional[str], repr=False)
    thumbnail_url = attrib(default=None, type=Optional[str], repr=False)
    timestamp = attrib(default=None, type=Optional[str], repr=False)
    username = attrib(default=None, type=Optional[str], repr=False)
    video_title = attrib(default=None, type=Optional[str], repr=False)


@attrs
class IgProMedia(MediaCommon):
    """
    A class representing the Instagram media info.

    Refer: https://developers.facebook.com/docs/instagram-api/reference/media
    """
    is_comment_enabled = attrib(default=None, type=Optional[bool], repr=False)

    # connections
    comments = attrib(default=None, type=Optional[Dict], repr=False)
    children = attrib(default=None, type=Optional[Dict], repr=False)

    def __attrs_post_init__(self):
        if self.children is not None and isinstance(self.children, dict):
            children = self.children.get("data", [])
            self.children = [IgProMediaChildren.new_from_json_dict(item) for item in children]
        if self.comments is not None and isinstance(self.comments, dict):
            comments = self.comments.get("data", [])
            self.comments = [IgProComment.new_from_json_dict(item) for item in comments]


@attrs
class IgProStory(MediaCommon):
    """
    A class representing the Instagram story info. It's similar to media but not have some fields.

    Refer: https://developers.facebook.com/docs/instagram-api/reference/ig-user/stories
    """
    pass


@attrs
class IgProHashtag(BaseModel):
    """
    A class representing the Instagram hashtag info.

    Refer: https://developers.facebook.com/docs/instagram-api/reference/hashtag
    """
    id = attrib(default=None, type=Optional[str])
    name = attrib(default=None, type=Optional[str])


@attrs
class IgProInsightValue(BaseModel):
    """
    A class representing the Instagram insight value info.

    Refer: https://developers.facebook.com/docs/instagram-api/guides/insights#getting-account-metrics
    """
    value = attrib(default=None, type=Optional[Any])
    end_time = attrib(default=None, type=Optional[str])


@attrs
class IgProInsight(BaseModel):
    """
    A class representing the Instagram insight info.

    Refer: https://developers.facebook.com/docs/instagram-api/guides/insights#getting-account-metrics
    """

    id = attrib(default=None, type=Optional[str], repr=False)
    name = attrib(default=None, type=Optional[str])
    period = attrib(default=None, type=Optional[str])
    title = attrib(default=None, type=Optional[str], repr=False)
    description = attrib(default=None, type=Optional[str], repr=False)
    values = attrib(default=None, type=Optional[List[Dict]], repr=False)

    def __attrs_post_init__(self):
        if self.values is not None and isinstance(self.values, List):
            values = self.values
            self.values = [IgProInsightValue.new_from_json_dict(item) for item in values]


@attrs
class IgProContainer(BaseModel):
    """
    A class representing the Instagram container info.

    Refer: https://developers.facebook.com/docs/instagram-api/reference/ig-container
    """

    id = attrib(default=None, type=Optional[str])
    status_code = attrib(default=None, type=Optional[str])
    status = attrib(default=None, type=Optional[str], repr=False)


@attrs
class IgProPublishLimitConfig(BaseModel):
    """
    A class representing the Instagram publish limit config

    Refer: https://developers.facebook.com/docs/instagram-api/reference/ig-user/content_publishing_limit#fields
    """

    quota_total = attrib(default=None, type=Optional[int])
    quota_duration = attrib(default=None, type=Optional[int])


@attrs
class IgProPublishLimit(BaseModel):
    """
    A class representing the Instagram publish limit

    Refer: https://developers.facebook.com/docs/instagram-api/reference/ig-user/content_publishing_limit#fields
    """

    quota_usage = attrib(default=None, type=Optional[int])
    config = attrib(default=None, type=Optional[IgProPublishLimitConfig], repr=False)
