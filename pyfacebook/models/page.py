"""
    These are models relative facebook page.

    Note:
        Some field which not common used has not include.
"""
import cattr
from typing import Dict, Optional, List
from attr import attrs, attrib

from .base import BaseModel
from .picture import CoverPhoto, ProfilePictureSource
from .._compat import str


@attrs
class PageCategory(BaseModel):
    """
    A class representing the page category info.

    Refer: https://developers.facebook.com/docs/graph-api/reference/page-category/
    """

    id = attrib(default=None, type=Optional[str])
    api_enum = attrib(default=None, type=Optional[str], repr=False)
    fb_page_categories = attrib(default=None, type=Optional[List], repr=False)
    name = attrib(default=None, type=Optional[str])

    def __attrs_post_init__(self):
        """
        Because field for fb_page_categories is a list of categories which same structure as PageCategory.
        So need init by hands.
        """
        if isinstance(self.fb_page_categories, (list, tuple)):
            self.fb_page_categories = [cattr.structure(item, PageCategory) for item in self.fb_page_categories]
        else:
            pass


@attrs
class ContactAddress(BaseModel):
    """
    A class representing the mailing address info.

    Refer: https://developers.facebook.com/docs/graph-api/reference/mailing-address/
    """
    id = attrib(default=None, type=Optional[str])
    city = attrib(default=None, type=Optional[str])
    country = attrib(default=None, type=Optional[str])
    postal_code = attrib(default=None, type=Optional[str], repr=False)
    region = attrib(default=None, type=Optional[str], repr=False)
    street1 = attrib(default=None, type=Optional[str], repr=False)
    street2 = attrib(default=None, type=Optional[str], repr=False)


@attrs
class PageEngagement(BaseModel):
    """
    A class representing the page engagement info.

    Refer: https://developers.facebook.com/docs/graph-api/reference/engagement/
    """

    count = attrib(default=None, type=Optional[int])
    count_string = attrib(default=None, type=Optional[str], repr=False)
    count_string_with_like = attrib(default=None, type=Optional[str], repr=False)
    count_string_without_like = attrib(default=None, type=Optional[str], repr=False)
    social_sentence = attrib(default=None, type=Optional[str])
    social_sentence_with_like = attrib(default=None, type=Optional[str], repr=False)
    social_sentence_without_like = attrib(default=None, type=Optional[str], repr=False)


@attrs
class PageStartDate(BaseModel):
    """
    A class representing the page start date info.

    Refer: https://developers.facebook.com/docs/graph-api/reference/page-start-date/
    """
    day = attrib(default=None, type=Optional[int])
    month = attrib(default=None, type=Optional[int])
    year = attrib(default=None, type=Optional[int])


@attrs
class PageStartInfo(BaseModel):
    """
    A class representing the page start info.

    Refer: https://developers.facebook.com/docs/graph-api/reference/page-start-info/
    """
    date = attrib(default=None, type=Optional[PageStartDate])
    type = attrib(default=None, type=Optional[str])


@attrs
class Page(BaseModel):
    """
    A class representing the page info.

    Refer: https://developers.facebook.com/docs/graph-api/reference/page/
    """

    id = attrib(default=None, type=Optional[str])
    about = attrib(default=None, type=Optional[str], repr=False)
    can_checkin = attrib(default=None, type=Optional[bool], repr=False)
    category = attrib(default=None, type=Optional[str], repr=False)
    category_list = attrib(default=None, type=Optional[List[PageCategory]], repr=False)
    checkins = attrib(default=None, type=Optional[int], repr=False)
    contact_address = attrib(default=None, type=Optional[ContactAddress], repr=False)
    cover = attrib(default=None, type=Optional[CoverPhoto], repr=False)
    current_location = attrib(default=None, type=Optional[str], repr=False)
    description = attrib(default=None, type=Optional[str], repr=False)
    description_html = attrib(default=None, type=Optional[str], repr=False)
    display_subtext = attrib(default=None, type=Optional[str], repr=False)
    emails = attrib(default=None, type=Optional[List[str]], repr=False)
    engagement = attrib(default=None, type=Optional[PageEngagement], repr=False)
    fan_count = attrib(default=None, type=Optional[int], repr=False)
    founded = attrib(default=None, type=Optional[str], repr=False)
    general_info = attrib(default=None, type=Optional[str], repr=False)
    global_brand_page_name = attrib(default=None, type=Optional[str], repr=False)
    global_brand_root_id = attrib(default=None, type=Optional[str], repr=False)
    link = attrib(default=None, type=Optional[str], repr=False)
    name = attrib(default=None, type=Optional[str])
    # name_with_location_descriptor = attrib(default=None, type=Optional[str], repr=False)
    phone = attrib(default=None, type=Optional[str], repr=False)
    picture = attrib(default=None, type=Optional[Dict], repr=False)
    rating_count = attrib(default=None, type=Optional[str], repr=False)
    single_line_address = attrib(default=None, type=Optional[str], repr=False)
    start_info = attrib(default=None, type=Optional[PageStartInfo], repr=False)
    talking_about_count = attrib(default=None, type=Optional[int], repr=False)
    username = attrib(default=None, type=Optional[str])
    verification_status = attrib(default=None, type=Optional[str], repr=False)
    website = attrib(default=None, type=Optional[str], repr=False)
    were_here_count = attrib(default=None, type=Optional[int], repr=False)
    whatsapp_number = attrib(default=None, type=Optional[str], repr=False)

    def __attrs_post_init__(self):
        if self.picture is not None and isinstance(self.picture, dict):
            picture = self.picture.get("data", {})
            self.picture = ProfilePictureSource.new_from_json_dict(picture)
