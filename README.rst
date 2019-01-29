Python Facebook

A Python wrapper around for Facebook Common API.

.. image:: https://travis-ci.org/MerleLiuKun/python-facebook.svg?branch=master
    :target: https://travis-ci.org/MerleLiuKun/python-facebook
    :alt: Build Status

.. image:: http://codecov.io/github/MerleLiuKun/python-facebook/coverage.svg?branch=master
    :target: http://codecov.io/github/MerleLiuKun/python-facebook
    :alt: Codecov


======
THANKS
======

This project structure is base on `Python-Twitter <https://github.com/bear/python-twitter>`_.

Thanks a lot for Python-Twitter Developers.


============
Introduction
============

Library provides a service to easy use Facebook web api.


=====
Using
=====

---
API
---

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

To fetch a list facebook page's posts data::

    In [6]: api.get_posts(username='facebook')
    Out[6]:
    [Post(ID=20531316728_10158033357426729, permalink_url=https://www.facebook.com/20531316728/posts/10158033357426729/),
     Post(ID=2031316728_10157806010111729, permalink_url=https://www.facebook.com/20531316728/posts/10157806010111729/),
     Post(ID=20531316728_1877006505687069, permalink_url=https://www.facebook.com/facebook/videos/1877006505687069/),
     Post(ID=20531316728_267444427196392, permalink_url=https://www.facebook.com/facebook/videos/267444427196392/)]

To fetch point post info::

    In [7]: res = api.get_post_info(post_id='20531316728_10157619579661729')

    In [8]: res
    Out[8]: Post(ID=20531316728_10157619579661729, permalink_url=https://www.facebook.com/20531316728/posts/10157619579661729/)

    In [9]: res.comments
    Out[9]: 1016


----
TODO
----

Now. You can get page info and page post info.

doing:

- publish
- more.