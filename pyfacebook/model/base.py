"""
    This is the base model
"""
import six

import cattr
from attr import attrs


@attrs
class BaseModel(object):

    @classmethod
    def drop_extra_attrs(cls, data):
        attrs_attrs = getattr(cls, '__attrs_attrs__', None)
        attributes = {attr.name for attr in attrs_attrs}
        return {key: val for key, val in six.iteritems(data) if key in attributes}

    @classmethod
    def new_from_json_dict(cls, data):
        data = cls.drop_extra_attrs(data)
        instance = cattr.structure(data, cls)
        return instance

    def as_dict(self):
        return cattr.unstructure(self)
