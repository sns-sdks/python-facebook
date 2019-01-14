# coding=utf-8


class BaseModel(object):
    """ Base model class  for instance use. """

    def __init__(self, **kwargs):
        self.param_defaults = {}


class AccessToken(BaseModel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
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

    @classmethod
    def new_from_json_dict(cls, data, **kwargs):
        json_data = data.copy()
        if kwargs:
            for key, val in kwargs.items():
                json_data[key] = val
        c = cls(**json_data)
        c.__json = data
        return c


class Page(BaseModel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
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
            'page_about_story': None,
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


class Post(BaseModel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
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
        return "Post(ID={pid}, link={link})".format(
            pid=self.id,
            link=self.link
        )
