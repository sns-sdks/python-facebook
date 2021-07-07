"""
    Client for facebook graph api
"""
import inspect

from pyfacebook import GraphAPI
from pyfacebook.api.facebook.resource.base import BaseResource
from pyfacebook.api.facebook import resource as rs


def _is_resource_cls(obj):
    return isinstance(obj, BaseResource)


class FacebookBaseApi(GraphAPI):
    def __new__(cls, *args, **kwargs):
        self = super().__new__(cls)
        resources = inspect.getmembers(cls, _is_resource_cls)
        for name, resource in resources:
            resource_cls = type(resource)
            resource = resource_cls(self)
            setattr(self, name, resource)
        return self


class FacebookApi(FacebookBaseApi):
    """
    Api class for facebook
    """

    user = rs.FacebookUser()
    page = rs.FacebookPage()
