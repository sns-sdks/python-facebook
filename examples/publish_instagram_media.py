"""
This is an example for instagram business account to publish an image media.

Refer: https://developers.facebook.com/docs/instagram-api/reference/ig-user/media
"""

import os

from pyfacebook import GraphAPI

ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")  # Your Access Token
INSTAGRAM_BUSINESS_ID = os.environ.get(
    "INSTAGRAM_BUSINESS_ID"
)  # Your instagram business id

api = GraphAPI(access_token=ACCESS_TOKEN)

data = api.post_object(
    object_id=INSTAGRAM_BUSINESS_ID,
    connection="media",
    params={
        "image_url": "https://example.com/example.png",  # replace with your image url.
        "caption": "Image by api",  # replace with your caption for the media.
    },
)
print(data)
# {'id': '17952987976782688'}
# Get your container id.
container_id = data["id"]

# Then publish the container.
publish_data = api.post_object(
    object_id=INSTAGRAM_BUSINESS_ID,
    connection="media_publish",
    params={
        "creation_id": container_id,
    },
)
print(publish_data)
# Now will get the published media id.
# {'id': '17899702154554435'}
