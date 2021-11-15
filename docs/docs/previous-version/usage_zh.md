<p align="center">
  <strong>
    Python Facebook
  </strong>
    <br>
    使用 `Python` 封装的 `Facebook` 平台下的一些数据接口.
</p>

<p align="center">
    <a href="https://github.com/sns-sdks/python-facebook/actions">
        <img src="https://github.com/sns-sdks/python-facebook/workflows/Test/badge.svg" alt="Build Status"/>
    </a>
    <a href="https://sns-sdks.github.io/python-facebook/">
        <img src="https://img.shields.io/badge/Docs-passing-brightgreen" alt="Documentation Status"/>
    </a>
    <a href="https://codecov.io/gh/sns-sdks/python-facebook">
        <img src="https://codecov.io/gh/sns-sdks/python-facebook/branch/master/graph/badge.svg" alt="Codecov">
    </a>
    <a href="https://pypi.org/project/python-facebook-api">
        <img src="https://img.shields.io/pypi/v/python-facebook-api.svg" alt="PyPI"/>
    </a>
</p>


## 致谢

灵感来自 [Python-Twitter](https://github.com/bear/python-twitter).


## 说明

该库提供一种更加简单的方式去使用 `Facebook` 平台的数据接口。 注意，当你使用时，由于一些原因，需要在外网环境下才可以使用。

目前包括了 `Facebook`, `Instagram Business`, `Instagram Basic Display` 产品数据的使用。


## 安装

现在可以使用 `pip` 来安装这个包啦:

```shell
$ pip install --upgrade python-facebook-api
# ✨🍰✨
```

## 文档

你可以访问: https://sns-sdks.github.io/python-facebook/ 去查看相关文档 (Doing).

涉及的 `Facebook Graph API` 你都可以通过访问: https://developers.facebook.com/docs/graph-api/ 去查看
涉及的 `Instagram Graph API` 你都可以通过访问: https://developers.facebook.com/docs/instagram-api/ 去查看
涉及的 `Instagram Basic Display API` 你都可以通过访问: https://developers.facebook.com/docs/instagram-basic-display-api/ 去查看


### Facebook Graph API

API 通过 `pyfacebook.Api` 类公开访问。

为了获取对应的数据，你首先需要一个 Facebook App。
你可以访问 [App docs](https://developers.facebook.com/docs/apps) 去获取更多关于如何创建 App 和 如何为 App 申请相关的权限的信息。

另外，你可以在 [Example folder](https://github.com/sns-sdks/python-facebook/tree/v0/examples) 中查看一些简单的例子

#### 初始化 API

Facebook 存在不同类型的访问口令。使用不同的访问口令可以获取不同类型的数据。

1. 用户访问口令
2. 应用访问口令
3. 主页访问口令
4. 客户端访问口令 (由于用到该口令的地方很少，此库不提供)

你可以阅读有关 [Access-Token](https://developers.facebook.com/docs/facebook-login/access-tokens) 的文档去获取更多的信息。

如果你想要通过用户进行授权来获取用户的访问口令，你可以按照 [手动授权](https://developers.facebook.com/docs/facebook-login/manually-build-a-login-flow) 的文档来初始化 `Api`。

如果你只是想通过应用访问口令来获取一些公开数据，你可以通过如下方式初始化 `Api`:

```python
api = Api(app_id="your app id", app_secret="your app secret", application_only_auth=True)
api.get_token_info()
# AccessToken(app_id='id', application='app name', user_id=None)
```

如果你已经有了一个短期的访问口令，你可以通过如下方式初始化 Api:

```python
api = Api(app_id="your app id", app_secret="your app secret", short_token="short-lived token")
api.get_token_info()
# AccessToken(app_id='id', application='app name', user_id='token user id')
```

如果你已经有了一个长期的访问口令，你可以通过如下方式初始化 Api
(注意，只提供一个 ``long_term_token``参数已经足以初始化，当时为了安全器件，最好还是提供一下 app 的认证数据):

```python
api = Api(app_id="your app id", app_secret="your app secret", long_term_token="long-term token")
api.get_token_info()
# AccessToken(app_id='id', application='app name', user_id='token user id')
#  只使用 ``long_term_token`` 参数时，需要该口令具有 ``manage_pages`` 的权限
api = Api(long_term_token="long-term token")
```

使用短期口令和长期口令初始化的区别在于，使用短期口令时，库会自动获取到 长期的口令。

`Facebook` 平台的速率限制很模糊，与你的应用的用户的数量有关，所以此处允许自定义两次请求的间隔时间。
你可以只设置参数 `sleep_on_rate_limit` 为 `True`, 这样两次请求之间的间隔固定为了 2 秒。
或者你可以给参数 `sleep_seconds_mapping` 传递一个自定义的时间数据，比如:

```python
mapping = {10: 2, 20: 5, 50: 20, 70: 30}  # key is api limit reached percent and value is seconds to sleep.
api = Api(
    app_id="your app id", app_secret="your app secret", long_term_token="long-term token",
    sleep_on_rate_limit=True, sleep_seconds_mapping=mapping
)
```

#### 获取数据

你可以通过如下的方式来获取一个主页的公开数据。

获取单个主页的公开数据:

```python
api.get_page_info(username='facebookapp')
# Page(id='20531316728', name='Facebook', username='facebookapp')
```

仅通过一次请求来获取多个主页的公开数据(参数 ``ids`` 可以是主页 ID 和主页用户名混用的列表):

```python
api.get_pages_info(ids=["20531316728", "nba"])
# {'20531316728': Page(id='20531316728', name='Facebook', username='facebookapp'), 'nba': Page(id='8245623462', name='NBA', username='nba')}
```

存在多种方法来获取主页的帖子数据。

```python
api.get_page_feeds()
api.get_page_posts()
api.get_page_published_posts()
api.get_page_tagged_posts()
```

主页 feeds 可以获取主页或者由此主页上的其他人发布的帖子动态(包括状态更新)和链接:

```python
api.get_page_feeds(page_id="20531316728", count=2)
# [Post(id='20531316728_587455038708591', permalink_url='https://www.facebook.com/facebookapp/videos/587455038708591/'),
#    Post(id='20531316728_10159023836696729', permalink_url='https://www.facebook.com/20531316728/posts/10159023836696729/')]
```

主页 posts 只能获取到由该主页发布的帖子:

```python
api.get_page_posts(page_id="20531316728", count=2)
# [Post(id='20531316728_587455038708591', permalink_url='https://www.facebook.com/facebookapp/videos/587455038708591/'), 
#   Post(id='20531316728_10159023836696729', permalink_url='https://www.facebook.com/20531316728/posts/10159023836696729/')]
```

因为图谱 API 的限制. [动态](https://developers.facebook.com/docs/graph-api/reference/v5.0/page/feed)。
API 每年返回大约 600 个经排名的帖子。

所以如果你想要获取主页的所有帖子或者标记该主页的帖子。你需要使用 `get_page_published_posts` 方法，该方法需要你的访问口令带有 `manage_pages` 的权限。

你可以通过授权来得到这样的访问口令，按照 [手动授权](https://developers.facebook.com/docs/facebook-login/manually-build-a-login-flow) 的文档即可。

之后你可以获取到主页所有帖子:

```python
api.get_published_posts(username='facebookapp', access_token='page access token')
# [Post...]
``` 

获取标记该主页的帖子:

```python
api.get_tagged_posts(username='facebookapp', access_token='page access token')
# [Post...]
```

如果你已经有了帖子的 ID，你可以通过如下方法来获取帖子的详情数据。

获取单个帖子的数据:

```python
api.get_post_info(post_id="20531316728_587455038708591")
# Post(id='20531316728_587455038708591', permalink_url='https://www.facebook.com/facebookapp/videos/587455038708591/')
```

单请求获取多个帖子的数据:

```python
api.get_posts_info(ids=["20531316728_587455038708591", "20531316728_10159023836696729"])
# {'20531316728_587455038708591': Post(id='20531316728_587455038708591', permalink_url='https://www.facebook.com/facebookapp/videos/587455038708591/'),
#    '20531316728_10159023836696729': Post(id='20531316728_10159023836696729', permalink_url='https://www.facebook.com/20531316728/posts/10159023836696729/')}
```


你可以通过资源对象(帖子，图片等)的 ID 来获取对应的评论数据:

```python
api.get_comments_by_object(object_id="20531316728_587455038708591", count=2)
# ([Comment(id='587455038708591_587460942041334', can_like=True, can_comment=True, comment_count=2, like_count=1),
#    Comment(id='587455038708591_587464298707665', can_like=True, can_comment=True, comment_count=2, like_count=14)],
#    CommentSummary(total_count=392, can_comment=True))
```

如果你已经有了评论的 ID，你可以通过如下方式来获取评论的详情数据:

获取单个评论的数据:

```python
api.get_comment_info(comment_id="587455038708591_587460942041334")
# Comment(id='587455038708591_587460942041334', comment_count=2, like_count=1)
```

单请求获取多个评论的数据:

```python
api.get_comments_info(ids=["587455038708591_587460942041334", "587455038708591_587464298707665"])
# {'587455038708591_587460942041334': Comment(id='587455038708591_587460942041334', comment_count=2, like_count=1),
#  '587455038708591_587464298707665': Comment(id='587455038708591_587464298707665', comment_count=2, like_count=14)}
```


你可以通过如下方式来获取主页的头像。

获取单个主页的头像数据:

```python
api.get_picture(page_id="20531316728")
# ProfilePictureSource(url='https://scontent.xx.fbcdn.net/v/t1.0-1/p100x100/58978526_10158354585751729_7411073224387067904_o.png?_nc_cat=1&_nc_oc=AQmaFO7eND-DVRoArrQLUZVDpmemw8nMPmHJWvoCyXId_MKLLHQdsS8UbTOX4oaEfeQ&_nc_ht=scontent.xx&oh=128f57c4dc65608993af62b562d92d84&oe=5E942420', height=100, width=100)
```


单请求获取多个主页的头像数据:

```python
api.get_pictures(ids=["20531316728", "nba"])
# {'20531316728': ProfilePictureSource(url='https://scontent.xx.fbcdn.net/v/t1.0-1/p100x100/58978526_10158354585751729_7411073224387067904_o.png?_nc_cat=1&_nc_oc=AQmaFO7eND-DVRoArrQLUZVDpmemw8nMPmHJWvoCyXId_MKLLHQdsS8UbTOX4oaEfeQ&_nc_ht=scontent.xx&oh=128f57c4dc65608993af62b562d92d84&oe=5E942420', height=100, width=100),
#  'nba': ProfilePictureSource(url='https://scontent.xx.fbcdn.net/v/t1.0-1/p100x100/81204460_10158199356848463_5727214464013434880_n.jpg?_nc_cat=1&_nc_oc=AQmcent57E-a-923C_VVpiX26nGqKDodImY1gsiu7h1czDmcpLHXR8D5hIh9g9Ao3wY&_nc_ht=scontent.xx&oh=1656771e6c11bd03147b69ee643238ba&oe=5E66450C', height=100, width=100)}
```

你可以通过对象(主页，用户)的ID获取该对象的视频:

```python
api.get_videos_by_object("ikaroskunlife", fields=["id", "title", "description"], count=None, limit=20)
# [Video(id='969222676905304', created_time=None, description='冬日'),
#  Video(id='210174653594254', created_time=None, description='Snowing'),
#  Video(id='674270653053120', created_time=None, description='Visible')]
```

如果你已经获得了视频的ID，你可以通过如下方式获取视频更多信息:

```python
api.get_video_info("969222676905304")
# Video(id='969222676905304', created_time='2020-09-12T09:53:06+0000', description='冬日')
api.get_videos(ids=["210174653594254", "674270653053120"])
# {'210174653594254': Video(id='210174653594254', created_time='2020-03-31T08:13:14+0000', description='Snowing'),
#  '674270653053120': Video(id='674270653053120', created_time='2019-09-02T06:13:17+0000', description='Visible')}
```

你可以通过对象(主页，用户)的ID获取该对象的相册:

```python
api.get_albums_by_object("instagram", count=20, limit=15)
# [Album(id='372558296163354', created_time='2012-10-29T19:46:35+0000', name='时间线照片'),
#  Album(id='623202484432266', created_time='2014-04-12T15:28:26+0000', name='手机上传')...]
```

如果你已经获得了相册的ID，你可以通过如下方式获取相册更多信息:

```python
api.get_album_info("372558296163354")
# Album(id='372558296163354', created_time='2012-10-29T19:46:35+0000', name='时间线照片')
api.get_albums(ids="372558296163354,623202484432266")
# {'372558296163354': Album(id='372558296163354', created_time='2012-10-29T19:46:35+0000', name='时间线照片'),
#  '623202484432266': Album(id='623202484432266', created_time='2014-04-12T15:28:26+0000', name='手机上传')}
```

你可以通过对象(主页，用户)的ID获取该对象的图片:

```python
api.get_photos_by_object("372558296163354", count=10, limit=5)
# [Photo(id='3293405020745319', created_time='2020-09-10T19:11:01+0000', name='Roller skating = Black joy for Travis Reynolds. 🖤\n\nWatch our IGTV to catch some good vibes and see his 🔥🔥🔥 tricks. \n\n#ShareBlackStories\n\nhttps://www.instagram.com/tv/CE9xgF3jwS_/'),
#  Photo(id='3279789248773563', created_time='2020-09-06T16:23:17+0000', name='#HelloFrom Los Glaciares National Park, Argentina 👏👏👏\n\nhttps://www.instagram.com/p/CEzSoQNMdfH/'),
#  Photo(id='3276650595754095', created_time='2020-09-05T16:52:54+0000', name=None)...]
```

如果你已经获得了图片的ID，你可以通过如下方式获取图片更多信息:

```python
api.get_photo_info("3293405020745319")
# Photo(id='3293405020745319', created_time='2020-09-10T19:11:01+0000', name='Roller skating = Black joy for Travis Reynolds. 🖤\n\nWatch our IGTV to catch some good vibes and see his 🔥🔥🔥 tricks. \n\n#ShareBlackStories\n\nhttps://www.instagram.com/tv/CE9xgF3jwS_/')
api.get_photos(ids=["3279789248773563", "3276650595754095"])
# {'3279789248773563': Photo(id='3279789248773563', created_time='2020-09-06T16:23:17+0000', name='#HelloFrom Los Glaciares National Park, Argentina 👏👏👏\n\nhttps://www.instagram.com/p/CEzSoQNMdfH/'),
# '3276650595754095': Photo(id='3276650595754095', created_time='2020-09-05T16:52:54+0000', name=None)}
```

同样的方式可以获取到: 直播视频数据，以及直播视频的流数据


### Instagram Graph API

Instagram 图谱 API 可以 `instagram Professional accounts <https://help.instagram.com/502981923235522>`_ (商家和创作者) 的数据。

#### 初始化 Api

和 Facebook 的图谱 API 的类似，你可以通过多种方式来初始化 Api。但是你只能使用用户访问口令，并且需要你的商务帐号 ID。

如果你想要通过授权来获取用户的访问口令，你可以按照 [手动授权](https://developers.facebook.com/docs/facebook-login/manually-build-a-login-flow) 来初始化 api。

如果你已经有了一个短期的访问口令，你可以通过如下方式初始化 Api:

```python
api = IgProApi(app_id="your app id", app_secret="your app secret", short_token="short-lived token",
               instagram_business_id="17841406338772941")
api.get_token_info()
# AccessToken(app_id='id', application='app name', user_id="token user id")
```

如果你已经有了一个长期的访问口令，你可以通过如下方式初始化 Api
(注意，只提供一个 `long_term_token` 参数已经足以初始化，当时为了安全器件，最好还是提供一下 app 的认证数据):

```python
api = IgProApi(app_id="your app id", app_secret="your app secret", long_term_token="long-lived token")
api.get_token_info()
# AccessToken(app_id='id', application='app name', user_id='token user id')
```

#### 获取数据

如果你想要搜索其他商家帐号的基础数据和帖子。你可以使用如下的方法:

 - discovery_user: 获取用户的基础数据
 - discovery_user_medias: 获取用户的帖子

!!! note 

   使用 discovery 方法进行搜索只支持使用用户名

通过其他商家用户的用户名来获取基础数据:

```python
api.discovery_user(username="facebook")
# IgProUser(id='17841400455970028', name='Facebook', username='facebook')
```

通过其他商家用户的用户名来获取帖子数据:

```python
api.discovery_user_medias(username="facebook", count=2)
# [IgProMedia(comments=None, id='17859633232647524', permalink='https://www.instagram.com/p/B6jje2UnoH8/'),
#  IgProMedia(comments=None, id='18076151185161297', permalink='https://www.instagram.com/p/B6ji-PZH2V1/')]
```

获取你的帐号的信息:

```python
api.get_user_info(user_id="your instagram business id")
# IgProUser(id='17841406338772941', name='LiuKun', username='ikroskun')
```

获取你的帖子:

```python
api.get_user_medias(user_id=api.instagram_business_id, count=2)
# [IgProMedia(comments=None, id='18075344632131157', permalink='https://www.instagram.com/p/B38X8BzHsDi/'),
#  IgProMedia(comments=None, id='18027939643230671', permalink='https://www.instagram.com/p/B38Xyp6nqsS/')]
```

如果你已经有了一些帖子的 ID 你可以通过如下方式获取帖子的详情数据。

获取单个帖子的详情信息:

```python
api.get_media_info(media_id="18075344632131157")
# IgProMedia(comments=None, id='18075344632131157', permalink='https://www.instagram.com/p/B38X8BzHsDi/')
```


通过单个请求获取多个帖子的详情数据:

```python
api.get_medias_info(media_ids=["18075344632131157", "18027939643230671"])
# {'18075344632131157': IgProMedia(comments=None, id='18075344632131157', permalink='https://www.instagram.com/p/B38X8BzHsDi/'),
#  '18027939643230671': IgProMedia(comments=None, id='18027939643230671', permalink='https://www.instagram.com/p/B38Xyp6nqsS/')}
```


获取某个帖子的评论数据:

```python
api.get_comments_by_media(media_id="17955956875141196", count=2)
# [IgProComment(id='17862949873623188', timestamp='2020-01-05T05:58:47+0000'),
#  IgProComment(id='17844360649889631', timestamp='2020-01-05T05:58:42+0000')]
```


如果你已经有了一些评论的的 ID，你可以通过如下方式来获取评论详情。

获取单个评论的详情:

```python
api.get_comment_info(comment_id="17862949873623188")
# IgProComment(id='17862949873623188', timestamp='2020-01-05T05:58:47+0000')
```

通过单个请求获取多个评论的详情:

```python
api.get_comments_info(comment_ids=["17862949873623188", "17844360649889631"])
# {'17862949873623188': IgProComment(id='17862949873623188', timestamp='2020-01-05T05:58:47+0000'),
#  '17844360649889631': IgProComment(id='17844360649889631', timestamp='2020-01-05T05:58:42+0000')}
```

获取某个评论的回复:

```python
api.get_replies_by_comment("17984127178281340", count=2)
# [IgProReply(id='18107567341036926', timestamp='2019-10-15T07:06:09+0000'),
#  IgProReply(id='17846106427692294', timestamp='2019-10-15T07:05:17+0000')]
```

如果你已经有了一些评论的 ID，你可以通过如下方法来获取回复详情。

获取单个评论的详情:

```python
api.get_reply_info(reply_id="18107567341036926")
# IgProReply(id='18107567341036926', timestamp='2019-10-15T07:06:09+0000')
```

通过单个请求获取多个回复的详情:

```python
api.get_replies_info(reply_ids=["18107567341036926", "17846106427692294"])
# {'18107567341036926': IgProReply(id='18107567341036926', timestamp='2019-10-15T07:06:09+0000'),
#  '17846106427692294': IgProReply(id='17846106427692294', timestamp='2019-10-15T07:05:17+0000')}
```

使用 `get_user_insights` 方法可以获取账号的授权数据。

如果你有另一个业务账号的授权，你可以指定 `user_id` 和 `access_token` 参数，来获取该账号的授权数据。

或者只获取你账号的授权数据:

```python
api.get_user_insights(user_id=api.instagram_business_id, period="day", metrics=["impressions", "reach"])
# [IgProInsight(name='impressions', period='day'), IgProInsight(name='reach', period='day')]
```

与 `get_user_insights` 方法类似，你可以指定 `user_id` 和 `access_token` 参数来获取其他业务帐号的帖子授权数据。
或者获取你自己的帖子的授权数据:

```python
api.get_media_insights(media_id="media_id", metrics=["engagement", "impressions"])
# [IgProInsight(name='engagement', period='lifetime'), IgProInsight(name='impressions', period='lifetime')]
```

搜索标签的ID:

```python
api.search_hashtag(q="love")
# [IgProHashtag(id='17843826142012701', name=None)]
```

获取标签的信息:

```python
api.get_hashtag_info(hashtag_id="17843826142012701")
# IgProHashtag(id='17843826142012701', name='love')
```

获取使用该标签的排名较高的帖子:

```python
api.get_hashtag_top_medias(hashtag_id="17843826142012701", count=5)
# [IgProMedia(comments=None, id='18086291068155608', permalink='https://www.instagram.com/p/B8ielBPpHaw/'),
#  IgProMedia(comments=None, id='17935250359346228', permalink='https://www.instagram.com/p/B8icUmwoF0Y/'),
#  IgProMedia(comments=None, id='17847031435934181', permalink='https://www.instagram.com/p/B8icycxKEn-/'),
#  IgProMedia(comments=None, id='18000940699302502', permalink='https://www.instagram.com/p/B8ieNN7Cv6S/'),
#  IgProMedia(comments=None, id='18025516372248793', permalink='https://www.instagram.com/p/B8iduQJgSyO/')]
```

获取使用该标签的最近的帖子:

```python
api.get_hashtag_recent_medias(hashtag_id="17843826142012701", count=5)
# [IgProMedia(comments=None, id='18128248021002097', permalink='https://www.instagram.com/p/B8ifnoWA5Ru/'),
#  IgProMedia(comments=None, id='18104579776105272', permalink='https://www.instagram.com/p/B8ifwfsgBw2/'),
#  IgProMedia(comments=None, id='17898846532442427', permalink='https://www.instagram.com/p/B8ifwZ4ltqP/'),
#  IgProMedia(comments=None, id='17891698510462453', permalink='https://www.instagram.com/p/B8ifwepgf_E/'),
#  IgProMedia(comments=None, id='17883544606492965', permalink='https://www.instagram.com/p/B8ifwabgiPf/')]
```

如果你有其他业务号的授权，你可以指定 `user_id` 和 `access_token` 来获取到该账号的标签搜索记录，
或者获取你自己的搜索记录:

```python
api.get_user_recently_searched_hashtags(user_id="17841406338772941")
# [IgProHashtag(id='17843826142012701', name='love'), IgProHashtag(id='17841562447105233', name='loveyou')]
```

获取标记了用户的帖子。如果你有其他业务账号的授权，可以指定 ``user_id`` 和 ``access_token`` 来获取到标记该账号的帖文。
或者获取标记你自己账号的帖子:

```python
medias = api.get_tagged_user_medias(user_id=api.instagram_business_id, count=2, limit=5)
# [IgProMedia(id='18027939643230671', permalink='https://www.instagram.com/p/B38Xyp6nqsS/'),
#  IgProMedia(id='17846368219941692', permalink='https://www.instagram.com/p/B8gQCApHMT-/')]
```

获取提到了你的评论的详情信息:

```python
api.get_mentioned_comment_info(user_id=api.instagram_business_id, comment_id="17892250648466172")
# IgProComment(id='17892250648466172', timestamp='2020-02-24T09:15:16+0000')
```

获取提到了你的帖子的详情信息:

```python
api.get_mentioned_media_info(user_id=api.instagram_business_id, media_id="18027939643230671")
# IgProMedia(id='18027939643230671', permalink='https://www.instagram.com/p/B38Xyp6nqsS/')
```


### Instagram Basic API

Instagram 基本显示 API 可以用来访问任何类型的 Instagram 账户，但是仅仅提供对基本数据的访问权限。

使用该 API 时，你需要首先进行授权，获取拥有访问数据的权限的访问口令。

所有的文档你可以你可以访问 [基本显示 API](https://developers.facebook.com/docs/instagram-basic-display-api).

#### 初始化 Api

现在提供三种方式初始化 Api 实例。

如果你已经拥有长效的访问口令。可以直接使用该访问口令进行初始化:

```python
from pyfacebook import IgBasicApi

api = IgBasicApi(long_term_token="token")
```

如果你有短效的访问口令，你需要提供你的应用程序的密钥，用以交换到长效的访问口令:

```python
api = IgBasicApi(app_id="app id", app_secret="app secret", short_token="token")
```

如果你只想要使用应用密钥初始化 Api，然后交由用户手动进行授权，你可以使用授权流程:

```python
api = IgBasicApi(app_id="app id", app_secret="app secret", initial_access_token=False)
api.get_authorization_url()
# ('https://api.instagram.com/oauth/authorize?response_type=code&client_id=app+id&redirect_uri=https%3A%2F%2Flocalhost%2F&scope=user_profile+user_media&state=PyFacebook', 'PyFacebook')
# give permission and copy the redirect full url.
api.exchange_access_token(response="the full url")
```

#### 数据获取

你可以获取用户的基础信息:

```python
api.get_user_info()
# IgBasicUser(id='17841406338772941', username='ikroskun')
``` 

你可以获取用户的帖子信息:

```python
api.get_user_medias()
# [IgBasicMedia(id='17846368219941692', media_type='IMAGE', permalink='https://www.instagram.com/p/B8gQCApHMT-/'),
#  IgBasicMedia(id='17970645226046242', media_type='IMAGE', permalink='https://www.instagram.com/p/Bme0cU1giOH/')]
```

你可以获取当个帖子的信息:

```python
api.get_media_info(media_id="18027939643230671")
# IgBasicMedia(id='18027939643230671', media_type='CAROUSEL_ALBUM', permalink='https://www.instagram.com/p/B38Xyp6nqsS/')
```

## TODO

### 当前的功能

Facebook：

- 主页信息
- 主页图片信息
- 帖子数据
- 评论数据
- 视频数据
- 相册数据
- 图片数据

Instagram：

- 搜索其他业务主页的基础信息和帖子
- 获取授权业务主页的基础信息
- 获取授权业务主页的帖子信息
- 获取授权业务主页的帖子评论数据
- 获取授权业务主页的评论的回复数据
- 获取授权业务主页用户的 Insights 数据
- 获取授权业务主页帖子的 Insights 数据
- 搜索标签 ID
- 获取标签信息
- 获取标签下排名靠前的帖子
- 获取标签下最近的帖子
- 获取授权业务主页的标签搜索记录
- 获取标记了用户的帖文
- 获取提到了用户的评论信息
- 获取提到了用户的帖子信息

Instagram 基础显示 API:

- 获取用户信息
- 获取的用户的帖子
- 获取帖子的详情

### 待做

- 发布帖子
