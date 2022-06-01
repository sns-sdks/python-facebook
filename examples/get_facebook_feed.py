"""
    This is an example for page get recent 50 feeds

    Refer: https://developers.facebook.com/docs/graph-api/reference/page/feed#read
"""
import json
import os

from pyfacebook import GraphAPI

APP_ID = os.environ.get("APP_ID")  # Your App ID
APP_SECRET = os.environ.get("APP_SECRET")  # Your App secret
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")  # Your Access Token


def handler(page_id):
    api = GraphAPI(app_id=APP_ID, app_secret=APP_SECRET, access_token=ACCESS_TOKEN)
    feed = api.get_full_connections(
        object_id=page_id,
        connection="feed",
        count=50,
        limit=25,
        fields="id,message,create_time",
    )
    with open(f"./{page_id}.json", "w+") as f:
        json.dump(feed, f)


if __name__ == "__main__":
    handler(page_id="meta")
