"""
    A demo for sample streaming api.
"""

import json
import logging

from pyfacebook import ServerSentEventAPI

access_token = "Your access token"
live_video_id = "ID for live video"
debug = False

if debug:
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)


class MyEvent(ServerSentEventAPI):
    def on_data(self, data):
        raw_data: str = data.decode()

        data = json.loads(raw_data[5:])
        print(f"Comment Data: {data}")


def handler():
    stream_api = MyEvent(access_token=access_token)
    stream_api.live_comments(
        live_video_id=live_video_id,
        comment_rate="one_per_two_seconds",
        fields="id,attachment,created_time,from{id,name},message,object",
    )


if __name__ == "__main__":
    handler()
