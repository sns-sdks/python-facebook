# coding=utf-8
import json


class BaseModel(object):
    """ Base model class  for instance use. """

    def __init__(self, **kwargs):
        self.param_defaults = {}

    def initial_param(self, kwargs):
        for (param, default) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, default))

    @classmethod
    def new_from_json_dict(cls, data, **kwargs):
        """ convert the data from api to model's properties. """
        json_data = data.copy()
        if kwargs:
            for key, val in kwargs.items():
                json_data[key] = val
        c = cls(**json_data)
        c.__json = data
        return c

    def as_dict(self):
        """ Create a dictionary representation of the object. To convert all model properties. """
        data = {}
        for (key, value) in self.param_defaults.items():
            key_attr = getattr(self, key, None)
            if isinstance(key_attr, (list, tuple, set)):
                data[key] = list()
                for sub_obj in key_attr:
                    if getattr(sub_obj, 'as_dict', None):
                        data[key].append(sub_obj.as_dict())
                    else:
                        data[key].append(sub_obj)
            elif getattr(key_attr, 'as_dict', None):
                data[key] = key_attr.as_dict()
            elif key_attr is not None:
                data[key] = getattr(self, key, None)
        return data

    def as_json_string(self):
        """ Create a json string representation of the object. To convert all model properties. """
        return json.dumps(self.as_dict(), sort_keys=True)


class AuthAccessToken(BaseModel):
    """
        A class representing the auth response access token structure.
        Refer: https://developers.facebook.com/docs/facebook-login/manually-build-a-login-flow#confirm
    """

    def __init__(self, **kwargs):
        BaseModel.__init__(self, **kwargs)
        self.param_defaults = {
            'access_token': None,
            'token_type': None,
            'expires_in': None,
            'expires_at': None,
        }
        self.initial_param(kwargs)

    def __repr__(self):
        return "AuthAccessToken(token_type={token_type}, access_token={access_token})".format(
            token_type=self.token_type, access_token=self.access_token,
        )


class AccessToken(BaseModel):
    """
    A class representing the access token structure.
    Refer: https://developers.facebook.com/docs/graph-api/reference/v4.0/debug_token
    """

    def __init__(self, **kwargs):
        BaseModel.__init__(self, **kwargs)
        self.app_id = None
        self.application = None
        self.param_defaults = {
            'app_id': None,
            'application': None,
            'type': None,
            'expires_at': None,
            'data_access_expires_at': None,
            'is_valid': None,
            'issued_at': None,
            'scopes': None,
            'user_id': None,
        }
        self.initial_param(kwargs)

    def __repr__(self):
        return "AccessToken(app_id={aid}, app_name={name})".format(
            aid=self.app_id,
            name=self.application,
        )


class Cover(BaseModel):
    """
    A class representing the cover photo structure.
    Refer: https://developers.facebook.com/docs/graph-api/reference/cover-photo/
    """

    def __init__(self, **kwargs):
        BaseModel.__init__(self, **kwargs)
        self.param_defaults = {
            "id": None,
            "cover_id": None,  # Has Deprecated. Use the id field instead.
            "offset_x": None,
            "offset_y": None,
            "source": None,
        }
        self.initial_param(kwargs)

    def __repr__(self):
        return "Cover(id={id},source={source})".format(
            id=self.id, source=self.source
        )


class PageCategory(BaseModel):
    """
    A class representing the page category structure.
    Refer: https://developers.facebook.com/docs/graph-api/reference/page-category/
    """

    def __init__(self, **kwargs):
        BaseModel.__init__(self, **kwargs)
        self.param_defaults = {
            "id": None,
            "api_enum": None,  # maybe never return.
            "name": None,
        }
        self.initial_param(kwargs)

    def __repr__(self):
        # for py2
        if self.name is not None:
            name = self.name.encode('utf-8')
        else:
            name = self.name  # pragma: no cover
        return "PageCategory(id={id},name={name})".format(
            id=self.id, name=name
        )


class PageEngagement(BaseModel):
    """
    A class representing the engagement structure.
    Refer: https://developers.facebook.com/docs/graph-api/reference/engagement/
    """

    def __init__(self, **kwargs):
        BaseModel.__init__(self, **kwargs)
        self.param_defaults = {
            "count": None,
            "count_string": None,
            "count_string_with_like": None,
            "count_string_without_like": None,
            "social_sentence": None,
            "social_sentence_with_like": None,
            "social_sentence_without_like": None,
        }
        self.initial_param(kwargs)

    def __repr__(self):
        # for py2
        if self.social_sentence is not None:
            social_sentence = self.social_sentence.encode('utf-8')
        else:
            social_sentence = self.social_sentence  # pragma: no cover
        return "PageEngagement(count={count},social_sentence={so})".format(
            count=self.count, so=social_sentence
        )


class Page(BaseModel):
    """
    A class representing the page structure.
    Refer: https://developers.facebook.com/docs/graph-api/reference/page/
    """

    def __init__(self, **kwargs):
        BaseModel.__init__(self, **kwargs)
        self.param_defaults = {
            'id': None,
            'about': None,
            'category': None,
            'category_list': None,
            'checkins': None,
            'cover': None,
            'description': None,
            'description_html': None,
            'display_subtext': None,
            'emails': None,
            'engagement': None,
            'fan_count': None,
            'founded': None,  # only for category_list has company
            'global_brand_root_id': None,
            'link': None,
            'name': None,
            'phone': None,
            'rating_count': None,
            'single_line_address': None,
            'username': None,
            'verification_status': None,
            'website': None,
        }

        for (param, default) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, default))

    def __repr__(self):
        return "Page(id={pid}, username={username})".format(
            pid=self.id,
            username=self.username
        )

    @classmethod
    def new_from_json_dict(cls, data, **kwargs):
        category_list = data.get('category_list')
        if category_list:
            category_list = [PageCategory.new_from_json_dict(ca) for ca in category_list]
        cover = data.get('cover')
        if cover:
            cover = Cover.new_from_json_dict(cover)
        engagement = data.get('engagement')
        if engagement:
            engagement = PageEngagement.new_from_json_dict(engagement)
        return super(cls, cls).new_from_json_dict(
            data=data, category_list=category_list,
            cover=cover, engagement=engagement
        )


class PagePicture(BaseModel):
    """
    A class representing the page picture structure.
    Refer: https://developers.facebook.com/docs/graph-api/reference/profile-picture-source/
    """

    def __init__(self, **kwargs):
        BaseModel.__init__(self, **kwargs)
        self.param_defaults = {
            'cache_key': None,
            'height': None,
            'width': None,
            'is_silhouette': None,
            'url': None
        }
        for (param, default) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, default))

    def __repr__(self):
        return "PagePicture(Height={h}, Width={w}, Url={u})".format(
            h=self.height, w=self.width,
            u=self.url
        )


class ReactionSummary(BaseModel):
    """
    A class representing the page post reaction summary structure.
    Refer: https://developers.facebook.com/docs/graph-api/reference/page-post/reactions/
    """

    def __init__(self, **kwargs):
        BaseModel.__init__(self, **kwargs)
        self.param_defaults = {
            'total_count': None,
            'viewer_reaction': None,
        }
        self.initial_param(kwargs)

    def __repr__(self):
        return "ReactionSummary(total={total},viewer_reaction={rc})".format(
            total=self.total_count, rc=self.viewer_reaction
        )


class ShareSummary(BaseModel):
    """
    A class representing the page post shares structure.
    Almost: {"count": 15892}
    """

    def __init__(self, **kwargs):
        BaseModel.__init__(self, **kwargs)
        self.param_defaults = {
            'count': None,
        }
        self.initial_param(kwargs)

    def __repr__(self):
        return "ShareSummary(count={count})".format(count=self.count)


class Attachment(BaseModel):
    """
    A class representing the attachment structure.
    Refer: https://developers.facebook.com/docs/graph-api/reference/story-attachment/
    """

    def __init__(self, **kwargs):
        BaseModel.__init__(self, **kwargs)
        self.param_defaults = {
            'description': None,
            'description_tags': None,  # almost not appear
            'media': None,  # https://developers.facebook.com/docs/graph-api/reference/story-attachment-media/
            'media_type': None,
            'target': None,  # https://developers.facebook.com/docs/graph-api/reference/story-attachment-target/
            'title': None,
            'type': None,
            'unshimmed_url': None,
            'url': None
        }
        for (param, default) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, default))

    def __repr__(self):
        # for py2
        if self.title is not None:
            title = self.title.encode('utf-8')
        else:
            title = self.title  # pragma: no cover
        return "Attachment(title={title},url={url})".format(
            title=title, url=self.url
        )


class Post(BaseModel):
    """
    A class representing the page post structure.
    Refer: https://developers.facebook.com/docs/graph-api/reference/page-post/
    """

    def __init__(self, **kwargs):
        BaseModel.__init__(self, **kwargs)
        self.param_defaults = {
            'id': None,
            'attachments': None,
            'created_time': None,
            'full_picture': None,
            'icon': None,
            'message': None,
            'permalink_url': None,
            'picture': None,
            'shares': None,
            'status_type': None,
            'tagged_time': None,  # if use tagged resource, this will return.
            'type': None,  # now  type change to attachments{media_type}
            'updated_time': None,
            'comments': None,
            'reactions': None,
            'like': None,
            'love': None,
            'wow': None,
            'haha': None,
            'sad': None,
            'angry': None,
            'thankful': None
        }
        for (param, default) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, default))

    def __repr__(self):
        return "Post(id={pid}, permalink_url={permalink_url})".format(
            pid=self.id,
            permalink_url=self.permalink_url
        )

    @classmethod
    def new_from_json_dict(cls, data, **kwargs):
        # comments summary model
        comments = data.get('comments', {}).get('summary')
        if comments:
            comments = CommentSummary.new_from_json_dict(comments)
        # shares summary model
        shares = data.get('shares')
        if shares:
            shares = ShareSummary.new_from_json_dict(shares)

        # reactions total and sub item
        reactions = data.get('reactions', {}).get('summary')
        if reactions:
            reactions = ReactionSummary.new_from_json_dict(reactions, viewer_reaction='total')
        reactions_like = data.get('like', {}).get('summary')
        if reactions_like:
            reactions_like = ReactionSummary.new_from_json_dict(reactions_like, viewer_reaction='like')
        reactions_love = data.get('love', {}).get('summary')
        if reactions_love:
            reactions_love = ReactionSummary.new_from_json_dict(reactions_love, viewer_reaction='love')
        reactions_wow = data.get('wow', {}).get('summary')
        if reactions_wow:
            reactions_wow = ReactionSummary.new_from_json_dict(reactions_wow, viewer_reaction='wow')
        reactions_haha = data.get('haha', {}).get('summary')
        if reactions_haha:
            reactions_haha = ReactionSummary.new_from_json_dict(reactions_haha, viewer_reaction='haha')
        reactions_sad = data.get('sad', {}).get('summary')
        if reactions_sad:
            reactions_sad = ReactionSummary.new_from_json_dict(reactions_sad, viewer_reaction='sad')
        reactions_angry = data.get('angry', {}).get('summary')
        if reactions_angry:
            reactions_angry = ReactionSummary.new_from_json_dict(reactions_angry, viewer_reaction='angry')
        reactions_thankful = data.get('thankful', {}).get('summary')
        if reactions_thankful:
            reactions_thankful = ReactionSummary.new_from_json_dict(reactions_thankful, viewer_reaction='thankful')

        # attachments
        attachments = data.get('attachments', {}).get('data', [])
        if attachments:
            attachments = [Attachment.new_from_json_dict(item) for item in attachments]
        # for post type
        """
        Deprecated for Page posts for v3.3+.
        Use attachments{media_type} instead.
        If there is no attachments or media_type=link,
        the value is the same as type=status.
        """
        post_type = 'status'  # default
        if attachments is not None and len(attachments) > 0:
            media_type = attachments[0].media_type
            if media_type is not None:
                post_type = media_type

        return super(cls, cls).new_from_json_dict(
            data=data, comments=comments, shares=shares, reactions=reactions,
            like=reactions_like, love=reactions_love, wow=reactions_wow,
            haha=reactions_haha, sad=reactions_sad, angry=reactions_angry,
            thankful=reactions_thankful, attachments=attachments, type=post_type
        )


class Comment(BaseModel):
    """
    A class representing the comment structure.
    Refer: https://developers.facebook.com/docs/graph-api/reference/v4.0/comment
    """

    def __init__(self, **kwargs):
        BaseModel.__init__(self, **kwargs)
        self.param_defaults = {
            'id': None,
            'attachment': None,
            'created_time': None,
            'like_count': None,
            'can_comment': None,
            'can_like': None,
            'comment_count': None,
            '_from': None,  # from is python keyword. so change field name.
            'message': None,
            'permalink_url': None,
        }
        for (param, default) in self.param_defaults.items():
            # handle from properties
            properties = param
            if param == 'from':
                properties = '_form'  # pragma: no cover
            setattr(self, properties, kwargs.get(param, default))

    def __repr__(self):
        return "Comment(id={c_id},created_time={c_time})".format(
            c_id=self.id,
            c_time=self.created_time
        )


class CommentSummary(BaseModel):
    """
    A class representing the comment summary structure.
    Refer: https://developers.facebook.com/docs/graph-api/reference/v4.0/post/comments
    """

    def __init__(self, **kwargs):
        BaseModel.__init__(self, **kwargs)
        self.param_defaults = {
            'order': None,
            'total_count': None,
            'can_comment': None,
        }
        for (param, default) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, default))

    def __repr__(self):
        return "CommentSummary(order={order},total_count={count})".format(
            order=self.order, count=self.total_count
        )


class InstagramUser(BaseModel):
    def __init__(self, **kwargs):
        BaseModel.__init__(self, **kwargs)
        self.id = None
        self.username = None
        self.param_defaults = {
            'biography': None,
            'id': None,
            'ig_id': None,
            'followers_count': None,
            'follows_count': None,
            'media_count': None,
            'name': None,
            'profile_picture_url': None,
            'username': None,
            'website': None,
        }
        for (param, default) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, default))

    def __repr__(self):
        return "User(ID={uid}, username={username})".format(
            uid=self.id,
            username=self.username
        )


class InstagramMedia(BaseModel):
    def __init__(self, **kwargs):
        BaseModel.__init__(self, **kwargs)
        self.id = None
        self.permalink = None
        self.param_defaults = {
            'caption': None,
            'children': None,
            'comments': None,
            'comments_count': None,
            'id': None,
            'ig_id': None,
            'is_comment_enabled': None,
            'like_count': None,
            'media_type': None,
            'media_url': None,
            'owner': None,
            'permalink': None,
            'shortcode': None,
            'thumbnail_url': None,
            'timestamp': None,
            'username': None,
        }
        for (param, default) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, default))

    def __repr__(self):
        return "Media(ID={mid}, link={link})".format(
            mid=self.id,
            link=self.permalink
        )
