"""
    These are models relative facebook page.
"""
import cattr
from typing import Optional, List
from attr import attrs, attrib

from .base import BaseModel


@attrs
class PageCategory(BaseModel):
    """
    A class representing the page category info.

    Refer: https://developers.facebook.com/docs/graph-api/reference/page-category/
    """

    id = attrib(default=None, type=Optional[str])
    api_enum = attrib(default=None, type=Optional[str], repr=False)
    fb_page_categories = attrib(default=None, type=Optional[List])
    name = attrib(default=None, type=Optional[str])

    def __attrs_post_init__(self):
        """
        Because field for fb_page_categories is a list of categories which same structure as PageCategory.
        So need init by hands.
        """
        if isinstance(self.fb_page_categories, (list, tuple)):
            self.fb_page_categories = [cattr.structure(item, PageCategory) for item in self.fb_page_categories]
        elif isinstance(self.fb_page_categories, dict):
            self.fb_page_categories = cattr.structure(self.fb_page_categories, PageCategory)
        else:
            pass


@attrs
class Page(BaseModel):
    """
    A class representing the page info.

    Refer: https://developers.facebook.com/docs/graph-api/reference/page/
    """

    id = attrib(default=None, type=Optional[str])
    about = attrib(default=None, type=Optional[str])
    can_checkin = attrib(default=None, type=Optional[bool], repr=False)
    category = attrib(default=None, type=Optional[str], repr=False)
    category_list = attrib(default=None, type=Optional[List], repr=False)
