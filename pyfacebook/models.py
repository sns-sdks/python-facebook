# coding=utf-8
import json


class BaseModel(object):
    """ Base model class  for instance use. """

    def __init__(self, **kwargs):
        self.param_defaults = {}

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
    def __init__(self, **kwargs):
        BaseModel.__init__(self, **kwargs)
        self.app_id = None
        self.application = None
        self.param_defaults = {
            'app_id': None,
            'application': None,
            'type': None,
            'expires_at': None,
            'is_valid': None,
            'issued_at': None,
            'scopes': None,
            'user_id': None,
        }
        for (param, default) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, default))

    def __repr__(self):
        return "AccessToken(app_id={aid}, app_name={name})".format(
            aid=self.app_id,
            name=self.application,
        )


class Page(BaseModel):
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
            'emails': None,
            'engagement': None,
            'fan_count': None,
            'global_brand_page_name': None,
            'global_brand_root_id': None,
            'link': None,
            'name': None,
            'phone': None,
            'username': None,
            'verification_status': None,
            'website': None,
        }

        for (param, default) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, default))

    def __repr__(self):
        return "Page(ID={pid}, username={username})".format(
            pid=self.id,
            username=self.username
        )


class PagePicture(BaseModel):
    def __init__(self, **kwargs):
        BaseModel.__init__(self, **kwargs)
        self.param_defaults = {
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
            'caption': None,
            'child_attachments': None,
            'created_time': None,
            'description': None,
            'full_picture': None,
            'icon': None,
            'link': None,
            'message': None,
            'name': None,  # Link's name
            'permalink_url': None,
            'picture': None,
            'shares': None,
            'source': None,
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
