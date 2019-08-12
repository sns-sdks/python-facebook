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
        return "PageCategory(id={id},name={name})".format(
            id=self.id, name=self.name
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
        return "PageEngagement(count={count},social_sentence={so})".format(
            count=self.count, so=self.social_sentence
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


class Post(BaseModel):
    def __init__(self, **kwargs):
        BaseModel.__init__(self, **kwargs)
        self.param_defaults = {
            'id': None,
            'attachments': None,
            'child_attachments': None,
            'created_time': None,
            'full_picture': None,
            'icon': None,
            'message': None,
            'permalink_url': None,
            'picture': None,
            'shares': None,
            'status_type': None,
            'type': None,
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
        return "Post(ID={pid}, permalink_url={permalink_url})".format(
            pid=self.id,
            permalink_url=self.permalink_url
        )

    @classmethod
    def new_from_json_dict(cls, data, **kwargs):
        json_data = data.copy()
        if kwargs:
            for key, val in kwargs.items():
                json_data[key] = val
        # handle the different count.
        for key, val in json_data.items():
            if isinstance(val, dict):
                if not key.endswith('attachments'):
                    if 'count' in val:
                        json_data[key] = val['count']
                    elif 'summary' in val:
                        json_data[key] = val['summary'].get('total_count', 0)
                else:
                    json_data[key] = val
            else:
                json_data[key] = val
        c = cls(**json_data)
        c.__json = data
        return c


class Attachment(BaseModel):
    def __init__(self, **kwargs):
        BaseModel.__init__(self, **kwargs)
        self.param_defaults = {
            'description': None,
            'description_tags': None,
            'media': None,
            'media_type': None,
            'target': None,
            'title': None,
            'type': None,
            'unshimmed_url': None,
            'url': None
        }
        for (param, default) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, default))

    def __repr__(self):
        return "Attachment(TITLE={title},url={url})".format(
            title=self.title,
            url=self.url
        )


class Comment(BaseModel):
    def __init__(self, **kwargs):
        BaseModel.__init__(self, **kwargs)
        self.param_defaults = {
            'id': None,
            'created_time': None,
            'message': None,
            'like_count': None,
            'permalink_url': None,
            '_from': None,
            'comment_count': None
        }
        for (param, default) in self.param_defaults.items():
            # handle from properties
            properties = param
            if param == 'from':
                properties = '_form'
            setattr(self, properties, kwargs.get(param, default))

    def __repr__(self):
        return "Comment(ID={c_id},created_time={c_time})".format(
            c_id=self.id,
            c_time=self.created_time
        )


class CommentSummary(BaseModel):
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
            order=self.order,
            count=self.total_count
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
