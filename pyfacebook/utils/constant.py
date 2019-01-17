"""
    This is different fields for to retrieve data from Facebook graph API.
"""

PAGE_FIELDS = [
    'id', 'about', 'category', 'category_list', 'checkins', 'cover',
    'description', 'description_html', 'emails', 'engagement', 'fan_count',
    'global_brand_page_name', 'global_brand_root_id', 'link', 'name', 'phone',
    'page_about_story', 'username', 'verification_status', 'website'
]

POST_BASIC_FIELDS = [
    'id', 'attachments', 'caption', 'child_attachments', 'created_time', 'description',
    'full_picture', 'icon', 'link', 'message', 'name',
    'permalink_url', 'picture', 'shares', 'source', 'status_type',
    'type', 'updated_time',
    'comments.summary(true).limit(0)',
    'reactions.summary(true).limit(0)',
]

POST_REACTIONS_FIELD = [
    'reactions.summary(true).limit(0)',
    'reactions.type(LIKE).limit(0).summary(total_count).as(like)',
    'reactions.type(LOVE).limit(0).summary(total_count).as(love)',
    'reactions.type(WOW).limit(0).summary(total_count).as(wow)',
    'reactions.type(HAHA).limit(0).summary(total_count).as(haha)',
    'reactions.type(SAD).limit(0).summary(total_count).as(sad)',
    'reactions.type(ANGRY).limit(0).summary(total_count).as(angry)',
    'reactions.type(THANKFUL).limit(0).summary(total_count).as(thankful)'
]
