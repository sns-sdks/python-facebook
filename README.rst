Python Facebook

A Python wrapper around for Facebook Common API.

.. image:: https://travis-ci.org/MerleLiuKun/python-facebook.svg?branch=master
    :target: https://travis-ci.org/MerleLiuKun/python-facebook
    :alt: Build Status

.. image:: https://readthedocs.org/projects/python-facebook-api/badge/?version=latest
    :target: https://python-facebook-api.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://codecov.io/gh/MerleLiuKun/python-facebook/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/MerleLiuKun/python-facebook
    :alt: Codecov

.. image:: https://img.shields.io/pypi/v/python-facebook-api.svg
    :target: https://pypi.org/project/python-facebook-api
    :alt: PyPI

.. image:: https://img.shields.io/pypi/pyversions/python-facebook-api.svg
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


Initialization of the ``pyfacebook.InstagramApi`` instance requires the provision of user authorization ``Token`` for App with ``Instagram`` privileges, and also need an available ``Instagram`` business account.

For detailed documentation, please consult:

- `Instagram Developer <https://developers.facebook.com/products/instagram/>`_
- `Business Discovery API <https://developers.facebook.com/docs/instagram-api/business-discovery>`_

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


Get basic information about a user::

    In [12]: api.get_user_info(username='jaychou')
    Out[12]: User(ID=17841405792603923, username=jaychou)

    In [13]: api.get_user_info(username='jaychou', return_json=True)
    Out[13]:
    {'business_discovery': {'biography': 'https://www.facebook.com/jay/',
      'id': '17841405792603923',
      'ig_id': 5951385086,
      'followers_count': 3303887,
      'follows_count': 50,
      'media_count': 319,
      'name': 'Jay Chou 周杰倫',
      'profile_picture_url': 'https://scontent.xx.fbcdn.net/v/t51.2885-15/21147825_124638651514445_4540910313213526016_a.jpg?_nc_cat=1&_nc_ht=scontent.xx&oh=9a84c5d93df1cf7fb600d21efc87f983&oe=5CE45FFA',
      'username': 'jaychou',
      'website': 'https://youtu.be/MAjY8mCTXWk'},
      'id': '17841406338772941'}

Mass access to a user's posts(Get nearly 50 by default)::

    In [3]: api.get_medias(username='jaychou')
    Out[3]:
        [Media(ID=17852512102358859, link=https://www.instagram.com/p/BuKth42Hpsm/),
         Media(ID=17914455160286660, link=https://www.instagram.com/p/BuILzrcnljS/),
         Media(ID=18038180344016282, link=https://www.instagram.com/p/BuDAlT0n0kq/),
         Media(ID=18000503476161727, link=https://www.instagram.com/p/Bt6SyHmnGyn/),
         Media(ID=17863710898325821, link=https://www.instagram.com/p/Bt49wLUnTaO/),
         Media(ID=17857272226339334, link=https://www.instagram.com/p/Bt4n5Q5ncKa/),
         Media(ID=17854413100345353, link=https://www.instagram.com/p/Bt33bRznSNo/),
         Media(ID=18033275821031206, link=https://www.instagram.com/p/Bt2bECmn0R_/),
         Media(ID=18033135562032465, link=https://www.instagram.com/p/Bt1sedfnnqD/),
         Media(ID=17933504032265945, link=https://www.instagram.com/p/BtzPPiGn2gE/),
         Media(ID=18017672368106762, link=https://www.instagram.com/p/Btt-rKqHGLH/),
         Media(ID=18033213532062450, link=https://www.instagram.com/p/BtkVolVnhXu/),
         Media(ID=18031391875036047, link=https://www.instagram.com/p/BtjkEmxH7gR/),
         Media(ID=18029417977062683, link=https://www.instagram.com/p/Btd5jPvHQUm/).....]


Get information about a post(This API is available only for posts on the current Instagram business account and is not available to others)::

    In [5]: api.get_media_info(media_id='17861821972334188')
    Out[5]: Media(ID=17861821972334188, link=https://www.instagram.com/p/BuGD8NmF4KI/)

----
TODO
----

Now features:

Facebook Api:

- Page Info.
- Page Picture Info.
- Feed Info (public posts, published posts, tagged posts).
- Comment Info.

Instagram Api:

- Business user info.
- Medias info

TODO:

- Acquisition of Insights Data
- publish