"""
    These are models relative facebook page.
"""
from typing import Optional, List
from attr import attrs, attrib

from .base import BaseModel


def ensure_cls(cls):
    """If the attribute is an instance of cls, pass, else try constructing."""

    def converter(val):
        if isinstance(val, cls):
            return val
        elif isinstance(val, (list, tuple)):
            return [cls(**item for item in val)]
        else:
            return cls(**val)

    return converter


@attrs
class PageCategory(BaseModel):
    """
    A class representing the page category info.

    Refer: https://developers.facebook.com/docs/graph-api/reference/page-category/
    """

    id = attrib(default=None, type=Optional[str])
    api_enum = attrib(default=None, type=Optional[str], repr=False)
    # fb_page_categories = attrib(converter=ensure_cls(PageCategory), default=None)
    name = attrib(default=None, type=Optional[str])


@attrs
class Page(BaseModel):
    """
    A class representing the page info.

    Refer: https://developers.facebook.com/docs/graph-api/reference/page/
    """

    id = attrib(default=None, type=Optional[str])
    about = attrib(default=None, type=Optional[str])
    category = attrib(default=None, type=Optional[str], repr=False)
    category_list = attrib(default=None, type=Optional[List], repr=False)
