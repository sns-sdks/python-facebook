"""
    Model class for Photo.

    Refer: https://developers.facebook.com/docs/graph-api/reference/photo/
"""

from dataclasses import dataclass
from typing import List, Optional

from dataclasses_json import config

from pyfacebook.models.base import BaseModel, field
from pyfacebook.models.extensions import Paging
from pyfacebook.models.attachment import EntityAtTextRange


@dataclass
class PlatformImageSource(BaseModel):
    """
    A class representing the Platform Image Source.

    Refer: https://developers.facebook.com/docs/graph-api/reference/platform-image-source/
    """

    height: Optional[int] = field()
    source: Optional[str] = field(repr=True)
    width: Optional[int] = field()


@dataclass
class Photo(BaseModel):
    """
    A class representing the Photo.
    """

    id: Optional[str] = field(repr=True, compare=True)
    album: Optional[
        dict
    ] = (
        field()
    )  # TODO Refer: https://developers.facebook.com/docs/graph-api/reference/album/
    alt_text: Optional[str] = field()
    alt_text_custom: Optional[str] = field()
    backdated_time: Optional[str] = field()
    backdated_time_granularity: Optional[str] = field()
    can_backdate: Optional[bool] = field()
    can_delete: Optional[bool] = field()
    can_tag: Optional[bool] = field()
    created_time: Optional[str] = field()
    event: Optional[
        dict
    ] = (
        field()
    )  # TODO Refer: https://developers.facebook.com/docs/graph-api/reference/event/
    _from: Optional[dict] = field(metadata=config(field_name="from"))
    height: Optional[int] = field()
    icon: Optional[str] = field()
    images: Optional[List[PlatformImageSource]] = field()
    link: Optional[str] = field()
    name: Optional[str] = field(repr=True)
    name_tags: Optional[List[EntityAtTextRange]] = field()
    page_story_id: Optional[str] = field()
    place: Optional[
        dict
    ] = (
        field()
    )  # TODO Refer: https://developers.facebook.com/docs/graph-api/reference/place/
    target: Optional[
        dict
    ] = (
        field()
    )  # TODO Refer: https://developers.facebook.com/docs/graph-api/reference/profile/
    updated_time: Optional[str] = field()
    webp_images: Optional[List[PlatformImageSource]] = field()
    width: Optional[int] = field()


@dataclass
class PhotosResponse(BaseModel):
    """
    A class representing the result for photos edge.

    Refer: https://developers.facebook.com/docs/graph-api/reference/page/photos
    """

    data: List[Photo] = field(repr=True, compare=True)
    paging: Optional[Paging] = field()
