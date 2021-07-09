"""
    Base model
"""
from copy import deepcopy
from dataclasses import dataclass, field as base_field
from typing import (
    Dict,
    Type,
    TypeVar,
    Optional,
)

from dataclasses_json import (
    DataClassJsonMixin,
)
from dataclasses_json.core import Json

A = TypeVar("A", bound=DataClassJsonMixin)


@dataclass
class BaseModel(DataClassJsonMixin):
    @classmethod
    def new_from_json_dict(
        cls: Type[A], data: Optional[Dict], *, infer_missing=False
    ) -> Optional[A]:
        """
        Convert json dict to dataclass
        :param data: A json dict which will convert model class.
        :param infer_missing: if set True, will let missing field (not have default vale) to None
        :return: The data class
        """
        if not data:
            return None
        c = cls.from_dict(data, infer_missing=infer_missing)
        # save origin data
        cls._json = data
        return c

    def to_dict(self, encode_json=False, ignore_nan=True) -> Dict[str, Json]:
        """
        Convert dataclass to dict
        :param encode_json:
        :param ignore_nan: Is the result include None data.
        :return: dict
        """
        data = super().to_dict(encode_json=encode_json)
        if ignore_nan:
            data = dict_minus_none_values(data)
        return data


def dict_minus_none_values(obj: Optional[dict]):
    """
    Remove data dict where value is None
    :param obj: dict object
    :return: obj
    """
    if obj is None:
        return None

    keys = list(obj.keys())
    for key in keys:
        value = obj[key]
        if value is None:
            obj.pop(key)
        if isinstance(value, (list, tuple)):
            obj[key] = type(value)([dict_minus_none_values(v) for v in value])
        if isinstance(value, dict):
            obj[key] = dict_minus_none_values(value)
    return deepcopy(obj)


def field(default=None, repr=False, compare=False, **kwargs):
    kwargs.update(
        {
            "default": default,
            "repr": repr,
            "compare": compare,
        }
    )
    return base_field(**kwargs)
