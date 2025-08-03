## Introduction

You may use the Threads API to enable people to create and publish content on a person’s behalf on Threads, and to
display those posts within your app solely to the person who created it.

## How to use

Just like the base `Graph API`.

The following code snippet shows how to perform an OAuth flow with the Threads API:

```python
from pyfacebook import ThreadsGraphAPI

api = ThreadsGraphAPI(
    app_id="Your app id",
    app_secret="Your app secret",
    oauth_flow=True,
    redirect_uri="Your callback domain",
    scope=["threads_basic", "threads_content_publish", "threads_read_replies", "threads_manage_replies",
           "threads_manage_insights"]
)

# Got authorization url
api.get_authorization_url()
# https://threads.net/oauth/authorize?response_type=code&client_id=app_id&redirect_uri=https%3A%2F%2Fexample.com%2Fcallback&scope=threads_basic%2Cthreads_content_publish%2Cthreads_read_replies%2Cthreads_manage_replies%2Cthreads_manage_insights&state=PyFacebook

# Once the user has authorized your app, you will get the redirected URL.
# like `https://example.com/callback?code=AQBZzYhLZB&state=PyFacebook#_`
token = await api.exchange_user_access_token(response="Your response url")
print(token)
# {'access_token': 'access_token', 'user_id': 12342412}
```

After those steps, you can use the `api` object to call the Threads API.

For example:

```python
await api.get_object(object_id="me", fields=["id"])

# {'id': '12342412'}
```
