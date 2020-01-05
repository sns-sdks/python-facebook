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


README: `English <README.rst>`_ | `中文 <README-zh.rst>`_

======
THANKS
======

Inspired by `Python-Twitter <https://github.com/bear/python-twitter>`_.

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


=============
Documentation
=============

You can view the latest ``python-facebook`` documentation at: https://python-facebook-api.readthedocs.io/en/latest/

Also view the full ``Facebook Graph API`` docs at: https://developers.facebook.com/docs/graph-api/

And full ``Instagram Graph API`` docs at: https://developers.facebook.com/docs/instagram-api/

=============================
Base-Usage-Facebook Graph API
=============================

The API is exposed via the ``pyfacebook.Api`` class.

To get data, you need have a facebook app first.
You can get more information about create, apply permissions for app at `App docs <https://developers.facebook.com/docs/apps>`_.

-----------
Initial Api
-----------

Facebook has different type access tokens. You can use different access token to get different data.

1. User Access Token
#. App Access Token
#. Page Access Token
#. Client Token (library not support)

You can see the docs `access-token`_ to get more information.

If you want to get user access token by authorize. You can follows the docs `authorization-manually`_ to initial the api.

If you just want to use app access token to get some public data. You can initial an api as follows::

    In [2]: api = Api(app_id="your app id", app_secret="your app secret", application_only_auth=True)
    In [3]: api.get_token_info()
    Out[3]: AccessToken(app_id='id', application='app name', user_id=None)

If you have a short-lived token you can initial an api as follows::

    In [4]: api = Api(app_id="your app id", app_secret="your app secret", short_token="short-lived token")
    In [5]: api.get_token_info()
    Out[5]: AccessToken(app_id='id', application='app name', user_id='token user id')

If you have a long term token you can initial an api as follows(Just provide only ``long_term_token`` parameter enough. but for security need provide with app credentials)::

    In [6]: api = Api(app_id="your app id", app_secret="your app secret", long_term_token="long-term token")
    In [7]: api.get_token_info()
    Out[7]: AccessToken(app_id='id', application='app name', user_id='token user id')

    # this need token have additional manage_pages permission.
    In [8]: api = Api(long_term_token="long-term token")

the different initial with parameter ``short_token`` or ``long_term_token`` is short token will auto exchange a long term token inside.

--------
Get Data
--------

You can get a facebook page information by follows methods.

To fetch one facebook page's public data::

    In [3]: api.get_page_info(username='facebookapp')
    Out[3]: Page(id='20531316728', name='Facebook', username='facebookapp')


To fetch multi page by one request, you can pass the page username list or page id list with the ``ids`` parameter as follows::

    In [4]: api.get_pages_info(ids=["20531316728", "nba"])
    Out[4]:
    {'20531316728': Page(id='20531316728', name='Facebook', username='facebookapp'),
     'nba': Page(id='8245623462', name='NBA', username='nba')}

There have multi methods to retrieve one page's posts data.

>>> api.get_page_feeds()
>>> api.get_page_posts()
>>> api.get_page_published_posts()
>>> api.get_page_tagged_posts()

Page feeds can get feed of posts (including status updates) and links published by this page, or by others on this page. You can call with follows::

    In [5]: api.get_page_feeds(page_id="20531316728",count=2)
    Out[5]:
    [Post(id='20531316728_587455038708591', permalink_url='https://www.facebook.com/facebookapp/videos/587455038708591/'),
     Post(id='20531316728_10159023836696729', permalink_url='https://www.facebook.com/20531316728/posts/10159023836696729/')]

Page posts can only get the posts that were published by this page::

    In [6]: api.get_page_posts(page_id="20531316728",count=2)
    Out[6]:
    [Post(id='20531316728_587455038708591', permalink_url='https://www.facebook.com/facebookapp/videos/587455038708591/'),
     Post(id='20531316728_10159023836696729', permalink_url='https://www.facebook.com/20531316728/posts/10159023836696729/')]


Because facebook graph api limit `Page Feed <https://developers.facebook.com/docs/graph-api/reference/v5.0/page/feed>`_.
Use public token only can get approximately 600 ranked, published posts per year.

So if you want to get page's all posts or posts which tagged the page. you need use method ``get_page_published_posts``, and this need a page access token with permission ``manage_pages``.

You can use authorization to get that page access token. Just follows docs `authorization-manually`_.
Then can get all published posts::

    In [7]: api.get_published_posts(username='facebookapp', access_token='page access token')
    Out[7]: [Post...]

You can get tagged posts::

    In [8]: api.get_tagged_posts(username='facebookapp', access_token='page access token')
    Out[8]: [Post...]


If you also have the post id, you can get post detail info by follows methods.

To fetch a post info::

    In [9]: api.get_post_info(post_id="20531316728_587455038708591")
    Out[9]: Post(id='20531316728_587455038708591', permalink_url='https://www.facebook.com/facebookapp/videos/587455038708591/')

To fetch multi posts by one requests::

    In [10]: api.get_posts_info(ids=["20531316728_587455038708591", "20531316728_10159023836696729"])
    Out[10]:
    {'20531316728_587455038708591': Post(id='20531316728_587455038708591', permalink_url='https://www.facebook.com/facebookapp/videos/587455038708591/'),
     '20531316728_10159023836696729': Post(id='20531316728_10159023836696729', permalink_url='https://www.facebook.com/20531316728/posts/10159023836696729/')}

You can get comments data by the object(post,page and so on) id::

    In [11]: api.get_comments_by_object(object_id="20531316728_587455038708591", count=2)
    Out[11]:
    ([Comment(id='587455038708591_587460942041334', can_like=True, can_comment=True, comment_count=2, like_count=1),
      Comment(id='587455038708591_587464298707665', can_like=True, can_comment=True, comment_count=2, like_count=14)],
     CommentSummary(total_count=392, can_comment=True))

If you already have the comment id, you can get comment details info with follows methods.

To fetch one comment info::

    In [12]: api.get_comment_info(comment_id="587455038708591_587460942041334")
    Out[12]: Comment(id='587455038708591_587460942041334', comment_count=2, like_count=1)

To fetch multi comment info by one request::

    In [13]: api.get_comments_info(ids=["587455038708591_587460942041334", "587455038708591_587464298707665"])
    Out[13]:
    {'587455038708591_587460942041334': Comment(id='587455038708591_587460942041334', comment_count=2, like_count=1),
     '587455038708591_587464298707665': Comment(id='587455038708591_587464298707665', comment_count=2, like_count=14)}



You can get the page's profile picture by follow methods.

To fetch one page picture::

    In [14]: api.get_picture(page_id="20531316728")
    Out[14]: ProfilePictureSource(url='https://scontent.xx.fbcdn.net/v/t1.0-1/p100x100/58978526_10158354585751729_7411073224387067904_o.png?_nc_cat=1&_nc_oc=AQmaFO7eND-DVRoArrQLUZVDpmemw8nMPmHJWvoCyXId_MKLLHQdsS8UbTOX4oaEfeQ&_nc_ht=scontent.xx&oh=128f57c4dc65608993af62b562d92d84&oe=5E942420', height=100, width=100)


To fetch multi page picture::

    In [15]: api.get_pictures(ids=["20531316728", "nba"])
    Out[15]:
    {'20531316728': ProfilePictureSource(url='https://scontent.xx.fbcdn.net/v/t1.0-1/p100x100/58978526_10158354585751729_7411073224387067904_o.png?_nc_cat=1&_nc_oc=AQmaFO7eND-DVRoArrQLUZVDpmemw8nMPmHJWvoCyXId_MKLLHQdsS8UbTOX4oaEfeQ&_nc_ht=scontent.xx&oh=128f57c4dc65608993af62b562d92d84&oe=5E942420', height=100, width=100),
     'nba': ProfilePictureSource(url='https://scontent.xx.fbcdn.net/v/t1.0-1/p100x100/81204460_10158199356848463_5727214464013434880_n.jpg?_nc_cat=1&_nc_oc=AQmcent57E-a-923C_VVpiX26nGqKDodImY1gsiu7h1czDmcpLHXR8D5hIh9g9Ao3wY&_nc_ht=scontent.xx&oh=1656771e6c11bd03147b69ee643238ba&oe=5E66450C', height=100, width=100)}



==============================
Base-Usage-Instagram Graph API
==============================

Instagram Graph API allows to get `instagram Professional accounts <https://help.instagram.com/502981923235522>`_ data.

-----------
Initial Api
-----------

As similar to facebook graph api. This api can initial by multi methods. But only can use user access token, and need your instagram business id.

If you want to get user access token by authorize. You can follows the docs `authorization-manually`_ to initial the api.

If you have a short-lived token you can initial an api as follows::

    In [2]: api = IgProApi(app_id="your app id", app_secret="your app secret", short_token="short-lived token", instagram_business_id="17841406338772941")
    In [3]: api.get_token_info()
    Out[3]: AccessToken(app_id='id', application='app name', user_id="token user id")

If you have a long term token you can initial an api as follows(Just provide only ``long_term_token`` parameter enough. but for security need provide with app credentials)::

    In [4]: api = IgProApi(app_id="your app id", app_secret="your app secret", long_term_token="long-lived token")
    In [5]: api.get_token_info()
    Out[5]: AccessToken(app_id='id', application='app name', user_id='token user id')

--------
Get Data
--------

If you want to search other's business account basic info and medias.
You can use methods as follows::

    - discovery_user: retrieve user basic data
    - discovery_user_medias: retrieve user medias data

.. note::
   Use discovery only support search by instagram user name.

Retrieve other user info by username::

    In [6]: api.discovery_user(username="facebook")
    Out[6]: IgProUser(id='17841400455970028', name='Facebook', username='facebook')

Retrieve other user medias by username::

    In [7]: api.discovery_user_medias(username="facebook", count=2)
    Out[7]:
    [IgProMedia(comments=None, id='17859633232647524', permalink='https://www.instagram.com/p/B6jje2UnoH8/'),
     IgProMedia(comments=None, id='18076151185161297', permalink='https://www.instagram.com/p/B6ji-PZH2V1/')]


Get your account info::

    In [10]: api.get_user_info(user_id="your instagram business id")
    Out[10]: IgProUser(id='17841406338772941', name='LiuKun', username='ikroskun')


Get your medias::

    In [11]: api.get_user_medias(user_id=api.instagram_business_id, count=2)
    Out[11]:
    [IgProMedia(comments=None, id='18075344632131157', permalink='https://www.instagram.com/p/B38X8BzHsDi/'),
     IgProMedia(comments=None, id='18027939643230671', permalink='https://www.instagram.com/p/B38Xyp6nqsS/')]


If you already have some medias id, you can get media info as follows methods.

To fetch a post info::

    In [12]: api.get_media_info(media_id="18075344632131157")
    Out[12]: IgProMedia(comments=None, id='18075344632131157', permalink='https://www.instagram.com/p/B38X8BzHsDi/')


To fetch multi medias by one requests::

    In [13]: api.get_medias_info(media_ids=["18075344632131157", "18027939643230671"])
    Out[13]:
    {'18075344632131157': IgProMedia(comments=None, id='18075344632131157', permalink='https://www.instagram.com/p/B38X8BzHsDi/'),
     '18027939643230671': IgProMedia(comments=None, id='18027939643230671', permalink='https://www.instagram.com/p/B38Xyp6nqsS/')}

Get comments for media::

    In [16]: api.get_comments_by_media(media_id="17955956875141196", count=2)
    Out[16]:
    [IgProComment(id='17862949873623188', timestamp='2020-01-05T05:58:47+0000'),
     IgProComment(id='17844360649889631', timestamp='2020-01-05T05:58:42+0000')]


If you already have some comments id, you can get comment details info as follows methods.

To fetch a comment info::

    In [17]: api.get_comment_info(comment_id="17862949873623188")
    Out[17]: IgProComment(id='17862949873623188', timestamp='2020-01-05T05:58:47+0000')

To fetch multi comments by one requests::

    In [18]: api.get_comments_info(comment_ids=["17862949873623188", "17844360649889631"
    ...: ])
    Out[18]:
    {'17862949873623188': IgProComment(id='17862949873623188', timestamp='2020-01-05T05:58:47+0000'),
     '17844360649889631': IgProComment(id='17844360649889631', timestamp='2020-01-05T05:58:42+0000')}

Get replies for a comments::

    In [19]: api.get_replies_by_comment("17984127178281340", count=2)
    Out[19]:
    [IgProReply(id='18107567341036926', timestamp='2019-10-15T07:06:09+0000'),
     IgProReply(id='17846106427692294', timestamp='2019-10-15T07:05:17+0000')]

If you already have some replies id, you can get replies details info as follows methods.

To fetch a reply info::

    In [20]: api.get_reply_info(reply_id="18107567341036926")
    Out[20]: IgProReply(id='18107567341036926', timestamp='2019-10-15T07:06:09+0000')

To fetch multi replies info by one requests::

    In [21]: api.get_replies_info(reply_ids=["18107567341036926", "17846106427692294"])
    Out[21]:
    {'18107567341036926': IgProReply(id='18107567341036926', timestamp='2019-10-15T07:06:09+0000'),
     '17846106427692294': IgProReply(id='17846106427692294', timestamp='2019-10-15T07:05:17+0000')}


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


.. _access-token: https://developers.facebook.com/docs/facebook-login/access-tokens
.. _authorization-manually: https://developers.facebook.com/docs/facebook-login/manually-build-a-login-flow