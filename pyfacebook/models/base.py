"""
    This is the base model
"""
import json

import cattr
from attr import attrs


@attrs
class BaseModel(object):

    @classmethod
    def new_from_json_dict(cls, data):
        instance = cattr.structure(data, cls)
        instance._json = data  # save original data
        return instance

    def as_dict(self):
        return cattr.unstructure(self)

    def as_json_str(self):
        return json.dumps(self.as_dict())
