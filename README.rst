Python Facebook

A Python wrapper for the Facebook Common API.

.. image:: https://github.com/sns-sdks/python-facebook/workflows/Test/badge.svg
    :target: https://github.com/sns-sdks/python-facebook/actions
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

Library provides a service to easily use Facebook Graph API.

It currently includes the use of ``Facebook``,  ``Instagram Business``, and ``Instagram Basic Display`` product data.

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

And full ``Instagram Basic Display API`` docs at: https://developers.facebook.com/docs/instagram-basic-display-api/

=============================
Base-Usage-Facebook Graph API
=============================

The API is exposed via the ``pyfacebook.Api`` class.

To get data, you need to have a facebook app first.
You can get more information about create, apply permissions for app at `App docs <https://developers.facebook.com/docs/apps>`_.

Also, you can get some examples for this library at `Example folder <examples>`_.

-----------
Initial Api
-----------

Facebook has different types of access tokens. You can use different access tokens to get different data.

1. User Access Token
#. App Access Token
#. Page Access Token
#. Client Token (library not support)

You can see the docs `access-token`_ to get more information.

If you want to get user access token by authorize. You can follow the docs `authorization-manually`_ to initial the api.

If you just want to use app access token to get some public data. You can initial an api as follows::

    In [2]: api = Api(app_id="your app id", app_secret="your app secret", application_only_auth=True)
    In [3]: api.get_token_info()
    Out[3]: AccessToken(app_id='id', application='app name', user_id=None)

If you have a short-lived token you can initial an api as follows::

    In [4]: api = Api(app_id="your app id", app_secret="your app secret", short_token="short-lived token")
    In [5]: api.get_token_info()
    Out[5]: AccessToken(app_id='id', application='app name', user_id='token user id')

If you have a long term token you can initial an api as follows (Just provide only ``long_term_token`` parameter enough. but for security need provide with app credentials)::

    In [6]: api = Api(app_id="your app id", app_secret="your app secret", long_term_token="long-term token")
    In [7]: api.get_token_info()
    Out[7]: AccessToken(app_id='id', application='app name', user_id='token user id')

    # this need token have additional manage_pages permission.
    In [8]: api = Api(long_term_token="long-term token")

the difference between initialize with parameter ``short_token`` or ``long_term_token`` is that short token will auto exchange a long term token inside.

Facebook rate limit is very vague, it is related to the number of users of your app. So the library provides the custom sleep times in requests.
You can only set parameter ``sleep_on_rate_limit`` with ``True`` to let api sleep two seconds between two requests.
Or you can set parameter ``sleep_seconds_mapping`` with a dict that contains your custom data. ex::

    In [9]: mapping = {10: 2, 20: 5, 50: 20, 70: 30}  # key is api limit reached percent and value is seconds to sleep.
    In [10]: api = Api(
        ...:     app_id="your app id", app_secret="your app secret", long_term_token="long-term token",
        ...:     sleep_on_rate_limit=True, sleep_seconds_mapping=mapping
        ...:)


--------
Get Data
--------

You can get a facebook page information by the following methods.

To fetch one facebook page's public data::

    In [3]: api.get_page_info(username='facebookapp')
    Out[3]: Page(id='20531316728', name='Facebook', username='facebookapp')


To fetch multi page by one request, you can pass the page username list or page id list with the ``ids`` parameter as follows::

    In [4]: api.get_pages_info(ids=["20531316728", "nba"])
    Out[4]:
    {'20531316728': Page(id='20531316728', name='Facebook', username='facebookapp'),
     'nba': Page(id='8245623462', name='NBA', username='nba')}

There are multiple methods to retrieve one page's posts data.

>>> api.get_page_feeds()
>>> api.get_page_posts()
>>> api.get_page_published_posts()
>>> api.get_page_tagged_posts()

Page feeds can get feed of posts (including status updates) and links published by this page, or by others on this page. You can call with the following::

    In [5]: api.get_page_feeds(page_id="20531316728",count=2)
    Out[5]:
    [Post(id='20531316728_587455038708591', permalink_url='https://www.facebook.com/facebookapp/videos/587455038708591/'),
     Post(id='20531316728_10159023836696729', permalink_url='https://www.facebook.com/20531316728/posts/10159023836696729/')]

Page posts can only get the posts that were published by this page::

    In [6]: api.get_page_posts(page_id="20531316728",count=2)
    Out[6]:
    [Post(id='20531316728_587455038708591', permalink_url='https://www.facebook.com/facebookapp/videos/587455038708591/'),
     Post(id='20531316728_10159023836696729', permalink_url='https://www.facebook.com/20531316728/posts/10159023836696729/')]


Because of facebook graph api limit `Page Feed <https://developers.facebook.com/docs/graph-api/reference/v5.0/page/feed>`_.
Using public token can only get approximately 600 ranked, published posts per year.

So if you want to get all of a page's posts or posts which tagged the page. you need use method ``get_page_published_posts``, and this needs a page's access token with permission ``manage_pages``.

You can use authorization to get that page access token. Just follows docs `authorization-manually`_.
Then you can get all published posts::

    In [7]: api.get_published_posts(username='facebookapp', access_token='page access token')
    Out[7]: [Post...]

You can get tagged posts::

    In [8]: api.get_tagged_posts(username='facebookapp', access_token='page access token')
    Out[8]: [Post...]


If you also have the post id, you can get post detail info by the following methods.

To fetch a post info::

    In [9]: api.get_post_info(post_id="20531316728_587455038708591")
    Out[9]: Post(id='20531316728_587455038708591', permalink_url='https://www.facebook.com/facebookapp/videos/587455038708591/')

To fetch multi posts by one requests::

    In [10]: api.get_posts_info(ids=["20531316728_587455038708591", "20531316728_10159023836696729"])
    Out[10]:
    {'20531316728_587455038708591': Post(id='20531316728_587455038708591', permalink_url='https://www.facebook.com/facebookapp/videos/587455038708591/'),
     '20531316728_10159023836696729': Post(id='20531316728_10159023836696729', permalink_url='https://www.facebook.com/20531316728/posts/10159023836696729/')}

You can get comments data by the object(post, page and so on) id::

    In [11]: api.get_comments_by_object(object_id="20531316728_587455038708591", count=2)
    Out[11]:
    ([Comment(id='587455038708591_587460942041334', can_like=True, can_comment=True, comment_count=2, like_count=1),
      Comment(id='587455038708591_587464298707665', can_like=True, can_comment=True, comment_count=2, like_count=14)],
     CommentSummary(total_count=392, can_comment=True))

If you already have the comment id, you can get comment details info with the following methods.

To fetch one comment info::

    In [12]: api.get_comment_info(comment_id="587455038708591_587460942041334")
    Out[12]: Comment(id='587455038708591_587460942041334', comment_count=2, like_count=1)

To fetch multi comment info by one request::

    In [13]: api.get_comments_info(ids=["587455038708591_587460942041334", "587455038708591_587464298707665"])
    Out[13]:
    {'587455038708591_587460942041334': Comment(id='587455038708591_587460942041334', comment_count=2, like_count=1),
     '587455038708591_587464298707665': Comment(id='587455038708591_587464298707665', comment_count=2, like_count=14)}



You can get the page's profile picture by the following methods.

To fetch one page picture::

    In [14]: api.get_picture(page_id="20531316728")
    Out[14]: ProfilePictureSource(url='https://scontent.xx.fbcdn.net/v/t1.0-1/p100x100/58978526_10158354585751729_7411073224387067904_o.png?_nc_cat=1&_nc_oc=AQmaFO7eND-DVRoArrQLUZVDpmemw8nMPmHJWvoCyXId_MKLLHQdsS8UbTOX4oaEfeQ&_nc_ht=scontent.xx&oh=128f57c4dc65608993af62b562d92d84&oe=5E942420', height=100, width=100)


To fetch multi page picture::

    In [15]: api.get_pictures(ids=["20531316728", "nba"])
    Out[15]:
    {'20531316728': ProfilePictureSource(url='https://scontent.xx.fbcdn.net/v/t1.0-1/p100x100/58978526_10158354585751729_7411073224387067904_o.png?_nc_cat=1&_nc_oc=AQmaFO7eND-DVRoArrQLUZVDpmemw8nMPmHJWvoCyXId_MKLLHQdsS8UbTOX4oaEfeQ&_nc_ht=scontent.xx&oh=128f57c4dc65608993af62b562d92d84&oe=5E942420', height=100, width=100),
     'nba': ProfilePictureSource(url='https://scontent.xx.fbcdn.net/v/t1.0-1/p100x100/81204460_10158199356848463_5727214464013434880_n.jpg?_nc_cat=1&_nc_oc=AQmcent57E-a-923C_VVpiX26nGqKDodImY1gsiu7h1czDmcpLHXR8D5hIh9g9Ao3wY&_nc_ht=scontent.xx&oh=1656771e6c11bd03147b69ee643238ba&oe=5E66450C', height=100, width=100)}

You can get videos data by the object(page, user...) id::

    In [16]: api.get_videos_by_object("ikaroskunlife", fields=["id", "title", "description"], count=None, limit=20)
    Out[16]:
    [Video(id='969222676905304', created_time=None, description='冬日'),
     Video(id='210174653594254', created_time=None, description='Snowing'),
     Video(id='674270653053120', created_time=None, description='Visible')]

If you already have the id of videos, you can get more info by the following methods::

    In [17]: api.get_video_info("969222676905304")
    Out[17]: Video(id='969222676905304', created_time='2020-09-12T09:53:06+0000', description='冬日')

    In [18]: api.get_videos(ids=["210174653594254", "674270653053120"])
    Out[18]:
    {'210174653594254': Video(id='210174653594254', created_time='2020-03-31T08:13:14+0000', description='Snowing'),
     '674270653053120': Video(id='674270653053120', created_time='2019-09-02T06:13:17+0000', description='Visible')}

You can get albums data by the object(page, user...) id::

    In[19]: api.get_albums_by_object("instagram", count=20, limit=15)
    Out[19]:
    [Album(id='372558296163354', created_time='2012-10-29T19:46:35+0000', name='时间线照片'),
     Album(id='623202484432266', created_time='2014-04-12T15:28:26+0000', name='手机上传')...]

If you already have the id of album, you can get more info by the following methods::

    In[20]: api.get_album_info("372558296163354")
    Out[20]: Album(id='372558296163354', created_time='2012-10-29T19:46:35+0000', name='时间线照片')

    In[21]: api.get_albums(ids="372558296163354,623202484432266")
    Out[21]:
    {'372558296163354': Album(id='372558296163354', created_time='2012-10-29T19:46:35+0000', name='时间线照片'),
     '623202484432266': Album(id='623202484432266', created_time='2014-04-12T15:28:26+0000', name='手机上传')}

You can get photos data by the object(page, album, user...) id::

    In [22]: api.get_photos_by_object("372558296163354", count=10, limit=5)
    Out[22]:
    [Photo(id='3293405020745319', created_time='2020-09-10T19:11:01+0000', name='Roller skating = Black joy for Travis Reynolds. 🖤\n\nWatch our IGTV to catch some good vibes and see his 🔥🔥🔥 tricks. \n\n#ShareBlackStories\n\nhttps://www.instagram.com/tv/CE9xgF3jwS_/'),
     Photo(id='3279789248773563', created_time='2020-09-06T16:23:17+0000', name='#HelloFrom Los Glaciares National Park, Argentina 👏👏👏\n\nhttps://www.instagram.com/p/CEzSoQNMdfH/'),
     Photo(id='3276650595754095', created_time='2020-09-05T16:52:54+0000', name=None)...]

If you already have the id of photos, you can get more info by the following methods::

    In [4]: api.get_photo_info("3293405020745319")
    Out[4]: Photo(id='3293405020745319', created_time='2020-09-10T19:11:01+0000', name='Roller skating = Black joy for Travis Reynolds. 🖤\n\nWatch our IGTV to catch some good vibes and see his 🔥🔥🔥 tricks. \n\n#ShareBlackStories\n\nhttps://www.instagram.com/tv/CE9xgF3jwS_/')

    In [5]: api.get_photos(ids=["3279789248773563", "3276650595754095"])
    Out[5]:
    {'3279789248773563': Photo(id='3279789248773563', created_time='2020-09-06T16:23:17+0000', name='#HelloFrom Los Glaciares National Park, Argentina 👏👏👏\n\nhttps://www.instagram.com/p/CEzSoQNMdfH/'),
     '3276650595754095': Photo(id='3276650595754095', created_time='2020-09-05T16:52:54+0000', name=None)}


You can get live videos data by the object(page, user...) id::

    In [6]: api.get_live_videos_by_object(object_id="2121008874780932", limit=10, count=2)
    Out[6]:
    [LiveVideo(id='2814245952123884', permalink_url='/IkaroskunLife/videos/710393869909608/'),
     LiveVideo(id='2809188389296307', permalink_url='/IkaroskunLife/videos/706216360286730/')]

If you already have the id of live videos, you can get more info by the following methods::

    In [7]: api.get_live_video_info(live_video_id="2814245952123884")
    Out[7]: LiveVideo(id='2814245952123884', permalink_url='/IkaroskunLife/videos/710393869909608/')

    In [8]: api.get_live_videos(ids=["2814245952123884", "2809188389296307"])
    Out[8]:
    {'2814245952123884': LiveVideo(id='2814245952123884', permalink_url='/IkaroskunLife/videos/710393869909608/'),
     '2809188389296307': LiveVideo(id='2809188389296307', permalink_url='/IkaroskunLife/videos/706216360286730/')}

Same as get live video input stream data.

==============================
Base-Usage-Instagram Graph API
==============================

Instagram Graph API allows you to get `instagram Professional accounts <https://help.instagram.com/502981923235522>`_ data.

-----------
Initial Api
-----------

As similar to facebook graph api. This api can be initialized by multiple methods. But can only use user access token, and needs your instagram business id.

If you want to get user access token by authorize. You can follows the docs `authorization-manually`_ to initialize the api.

If you have a short-lived token you can initialize an api as follows::

    In [2]: api = IgProApi(app_id="your app id", app_secret="your app secret", short_token="short-lived token", instagram_business_id="17841406338772941")
    In [3]: api.get_token_info()
    Out[3]: AccessToken(app_id='id', application='app name', user_id="token user id")

If you have a long term token you can initialize an api as follows (Just providing only ``long_term_token`` parameter is enough, but for security you need to provide app credentials)::

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


If you already have some medias id, you can get media info by the following methods.

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


If you already have some comments id, you can get comment details info by the following methods.

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

If you already have some replies id, you can get replies details info by the following methods.

To fetch a reply info::

    In [20]: api.get_reply_info(reply_id="18107567341036926")
    Out[20]: IgProReply(id='18107567341036926', timestamp='2019-10-15T07:06:09+0000')

To fetch multi replies info by one requests::

    In [21]: api.get_replies_info(reply_ids=["18107567341036926", "17846106427692294"])
    Out[21]:
    {'18107567341036926': IgProReply(id='18107567341036926', timestamp='2019-10-15T07:06:09+0000'),
     '17846106427692294': IgProReply(id='17846106427692294', timestamp='2019-10-15T07:05:17+0000')}


Use ``get_user_insights`` method, you can get account insights data.

If you want get your account insights, just provide ``user_id`` with your id.

If you have other account's access token, you can provide with ``user_id`` and ``access_token``::

    In [4]: api.get_user_insights(user_id=api.instagram_business_id, period="day", metrics=["impressions", "reach"])
    Out[4]:
    [IgProInsight(name='impressions', period='day'),
     IgProInsight(name='reach', period='day')]


The same as ``get_user_insights``, you can custom provide ``media_id`` and ``access_token``.

Get your media insights data::

    In [6]: api.get_media_insights(media_id="media_id", metrics=["engagement","impressions"])
    Out[6]:
    [IgProInsight(name='engagement', period='lifetime'),
     IgProInsight(name='impressions', period='lifetime')]

Get hashtag id::

    In [3]: api.search_hashtag(q="love")
    Out[3]: [IgProHashtag(id='17843826142012701', name=None)]

Get hashtag info::

    In [4]: api.get_hashtag_info(hashtag_id="17843826142012701")
    Out[4]: IgProHashtag(id='17843826142012701', name='love')

Get hashtag's top medias::

    In [5]: r = api.get_hashtag_top_medias(hashtag_id="17843826142012701", count=5)

    In [6]: r
    Out[6]:
    [IgProMedia(comments=None, id='18086291068155608', permalink='https://www.instagram.com/p/B8ielBPpHaw/'),
     IgProMedia(comments=None, id='17935250359346228', permalink='https://www.instagram.com/p/B8icUmwoF0Y/'),
     IgProMedia(comments=None, id='17847031435934181', permalink='https://www.instagram.com/p/B8icycxKEn-/'),
     IgProMedia(comments=None, id='18000940699302502', permalink='https://www.instagram.com/p/B8ieNN7Cv6S/'),
     IgProMedia(comments=None, id='18025516372248793', permalink='https://www.instagram.com/p/B8iduQJgSyO/')]

Get hashtag's recent medias::

    In [7]: r1 = api.get_hashtag_recent_medias(hashtag_id="17843826142012701", count=5)

    In [8]: r1
    Out[8]:
    [IgProMedia(comments=None, id='18128248021002097', permalink='https://www.instagram.com/p/B8ifnoWA5Ru/'),
     IgProMedia(comments=None, id='18104579776105272', permalink='https://www.instagram.com/p/B8ifwfsgBw2/'),
     IgProMedia(comments=None, id='17898846532442427', permalink='https://www.instagram.com/p/B8ifwZ4ltqP/'),
     IgProMedia(comments=None, id='17891698510462453', permalink='https://www.instagram.com/p/B8ifwepgf_E/'),
     IgProMedia(comments=None, id='17883544606492965', permalink='https://www.instagram.com/p/B8ifwabgiPf/')]

If you have other account's access token, you can provide it with ``user_id`` and ``access_token`` to get its search hashtags.
Or just get your account recent searched hashtags::

    In [9]: api.get_user_recently_searched_hashtags(user_id="17841406338772941")
    Out[9]:
    [IgProHashtag(id='17843826142012701', name='love'),
     IgProHashtag(id='17843421130029320', name='liukun'),
     IgProHashtag(id='17841562447105233', name='loveyou'),
     IgProHashtag(id='17843761288040806', name='a')]


Get the media objects in which a Business or Creator Account has been tagged.
If you have another account authorized access token, you can provide it with ``user_id`` and ``access_token`` to get its data.
Or only get your account's data::

    In [10]: medias = api.get_tagged_user_medias(user_id=api.instagram_business_id, count=5, limit=5)
    Out[10]:
    [IgProMedia(id='18027939643230671', permalink='https://www.instagram.com/p/B38Xyp6nqsS/'),
     IgProMedia(id='17846368219941692', permalink='https://www.instagram.com/p/B8gQCApHMT-/'),
     IgProMedia(id='17913531439230186', permalink='https://www.instagram.com/p/Bop3AGOASfY/'),
     IgProMedia(id='17978630677077508', permalink='https://www.instagram.com/p/BotSABoAn8E/'),
     IgProMedia(id='17955956875141196', permalink='https://www.instagram.com/p/Bn-35GGl7YM/')]

Get data about a comment that an Business or Creator Account has been @mentioned in comment text::

    In [11]: api.get_mentioned_comment_info(user_id=api.instagram_business_id, comment_id="17892250648466172")
    Out[11]: IgProComment(id='17892250648466172', timestamp='2020-02-24T09:15:16+0000')


Get data about a media object on which a Business or Creator Account has been @mentioned in a caption::

    In [12]: api.get_mentioned_media_info(user_id=api.instagram_business_id, media_id="18027939643230671")
    Out[12]: IgProMedia(id='18027939643230671', permalink='https://www.instagram.com/p/B38Xyp6nqsS/')

Now you can publish instagram content if your app have publish permission.

for publish, you need create a container first, the make the container publish.

.. code-block:: python

    # create photo
    >>> api.create_photo(
            image_url="https://www.example.com/images/gugges.jpg",
            caption="publish test",
            location_id="7640348500",
            user_tags='[{"username": "somebody", "x": 0.5, "y": 0.8}]'
        )
    # IgProContainer(id='17877174857201040', status_code=None)

    # create video
    >>> api.create_video(
            video_url="https://www.example.com/videos/hungry-fonzes.mov",
            caption="video test",
            location_id="",
            thumb_offset=5,
        )
    # IgProContainer(id='17877174857201041', status_code=None)

Then you can get container status, if container is ready, You can make it published.

.. code-block:: python

    >>> api.get_container_info(container_id="17877174857201040")
    # IgProContainer(id='17877174857201040', status_code='FINISHED')

Then you can publish it.

.. code-block:: python

    >>> api.publish_container(creation_id="17877174857201040")
    # {'id': '17892354025952911'}

If success, will return the media id.


For now, Instagram accounts are limited to 25 API-published posts within a 24 hour moving period.

So you can get current limit info.

.. code-block:: python

    >>> api.get_publish_limit()
    # IgProPublishLimit(quota_usage=4)

==============================
Base-Usage-Instagram Basic API
==============================

Instagram Basic Display API can be used to access any type of Instagram account but only provides read-access to basic data.

You need do authorize first, and get access token which has permission to retrieve data.

All docs on `Basic Display APi <https://developers.facebook.com/docs/instagram-basic-display-api>`_.

-----------
Initial Api
-----------

Now provide three methods to init api.

If you have long-lived access token, can just initial by token::

    In[1]: from pyfacebook import IgBasicApi
    In[2]: api = IgBasicApi(long_term_token="token")

If you have short-lived access token, can provide with app credentials::

    In[3]: api = IgBasicApi(app_id="app id", app_secret="app secret", short_token="token")

If you want to authorized by user on hand. You can use authorize flow::

    In[4]: api = IgBasicApi(app_id="app id", app_secret="app secret", initial_access_token=False)
    In[5]: api.get_authorization_url()
    Out[5]:
    ('https://api.instagram.com/oauth/authorize?response_type=code&client_id=app+id&redirect_uri=https%3A%2F%2Flocalhost%2F&scope=user_profile+user_media&state=PyFacebook',
     'PyFacebook')
    # give permission and copy the redirect full url.
    In[6]: api.exchange_access_token(response="the full url")

--------
Get Data
--------

You can get user basic info::

    In[7]: api.get_user_info()
    Out[7]: IgBasicUser(id='17841406338772941', username='ikroskun')

You can get user medias::

    In[7]: r = api.get_user_medias()
    In[8]: r
    Out[8]:
    [IgBasicMedia(id='17846368219941692', media_type='IMAGE', permalink='https://www.instagram.com/p/B8gQCApHMT-/'),
     IgBasicMedia(id='18091893643133286', media_type='IMAGE', permalink='https://www.instagram.com/p/B8gPx-UnsjA/'),
     IgBasicMedia(id='18075344632131157', media_type='VIDEO', permalink='https://www.instagram.com/p/B38X8BzHsDi/'),
     IgBasicMedia(id='18027939643230671', media_type='CAROUSEL_ALBUM', permalink='https://www.instagram.com/p/B38Xyp6nqsS/'),
     IgBasicMedia(id='17861821972334188', media_type='IMAGE', permalink='https://www.instagram.com/p/BuGD8NmF4KI/'),
     IgBasicMedia(id='17864312515295083', media_type='IMAGE', permalink='https://www.instagram.com/p/BporjsCF6mt/'),
     IgBasicMedia(id='17924095942208544', media_type='IMAGE', permalink='https://www.instagram.com/p/BoqBgsNl5qT/'),
     IgBasicMedia(id='17896189813249754', media_type='IMAGE', permalink='https://www.instagram.com/p/Bop_Hz5FzyL/'),
     IgBasicMedia(id='17955956875141196', media_type='CAROUSEL_ALBUM', permalink='https://www.instagram.com/p/Bn-35GGl7YM/'),
     IgBasicMedia(id='17970645226046242', media_type='IMAGE', permalink='https://www.instagram.com/p/Bme0cU1giOH/')]

You can get just one media info::

    In[9]: r = basic_api.get_media_info(media_id="18027939643230671")
    In[9]: r
    Out[10]: IgBasicMedia(id='18027939643230671', media_type='CAROUSEL_ALBUM', permalink='https://www.instagram.com/p/B38Xyp6nqsS/')


=======
SUPPORT
=======

``python-facebook-api`` had been being developed with Pycharm under the free JetBrains Open Source license(s) granted by JetBrains s.r.o.,
hence I would like to express my thanks here.

.. image:: docs/imgs/jetbrains.svg
    :target: https://www.jetbrains.com/?from=sns-sdks/python-facebook
    :alt: Jetbrains

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
- Video Info.
- Album Info.
- Photo Info.
- Live Video Info.

Instagram Professional Api:

- Other business account info and media.
- Authorized business account info
- Authorized account medias
- Authorized account comments
- Authorized account replies
- Authorized account insights and media insights
- Search hashtag id
- Get hashtag info
- Get top medias with hashtag
- Get recent medias with hashtag
- Get Authorized account recent searched hashtags
- Get medias which tagged account
- Get comment info mentioned user.
- Get media info mentioned user.
- Publish Content

Instagram Basic display api:

- Get user info
- Get user medias
- Get media info

----
TODO
----

- publish

.. _access-token: https://developers.facebook.com/docs/facebook-login/access-tokens
.. _authorization-manually: https://developers.facebook.com/docs/facebook-login/manually-build-a-login-flow