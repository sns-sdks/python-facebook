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
            data[key] = getattr(self, key, None)
        return data

    def as_json_string(self):
        """ Create a json string representation of the object. To convert all model properties. """
        return json.dumps(self.as_dict(), sort_keys=True)


class AccessToken(BaseModel):
    def __init__(self, **kwargs):
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


class Post(BaseModel):
    def __init__(self, **kwargs):
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
