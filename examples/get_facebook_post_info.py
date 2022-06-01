"""
    This is an example for get post detail by FacebookApi class.

    Refer: https://developers.facebook.com/docs/graph-api/reference/pagepost
"""

import os

from pyfacebook import FacebookApi

APP_ID = os.environ.get("APP_ID")  # Your App ID
APP_SECRET = os.environ.get("APP_SECRET")  # Your App secret
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")  # Your Access Token


def handler(post_id):
    api = FacebookApi(app_id=APP_ID, app_secret=APP_SECRET, access_token=ACCESS_TOKEN)
    post = api.post.get_info(
        post_id=post_id,
        fields="id,message,created_time,full_picture,status_type,updated_time",
    )
    print(f"ID: {post.id}")
    print(f"Time: {post.created_time}")
    print(f"Data: {post.to_json()}")
    return True


if __name__ == "__main__":
    handler(post_id="19292868552_371106181716390")
