Python Facebook

A Python wrapper around for Facebook Common API.

.. image:: https://travis-ci.org/sns-sdks/python-facebook.svg?branch=master
    :target: https://travis-ci.org/sns-sdks/python-facebook
    :alt: Build Status

.. image:: https://readthedocs.org/projects/python-facebook-api/badge/?version=latest
    :target: https://python-facebook-api.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://codecov.io/gh/sns-sdks/python-facebook/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/sns-sdks/python-facebook
    :alt: Codecov

.. image:: https://img.shields.io/pypi/v/python-facebook-api.svg
    :target: https://pypi.org/project/python-facebook-api
    :alt: PyPI




README: `English <https://github.com/MerleLiuKun/python-facebook/blob/master/README.rst>`_ | `中文 <https://github.com/MerleLiuKun/python-facebook/blob/master/README-zh.rst>`_

======
THANKS
======

This project structure is base on `Python-Twitter <https://github.com/bear/python-twitter>`_.

Thanks a lot for Python-Twitter Developers.


============
Introduction
============

Library provides a service to easy use Facebook Graph API.

It currently includes the use of ``Facebook`` and ``Instagram Business`` product data.

==========
Installing
==========

You can install this library from ``pypi``::

    $pip install --upgrade python-facebook-api
    ✨🍰✨

This is name is ugly. but the ``python-facebook`` is exists and it not update long time.

=============
Documentation
=============

You can view the latest ``python-facebook`` documentation at: https://python-facebook-api.readthedocs.io/en/latest/

Also view the full ``Facebook Graph API`` docs at: https://developers.facebook.com/docs/graph-api/

=====
Using
=====

------------
Facebook API
------------

The API is exposed via the ``pyfacebook.Api`` class.

This API need facebook OAUTH keys to get any data from facebook. And the facebook app is required first.

If you not have facebook app, you can view `Facebook Developers <https://developers.facebook.com/>`_ to apply one. If you
have app. you can do as follows example.

All the OAuth Doc to see `Facebook Access Token <https://developers.facebook.com/docs/facebook-login/access-tokens/#usertokens>`_

To create an instance of the ``pyfacebook.Api`` with two different methods. Use only long term token or provide app
id, app secret and short token::

    In [1]: import pyfacebook

    In [2]: api = pyfacebook.Api(app_id='your app id',   # use the second method.
       ...:                      app_secret='your app secret',
       ...:                      short_token='your short token')

    In [3]: api = pyfacebook.Api(long_term_token='your long term access token')

To see if your config well::

    In [4]: api.get_token_info(return_json=True)
    Out[4]:
    {'data': {'app_id': 'xxx',
    'type': 'USER',
    'application': 'xxx',
    'data_access_expires_at': 1555231532,
    'expires_at': 1553244944,
    'is_valid': True,
    'issued_at': 1548060944,
    'scopes': ['public_profile'],
    'user_id': 'xxx'}}

To fetch one facebook page's public data::

    In [5]: api.get_page_info(page_id='20531316728')  # you can make return_json True to see more fields
    Out[5]: Page(ID=20531316728, username=facebook)

Because facebook graph api limit `Page Feed <https://developers.facebook.com/docs/graph-api/reference/v4.0/page/feed>`_.
Use public token only can get approximately 600 ranked, published posts per year.
If you want to get page's all posts. you need query the ``/{page_id}/published_posts`` endpoint with ``page's access token``.
First get page's access token (Must the page's administer give the permission ``manage_pages``.)::

    In [6]: access_token = api.exchange_insights_token(token='user token', page_id='page id')
    Out[6]: 'page access token'

Now. You can use page access token to get page's all posts::

    In [7]: api.get_published_posts(username='facebook', access_token='page access token')
    Out[7]: [Post...]

Use the page access token, you can also get the posts who has tagged your page. Like this::

    In [8]: api.get_tagged_posts(username='facebook', access_token='page access token')
    Out[8]: [Post...]


To fetch a list facebook page's public posts data (Not full)::

    In [9]: api.get_posts(username='facebook')
    Out[9]:
    [Post(ID=20531316728_10158033357426729, permalink_url=https://www.facebook.com/20531316728/posts/10158033357426729/),
     Post(ID=2031316728_10157806010111729, permalink_url=https://www.facebook.com/20531316728/posts/10157806010111729/),
     Post(ID=20531316728_1877006505687069, permalink_url=https://www.facebook.com/facebook/videos/1877006505687069/),
     Post(ID=20531316728_267444427196392, permalink_url=https://www.facebook.com/facebook/videos/267444427196392/)]

To fetch point post info::

    In [10]: res = api.get_post_info(post_id='20531316728_10157619579661729')

    In [11]: res
    Out[11]: Post(ID=20531316728_10157619579661729, permalink_url=https://www.facebook.com/20531316728/posts/10157619579661729/)

    In [12]: res.comments
    Out[12]: 1016


To fetch pointed object(post,picture and so on)'s comments data::

    In [13]: res = api.get_comments(object_id='20531316728_10157619579661729', summary=True)
    In [14]: res
    Out[14]:
    ([Comment(ID=10157619579661729_10157621841846729,created_time=2018-08-16T13:01:09+0000),
      Comment(ID=10157619579661729_10157621842496729,created_time=2018-08-16T13:01:31+0000),
      Comment(ID=10157619579661729_10157621842611729,created_time=2018-08-16T13:01:34+0000),
      Comment(ID=10157619579661729_10157621842701729,created_time=2018-08-16T13:01:37+0000),
      Comment(ID=10157619579661729_10157621843186729,created_time=2018-08-16T13:01:52+0000),
      Comment(ID=10157619579661729_10157621843316729,created_time=2018-08-16T13:01:55+0000),
      Comment(ID=10157619579661729_10157621843376729,created_time=2018-08-16T13:01:58+0000),
      Comment(ID=10157619579661729_10157621843721729,created_time=2018-08-16T13:02:11+0000),
      Comment(ID=10157619579661729_10157621843771729,created_time=2018-08-16T13:02:13+0000),
      Comment(ID=10157619579661729_10157621843836729,created_time=2018-08-16T13:02:14+0000)],
     CommentSummary(order=chronological,total_count=987))
    In [15]: res[1]
    Out[15]: CommentSummary(order=chronological,total_count=987)
    In [16]: res.as_json_string()
    Out[16]: '{"can_comment": true, "order": "chronological", "total_count": 987}'


-------------
Instagram API
-------------

At present, the business Account of Instagram can be accessed through the API provided by Facebook.

That is ``pyfacebook.Instagram Api`` can only get data of the business Account on Instagram platform.

The business Account is the Account who associates ``Instagram`` account with ``Facebook`` page.

If you want to search other's business account basic info and medias.
You can use methods as follows::

    - discovery_user: retrieve user basic data
    - discovery_user_medias: retrieve user medias data

.. note::
   Use discovery only support search by instagram user name.

If you have other business account's access token with relative permissions.
You can use remain methods with the access token to retrieve this account's data::

    - get_user_info
    - get_medias
    - get_media_info
    - get_comments
    - get_comment_info
    - get_replies
    - get_reply_info

Initialization of the ``pyfacebook.InstagramApi`` instance requires the provision of user authorization ``Token`` for App with ``Instagram`` privileges, and also need an available ``Instagram`` business account.

For detailed documentation, please consult:

- `Instagram Developer <https://developers.facebook.com/products/instagram/>`_
- `Instagram Graph API <https://developers.facebook.com/docs/instagram-api>`_

Usage example:

Similar to ``Facebook Api``, the ``InstagramApi`` instance can also be initialized in two ways, but requires an additional ``instagram_business_id`` parameter::

    # Use temporary tokens and App secret
    In [1] import pyfacebook

    In [2] api = pyfacebook.InstagramApi(
       ...     app_id = 'App ID',
       ...     app_secret='App secret',
       ...     short_token='your temporary token',
       ...     instagram_business_id='your Instagram business id')

    # Use long-term tokens
    In [3] api = pyfacebook.InstagramApi(
       ...     long_term_token='your long term access token',
       ...     instagram_business_id='your Instagram business id')


Get other account information by discovery::

    In [3]: api.discovery_user(username='jaychou')
    Out[3]: User(ID=17841405792603923, username=jaychou)

    In [4]: api.discovery_user(username='jaychou', return_json=True)
    Out[4]:
    {'website': 'https://youtu.be/HK7SPnGSxLM',
     'biography': 'https://www.facebook.com/jay/',
     'profile_picture_url': 'https://scontent.xx.fbcdn.net/v/t51.2885-15/21147825_124638651514445_4540910313213526016_a.jpg?_nc_cat=1&_nc_oc=AQl4VclkS9_O1iwa1KDetuR89g6yHkTHZOJZ2-kemhQcnFb1kIPzPBXsUydf1To2ZeM&_nc_ht=scontent.xx&oh=a86a0b98abb5294266d550095ecd7621&oe=5E20C7FA',
     'ig_id': 5951385086,
     'follows_count': 81,
     'media_count': 516,
     'username': 'jaychou',
     'id': '17841405792603923',
     'followers_count': 5237768,
     'name': 'Jay Chou 周杰倫'}

Get other account medias by discovery(default return 10)::

    In [5]: api.discovery_user_medias(username='jaychou')
    Out[5]:
    [Media(ID=17871925513478048, link=https://www.instagram.com/p/B382ojgHemq/),
     Media(ID=17861378536535135, link=https://www.instagram.com/p/B36TG8AHbGd/),
     Media(ID=17862568840534713, link=https://www.instagram.com/p/B33k7llnd_S/),
     Media(ID=18002681875267830, link=https://www.instagram.com/p/B319fbuHXIt/),
     Media(ID=17873056222479764, link=https://www.instagram.com/p/B31duvoH26O/),
     Media(ID=17906467621371226, link=https://www.instagram.com/p/B3xCYNonlqn/),
     Media(ID=17850201154639505, link=https://www.instagram.com/p/B3ufD-JH3a5/),
     Media(ID=17855908660588183, link=https://www.instagram.com/p/B3q-bMuHvnl/),
     Media(ID=18108170392062569, link=https://www.instagram.com/p/B3olnLxnRsy/),
     Media(ID=17900244466380038, link=https://www.instagram.com/p/B3oQVpEHM3Q/)]

Get account information by his access token::

    In [6]: api.get_user_info(user_id='account id', access_token='access token')
    Out[6]: User(ID=17841406338772941, username=ikroskun)

Get account medias by his access token::

    In [7]: api.get_medias(user_id='account id', access_token='access token')
    Out[7]:
    [Media(ID=18075344632131157, link=https://www.instagram.com/p/B38X8BzHsDi/),
     Media(ID=18027939643230671, link=https://www.instagram.com/p/B38Xyp6nqsS/),
     Media(ID=17861821972334188, link=https://www.instagram.com/p/BuGD8NmF4KI/),
     Media(ID=17864312515295083, link=https://www.instagram.com/p/BporjsCF6mt/),
     Media(ID=17924095942208544, link=https://www.instagram.com/p/BoqBgsNl5qT/),
     Media(ID=17896189813249754, link=https://www.instagram.com/p/Bop_Hz5FzyL/),
     Media(ID=17955956875141196, link=https://www.instagram.com/p/Bn-35GGl7YM/),
     Media(ID=17970645226046242, link=https://www.instagram.com/p/Bme0cU1giOH/)]

Get account media comments by his access token::

    In [8]: api.get_comments(media_id='media id', access_token='access token')
    Out[8]: [Comment(ID=18008567518250255,timestamp=2019-10-23T02:10:32+0000)]

And so on...

====
TODO
====

------------
Now features
------------

Facebook Api:

- Page Info.
- Page Picture Info.
- Feed Info (public posts, published posts, tagged posts).
- Comment Info.

Instagram Api:

- Other business account info and media.
- Authorized business account info
- Authorized account medias
- Authorized account comments
- Authorized account replies

----
TODO
----

- Acquisition of Insights Data
- publish