"""
    This is an example for facebook page publish a post.

    Refer: https://developers.facebook.com/docs/graph-api/reference/page/feed#publish
"""

import os

from pyfacebook import GraphAPI

APP_ID = os.environ.get("APP_ID")  # Your App ID
APP_SECRET = os.environ.get("APP_SECRET")  # Your App secret
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")  # Your Access Token with the target page


def publish_simple_posts(page_id):
    api = GraphAPI(app_id=APP_ID, app_secret=APP_SECRET, access_token=ACCESS_TOKEN)

    data = api.post_object(
        object_id=page_id,
        connection="feed",
        params={
            "fields": "id,message,created_time,from",
        },
        data={"message": "This is a test message by api"},
    )
    print(data)
    # {'id': 'xxx', 'message': 'This is a test message by api', 'created_time': '2022-06-01T03:49:36+0000', 'from': {'name': 'xx', 'id': 'xxxx'}}
    return True


if __name__ == "__main__":
    publish_simple_posts(page_id="meta")
