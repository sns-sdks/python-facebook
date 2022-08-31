"""
    Tests for ServerSentEventAPI
"""
import random
from unittest.mock import patch

import pytest
import requests
import responses
from responses import matchers

from pyfacebook import ServerSentEventAPI


class MyEvent(ServerSentEventAPI):
    count, max_count = 0, 5

    def on_data(self, data):
        super().on_data(data=data)
        self.count += 1
        if self.count >= self.max_count:
            self.disconnect()


@responses.activate
def test_live_reactions():
    live_video_id = "380505100913581"
    reactions_data = (
        b'data: {"reaction_stream":[{"key":"LIKE","value":2},{"key":"LOVE","value":1}]}'
    )

    def callback(request):
        s = random.randint(1, 2)
        if s == 1:
            return 200, {}, reactions_data
        else:
            return 200, {}, b": ping"

    req_kwargs = {"stream": True}
    responses.add(
        responses.CallbackResponse(
            responses.GET,
            url=f"https://streaming-graph.facebook.com/{live_video_id}/live_reactions",
            callback=callback,
            content_type="text/event-stream",
        ),
        match=[matchers.request_kwargs_matcher(req_kwargs)],
    )

    stream_api = MyEvent(access_token="token")
    stream_api.live_reactions(live_video_id=live_video_id)

    assert not stream_api.running


@responses.activate
def test_live_comments():
    live_video_id = "380505100913581"
    comments_data = b'data: {"id":"610800597327576_364546219223792","created_time":"2022-08-31T09:09:39+0000","from":{"id":"413140042878187","name":"Kun Liu"},"message":"wow","object":{"description":"section 1, 1","updated_time":"2022-08-31T09:09:20+0000","id":"610800597327576"}}'

    def callback(request):
        s = random.randint(1, 2)
        if s == 1:
            return 200, {}, comments_data
        else:
            return 200, {}, b" "

    req_kwargs = {"stream": True}
    responses.add(
        responses.CallbackResponse(
            responses.GET,
            url=f"https://streaming-graph.facebook.com/{live_video_id}/live_comments",
            callback=callback,
            content_type="text/event-stream",
        ),
        match=[matchers.request_kwargs_matcher(req_kwargs)],
    )

    stream_api = MyEvent(access_token="token")
    stream_api.live_comments(live_video_id=live_video_id)

    assert stream_api.count == 5


@responses.activate
@patch("time.sleep", return_value=None)
def test_stream_retry_connect(patched_time_sleep):
    live_video_id = "123456"
    responses.add(
        responses.GET,
        url=f"https://streaming-graph.facebook.com/{live_video_id}/live_reactions",
        status=400,
        stream=True,
    )

    stream_api = MyEvent(access_token="token")
    stream_api.live_reactions(live_video_id=live_video_id)
