Python Facebook

使用 `Python` 封装的 `Facebook` 平台下的一些数据接口

.. image:: https://travis-ci.org/MerleLiuKun/python-facebook.svg?branch=master
    :target: https://travis-ci.org/MerleLiuKun/python-facebook
    :alt: Build Status

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
使用普通的 `Token` 只能获取大约 600 个经排名的已发布帖子。如果你想要获取到某主页的所有发布贴文，需要使用 `/{page_id}/published_posts` 端点。
使用此端点, 需要使用经过主页管理员授予 `manage_pages` 权限的主页授权 `Token` 。
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


初始化 ``pyfacebook.InstagramApi`` 实例需要提供带有 ``Instagram`` 权限的App的用户授权 ``Token``, 以及一个 可用的 ``Instagram`` 商业账号。


详细文档请参阅：

- `Instagram 平台 <https://developers.facebook.com/products/instagram/>`_
- `Business Discovery API <https://developers.facebook.com/docs/instagram-api/business-discovery>`_

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


获取某用户的基本信息::

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

批量获取某用户的贴文(默认获取近50条)::

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

获取某贴文的信息(此API只可以供给当前Instagram商业账号的贴文可用, 对他人无法获取)::

    In [5]: api.get_media_info(media_id='17861821972334188')
    Out[5]: Media(ID=17861821972334188, link=https://www.instagram.com/p/BuGD8NmF4KI/)


====
TODO
====

现在只可以通过该``API`` 获取到主页基本信息以及主页的贴文数据以及对象(帖子,图片)的评论数据。

待做：

- Insights 数据的获取
- 发布帖子
- 更多....

