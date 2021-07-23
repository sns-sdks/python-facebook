"""
    This is default fields for to retrieve data from Facebook graph API.
"""

# =============================================
# Follows is Facebook graph fields to get data
# =============================================

USER_PUBLIC_FIELDS = [
    "id",
    "first_name",
    "last_name",
    "middle_name",
    "name",
    "name_format",
    "picture",
    "short_name",
]

PAGE_PUBLIC_FIELDS = [
    "id",
    "about",
    "category",
    "category_list",
    "cover",
    "description",
    "description_html",
    "display_subtext",
    "emails",
    "engagement",
    "fan_count",
    "global_brand_page_name",
    "global_brand_root_id",
    "link",
    "name",
    "phone",
    "picture",
    "username",
    "verification_status",
    "website",
]

GROUP_PUBLIC_FIELDS = [
    "id",
    "name",
    "description",
    "created_time",
    "member_count",
]

ATTACHMENT_FIELDS = [
    "description",
    "description_tags",
    "media",
    "media_type",
    "target",
    "title",
    "type",
    "unshimmed_url",
    "url",
    "subattachments",
]

POST_PUBLIC_FIELDS = [
    "id",
    f"attachments{{{','.join(ATTACHMENT_FIELDS)}}}",
    "created_time",
    "full_picture",
    "icon",
    "message",
    "message_tags",
    "permalink_url",
    "picture",
    "shares",
    "status_type",
    "updated_time",
]

POST_CONNECTIONS_SUMMERY_FIELDS = [
    "comments.filter(stream).summary(true).limit(0)",
    "reactions.summary(true).limit(0)",
    "reactions.type(LIKE).limit(0).summary(total_count).as(like)",
    "reactions.type(LOVE).limit(0).summary(total_count).as(love)",
    "reactions.type(WOW).limit(0).summary(total_count).as(wow)",
    "reactions.type(HAHA).limit(0).summary(total_count).as(haha)",
    "reactions.type(SAD).limit(0).summary(total_count).as(sad)",
    "reactions.type(ANGRY).limit(0).summary(total_count).as(angry)",
]

PHOTO_PUBLIC_FIELDS = ["id", "created_time", "name", "updated_time", "link"]

ALBUM_PUBLIC_FIELDS = ["id", "created_time", "count", "name", "updated_time", "link"]

VIDEO_PUBLIC_FIELDS = [
    "id",
    "created_time",
    "description",
    "title",
    "published",
    "length",
    "permalink_url",
    "updated_time",
]

LIVE_VIDEO_PUBLIC_FIELDS = [
    "id",
    "creation_time",
    "description",
    "embed_html",
    "live_views",
    "permalink_url",
    "secure_stream_url",
    "status",
    "stream_url",
    "title",
]
