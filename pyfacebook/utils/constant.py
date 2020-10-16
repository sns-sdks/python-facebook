"""
    This is default fields for to retrieve data from Facebook graph API.

    Updated at: v5.0
"""

FB_PAGE_FIELDS = {
    "id", "about", "can_checkin", "category", "category_list", "checkins",
    "contact_address", "cover", "current_location", "description", "description_html",
    "display_subtext", "emails", "engagement", "fan_count", "founded", "general_info",
    "global_brand_page_name", "global_brand_root_id", "link", "name",
    "phone", "picture", "rating_count", "single_line_address", "start_info",
    "talking_about_count", "username", "verification_status", "website",
    "were_here_count", "whatsapp_number",
}

FB_POST_ATTACHMENTS = {
    "description", "description_tags", "media", "media_type", "target", "title",
    "type", "unshimmed_url", "url", "subattachments"
}

FB_POST_BASIC_FIELDS = {
    "id", "attachments{{{}}}".format(",".join(FB_POST_ATTACHMENTS)),
    "created_time", "full_picture", "icon", "message",
    "permalink_url", "picture", "shares", "status_type", "updated_time",
    # filter stream return all comments count
    # refer: https://developers.facebook.com/docs/graph-api/reference/page-post/comments/
    "comments.filter(stream).summary(true).limit(0)",
    "reactions.summary(true).limit(0)",
}

FB_POST_REACTIONS_FIELD = {
    "reactions.summary(true).limit(0)",
    "reactions.type(LIKE).limit(0).summary(total_count).as(like)",
    "reactions.type(LOVE).limit(0).summary(total_count).as(love)",
    "reactions.type(WOW).limit(0).summary(total_count).as(wow)",
    "reactions.type(HAHA).limit(0).summary(total_count).as(haha)",
    "reactions.type(SAD).limit(0).summary(total_count).as(sad)",
    "reactions.type(ANGRY).limit(0).summary(total_count).as(angry)",
    "reactions.type(THANKFUL).limit(0).summary(total_count).as(thankful)"
}

FB_COMMENT_BASIC_FIELDS = {
    "id", "attachment", "created_time", "like_count",
    "can_comment", "can_like", "comment_count",
    "from", "message", "permalink_url",
}

FB_PAGE_PICTURE_TYPE = {
    "small", "normal", "album", "large", "square"
}

FB_VIDEO_BASIC_FIELDS = {
    "id", "title", "description",
    "created_time", "updated_time",
    # common connections
    "likes.summary(true).limit(0)", "comments.summary(true).limit(0)"
}

FB_VIDEO_CAPTION_BASIC_FIELDS = {
    "create_time", "is_auto_generated", "is_default",
    "locale", "locale_name", "uri",
}

FB_ALBUM_BASIC_FIELDS = {
    "id", "created_time", "count",
    "name", "description",
    # common connections
    "likes.summary(true).limit(0)",
    "comments.summary(true).limit(0)",
}

FB_PHOTO_BASIC_FIELDS = {
    "id", "created_time", "name", "link",
    # common connections
    "likes.summary(true).limit(0)",
}

# ====================================================
# Follows is Instagram Professional fields to get data
# ====================================================

INSTAGRAM_USER_FIELD = {
    "biography", "id", "ig_id",
    "followers_count", "follows_count", "media_count",
    "name", "profile_picture_url", "username", "website",
}

INSTAGRAM_MEDIA_CHILDREN_PUBLIC_FIELD = {
    "id", "media_type", "media_url", "permalink", "timestamp", "username"
}

INSTAGRAM_MEDIA_CHILDREN_OWNER_FIELD = INSTAGRAM_MEDIA_CHILDREN_PUBLIC_FIELD.union({
    "ig_id", "owner", "shortcode", "thumbnail_url",
})

INSTAGRAM_MEDIA_FIELD = {
    "caption", "comments_count", "id",
    "like_count", "media_type", "media_url",
    "permalink", "timestamp", "username"
}

INSTAGRAM_MEDIA_PUBLIC_FIELD = INSTAGRAM_MEDIA_FIELD.union({
    "children{{{}}}".format(",".join(INSTAGRAM_MEDIA_CHILDREN_PUBLIC_FIELD))
})

INSTAGRAM_MEDIA_OWNER_FIELD = INSTAGRAM_MEDIA_FIELD.union({
    "children{{{}}}".format(",".join(INSTAGRAM_MEDIA_CHILDREN_OWNER_FIELD)),
    "ig_id", "is_comment_enabled",
    "owner", "shortcode", "thumbnail_url"
})

INSTAGRAM_STORY_FIELD = {
    "id", "ig_id", "caption",
    "media_type", "media_url", "owner", "permalink",
    "shortcode", "thumbnail_url", "timestamp", "username"
}

INSTAGRAM_COMMENT_FIELD = {
    "hidden", "id", "like_count", "media",
    "text", "timestamp", "user", "username"
}

INSTAGRAM_REPLY_FIELD = INSTAGRAM_COMMENT_FIELD

INSTAGRAM_HASHTAG_FIELD = {
    "id", "name"
}

INSTAGRAM_HASHTAG_MEDIA_FIELD = {
    "caption", "children{id,media_type,media_url,permalink}",
    "comments_count", "id", "like_count", "media_type",
    "media_url", "permalink",
}

INSTAGRAM_MENTION_COMMENT_FIELD = {
    "id", "like_count", "media{{{}}}".format(",".join(INSTAGRAM_MEDIA_FIELD)),
    "text", "timestamp",
}

# =====================================================
# Follows is Instagram Basic display fields to get data
# =====================================================
INSTAGRAM_BASIC_USER_FIELD = [
    "account_type", "id", "media_count", "username"
]

INSTAGRAM_BASIC_MEDIA_CHILDREN_FIELD = {
    "id", "media_type", "media_url", "permalink",
    "thumbnail_url", "timestamp", "username"
}

INSTAGRAM_BASIC_MEDIA_FIELD = {
    "caption", "id", "media_type", "media_url", "permalink",
    "thumbnail_url", "timestamp", "username", "children{{{}}}".format(",".join(INSTAGRAM_BASIC_MEDIA_CHILDREN_FIELD))
}
