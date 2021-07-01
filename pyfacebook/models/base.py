"""
    Base model
"""

from dataclasses import dataclass
from typing import (
    Dict,
    Type,
    TypeVar,
    Optional,
)

from dataclasses_json import (
    DataClassJsonMixin,
)

A = TypeVar("A", bound=DataClassJsonMixin)


@dataclass
class BaseModel(DataClassJsonMixin):
    @classmethod
    def new_from_json_dict(
        cls: Type[A], data: Optional[Dict], *, infer_missing=False
    ) -> Optional[A]:
        """
        Convert json dict to data class
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
