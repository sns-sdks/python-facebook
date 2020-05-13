"""
    This show how to get facebook page public posts.
"""

import json

from pyfacebook import Api

# Use version 5+, Call API need app secret proof. So need provide your app secret.
# If not have, you can just use version 4.0.
APP_ID = "Your APP ID"
APP_SECRET = "Your APP SECRET"

ACCESS_TOKEN = "Your Access Token"


def get_posts(page_username: str):
    api = Api(
        app_id=APP_ID,
        app_secret=APP_SECRET,
        long_term_token=ACCESS_TOKEN,
    )
    data = api.get_page_posts(
        page_id=page_username,
        since_time="2020-05-01",
        count=None,
        limit=100,
        return_json=True,
    )
    return data


def processor():
    page_username = "WHO"
    data = get_posts(page_username)
    with open("wto_posts.json", 'w') as f:
        json.dump(data, f)


if __name__ == "__main__":
    processor()
