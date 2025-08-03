## Introduction

This library provides a simpler service to help developers access Facebook's Graph API.

Here, we will help to use base class `GraphAPI` to get data from Facebook.

## How to use

### Initial API

Once you have access token, you can use it to initial the `GraphAPI` class.

As for the [Security docs](https://developers.facebook.com/docs/graph-api/security/). You may need provide your app
credential to generate `appsecret_proof` to verify Graph API calls.

```python
from pyfacebook import GraphAPI

api = GraphAPI(
    app_id="Your app id",
    app_secret="Your app secret",
    access_token="Your access token",
)
```

The [access token](https://developers.facebook.com/docs/facebook-login/access-tokens/) can be `User Access Token`
, `App Access Token` or `Page Access Token`, and this depending on the data type what you need.

After initial API. Now we can access facebook api with this API.

### Methods

You can get data of an object, such as page,post,photo and so on.

```python
await api.get_object(object_id="108824017345866")
# {'name': 'Meta', 'id': '108824017345866'}
```

You can get the data of some objects.

```python
await api.get_objects(ids="108824017345866,20531316728")
# {'108824017345866': {'name': 'Meta', 'id': '108824017345866'}, '20531316728': {'name': 'Facebook App', 'id': '20531316728'}}
```

If you want to get data for an object's edge. For example, a User node can have photos connected to it, and a Photo node
can have comments connected to it.

```python
await api.get_connection(object_id="20531316728", connection="posts")
# {'data': [{'created_time': '2021-11-26T20:01:40+0000', 'message': "Do Black Friday right with the #BuyBlack Friday Show! For the finale, host Elaine Welteroth will be talking with Sir Darius Brown, the owner of Beaux and Paws. We'll also have special guests D-Nice, Iddris Sandu., and Jaden Smith! Join this fun shop-a-thon in partnership with Meta for Business \n\nShop directly on [Beaux and Paws] Facebook page so you can get your pet looking proper.  fb.me/buyblackfri", 'story': 'Facebook App was live.', 'id': '20531316728_3789869301238646'}], 'paging': {'cursors': {'before': 'before', 'after': 'after'}, 'next': 'https://graph.facebook.com/v12.0/20531316728/posts?access_token=access_token&limit=1&after=after'}}
```

If you want to get all data for an object's edge. Auto paging inside.

```python
await api.get_full_connections(object_id="20531316728", connection="posts")
# {'data': [{'created_time': '2021-11-26T20:01:40+0000', 'message': "Do Black Friday right with the #BuyBlack Friday Show! For the finale, host Elaine Welteroth will be talking with Sir Darius Brown, the owner of Beaux and Paws. We'll also have special guests D-Nice, Iddris Sandu., and Jaden Smith! Join this fun shop-a-thon in partnership with Meta for Business \n\nShop directly on [Beaux and Paws] Facebook page so you can get your pet looking proper.  fb.me/buyblackfri", 'story': 'Facebook App was live.', 'id': '20531316728_3789869301238646'}], 'paging': {'cursors': {'before': 'before', 'after': 'after'}, 'next': 'https://graph.facebook.com/v12.0/20531316728/posts?access_token=access_token&limit=1&after=after'}}
```

If you have permissions to publish data. you can use `post` to create data.

```python
await api.post_object(object_id="2121008874780932_404879271158877", connection="comments",
                data={"message": "Comment by the api"})
# {'id': '404879271158877_405046241142180'}
```

If you have permissions to delete data.

```python
await api.delete_object(object_id="404879271158877_405046241142180")
# {'success': True}
```
