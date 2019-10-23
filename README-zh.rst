Python Facebook

使用 `Python` 封装的 `Facebook` 平台下的一些数据接口

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

====
致谢
====

项目的结构基于 `Python-Twitter <https://github.com/bear/python-twitter>`_.

感谢 `Python-Twitter` 项目组的大佬.


====
安装
====

现在可以使用 `pip` 来安装这个包啦::

    $pip install --upgrade python-facebook-api
    ✨🍰✨

由于 `python-facebook` 名称已经被占用，所以只能以这样的名字了。吐槽一波，好名字都被占用，并且好久都没有更新了！！


====
文档
====

你可以访问: https://python-facebook-api.readthedocs.io/en/latest/ 去查看相关文档 (Doing).

所涉及的 ``Facebook Graph API`` 你都可以通过访问: https://developers.facebook.com/docs/graph-api/ 去查看

====
说明
====

该库提供一种更加简单的方式去使用 ``Facebook`` 平台的数据接口。 注意，当你使用时，由于一些原因，需要在外网环境下才可以使用。

目前包括了 ``Facebook``, ``Instagram Business`` 产品数据的使用。


========
如何使用
========

------------
Facebook API
------------

``Facebook API`` 提供了对于 ``Facebook`` 应用下的主页的相关数据的访问。核心层是 ``pyfacebook.Api`` .

在初始化 ``pyfacebook.Api`` 实例时，需要提供脸书平台的 ``App`` 的授权代码，此授权依据获取不同数据需要不同的权限。具体请参阅脸书开发文档的相关权限信息。
最基础的权限是 ``public_content``. 可以获取主页的一些公开数据。

如果你没有相应的 ``App``，需要在 ``Facebook`` 开发者平台下进行申请。

相关文档如下：

- `Facebook 开发者官网 <https://developers.facebook.com/>`_
- `Facebook 授权 <https://developers.facebook.com/docs/facebook-login/access-tokens/#usertokens>`_

使用示例：

可以使用两种方式创建 ``Api`` 实例::

    # 使用临时令牌和App密钥
    In [1]: import pyfacebook

    In [2]: api = pyfacebook.Api(app_id='your app id',   # use the second method.
       ...:                      app_secret='your app secret',
       ...:                      short_token='your short token')

    # 使用长期令牌
    In [3]: api = pyfacebook.Api(long_term_token='your long term access token')


初始化完毕之后可以使用该 ``Api`` 实例获取数据信息.

获取当前Token的关联信息::

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


获取某个 ``Facebook`` 主页的公开数据信息::

    In [5]: api.get_page_info(page_id='20531316728')  # 你可以指定参数 return_json 为 True, 返回 JSON 格式数据
    Out[5]: Page(ID=20531316728, username=facebook)

因为脸书的图谱API的限制 `Page Feed <https://developers.facebook.com/docs/graph-api/reference/v4.0/page/feed>`_ ，
使用普通的 ``User Access Token`` 只能获取大约 600 个经排名的已发布帖子。如果你想要获取到某主页的所有发布贴文，需要使用 ``/{page_id}/published_posts`` 端点。
使用此端点, 需要使用经过主页管理员授予 ``manage_pages`` 权限的主页授权 ``Page Access Token`` 。
如果你有经过授权，可以使用如下操作获取到主页访问口令::

    n [6]: access_token = api.exchange_insights_token(token='user token', page_id='page id')
    Out[6]: 'page access token'

获取到主页访问口令之后，就可以使用如下函数获取当前主页所发布的所有贴文::

    In [7]: api.get_published_posts(username='facebook', access_token='page access token')
    Out[7]: [Post...]

使用主页访问口令，你还可以获取到那些在贴文中对该主页进行标记的贴文。如下::

    In [8]: api.get_tagged_posts(username='facebook', access_token='page access token')
    Out[8]: [Post...]


批量获取某主页的贴文信息(不全)::

    In [9]: api.get_posts(username='facebook')
    Out[9]:
    [Post(ID=20531316728_10158033357426729, permalink_url=https://www.facebook.com/20531316728/posts/10158033357426729/),
     Post(ID=2031316728_10157806010111729, permalink_url=https://www.facebook.com/20531316728/posts/10157806010111729/),
     Post(ID=20531316728_1877006505687069, permalink_url=https://www.facebook.com/facebook/videos/1877006505687069/),
     Post(ID=20531316728_267444427196392, permalink_url=https://www.facebook.com/facebook/videos/267444427196392/)]

获取指定的某个贴文的信息::

    In [10]: res = api.get_post_info(post_id='20531316728_10157619579661729')

    In [11]: res
    Out[11]: Post(ID=20531316728_10157619579661729, permalink_url=https://www.facebook.com/20531316728/posts/10157619579661729/)

    In [12]: res.comments
    Out[12]: 1016


获取某对象(贴文,图片等)的评论数据::

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

目前，Instagram的商家主页可以通过 Facebook 提供的 API 进行数据获取。

即 ``pyfacebook.InstagramApi`` 只能获取 Instagram 平台上的商家主页的数据信息。
所谓的商家主页即是 将 ``Instagram`` 账号和 ``Facebook`` 主页进行关联的 ``Instagram`` 用户。

如果你想要搜索其他的业务主页的数据，你可以使用如下方法::

    - discovery_user: 获取基础数据
    - discovery_user_medias: 获取贴文数据

.. note::
    使用 discovery 方法只支持通过主页用户名进行搜索.

如果你拥有某个主页的相关权限的授权，你可以使用如下方法获取数据::

    - get_user_info
    - get_medias
    - get_media_info
    - get_comments
    - get_comment_info
    - get_replies
    - get_reply_info


初始化 ``pyfacebook.InstagramApi`` 实例需要提供带有 ``Instagram`` 权限的App的用户授权 ``Token``, 以及一个 可用的 ``Instagram`` 商业账号。

详细文档请参阅：

- `Instagram 平台 <https://developers.facebook.com/products/instagram/>`_
- `Instagram Graph API <https://developers.facebook.com/docs/instagram-api>`_

使用示例：

与 ``Facebook Api`` 类似，同样可以使用两种方式初始化 ``InstagramApi`` 实例, 但需要多一个 ``instagram_business_id`` 参数::

    # 使用临时令牌和App密钥
    In [1]: import pyfacebook

    In [2]: api = pyfacebook.InstagramApi(
       ...:     app_id = 'App ID',
       ...:     app_secret='App密钥',
       ...:     short_token='临时令牌',
       ...:     instagram_business_id='你的 Instagram 业务账号ID')

    # 使用长期令牌
    In [3]: api = pyfacebook.InstagramApi(
       ...:     long_term_token='your long term access token',
       ...:     instagram_business_id='你的 Instagram 业务账号ID')


获取其他业务主页用户的基本信息::

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


获取其他业务主页的贴文数据(默认返回近10条)::

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

通过授权的 ``token`` 获取当前业务主页的基础信息::

    In [6]: api.get_user_info(user_id='account id', access_token='access token')
    Out[6]: User(ID=17841406338772941, username=ikroskun)

通过授权的 ``token`` 获取当前业务主页的贴文信息::

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

通过授权的 ``token`` 获取当前业务主页的贴文评论信息::

    In [8]: api.get_comments(media_id='media id', access_token='access token')
    Out[8]: [Comment(ID=18008567518250255,timestamp=2019-10-23T02:10:32+0000)]

等等...

====
TODO
====

当前的功能
---------

Facebook：

- 主页信息
- 主页图片信息
- 贴文数据
- 评论数据

Instagram：

- 搜索其他业务主页的基础信息和贴文
- 获取授权业务主页的基础信息
- 获取授权业务主页的贴文信息
- 获取授权业务主页的贴文评论数据
- 获取授权业务主页的评论的回复数据

待做
----

- Insights 数据的获取
- 发布帖子

