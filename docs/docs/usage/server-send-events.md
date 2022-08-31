## Introduction

Server-Sent Events allows you to receive real-time updates for live video comments and reactions. It uses the Server-Sent Events (SSE) web standard to send real-time, continuous data streams to browser clients, once an initial client connection has been established.

More detail you can see [docs](https://developers.facebook.com/docs/graph-api/server-sent-events).

Here, we give a simple example to show how to implement it by this library.

## How to use

### Custom data handler

You need override `on_data` method to handle the data.

As follows, we just print the real data from facebook.

```python
import json

from pyfacebook import ServerSentEventAPI

class MyEvent(ServerSentEventAPI):
    def on_data(self, data):
        raw_data: str = data.decode()

        data = json.loads(raw_data[5:])
        print(f"Comment Data: {data}")

```

### Connect the server

Then you can connect the facebook server to get pushed data.

```python
event_api = MyEvent(access_token="Your access token")
event_api.live_comments(
    live_video_id="ID for the live video",
    fields="from{id,name},message"
)

# output
# Comment Data: {'id': '611384697233703_2059142704258615', 'created_time': '2022-08-31T10:03:00+0000', 'from': {'id': '100621042235323', 'name': 'HeyJoklena'}, 'message': 'hello sse', 'object': {'description': 'section 1, 1, 2', 'updated_time': '2022-08-31T10:03:00+0000', 'id': '611384697233703'}}
# Comment Data: {'id': '611384697233703_1165171867677765', 'created_time': '2022-08-31T10:03:29+0000', 'from': {'id': '100621042235323', 'name': 'HeyJoklena'}, 'message': 'sse is nice', 'object': {'description': 'section 1, 1, 2', 'updated_time': '2022-08-31T10:03:00+0000', 'id': '611384697233703'}}
```

Now if the live video has new comment, you will see the comment output.
