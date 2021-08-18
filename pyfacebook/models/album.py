"""
    Model class for album.

    Refer: https://developers.facebook.com/docs/graph-api/reference/album/
"""

from dataclasses import dataclass
from typing import List, Optional

from dataclasses_json import config

from pyfacebook.models.base import BaseModel, field
from pyfacebook.models.extensions import Paging


@dataclass
class Album(BaseModel):
    """
    A class representing the Album.
    """

    id: Optional[str] = field(repr=True, compare=True)
    backdated_time: Optional[str] = field()
    backdated_time_granularity: Optional[str] = field()
    can_upload: Optional[bool] = field()
    count: Optional[int] = field()
    cover_photo: Optional[
        dict
    ] = (
        field()
    )  # TODO Refer: https://developers.facebook.com/docs/graph-api/reference/photo/
    created_time: Optional[str] = field()
    description: Optional[str] = field()
    event: Optional[
        dict
    ] = (
        field()
    )  # TODO Refer: https://developers.facebook.com/docs/graph-api/reference/event/
    _from: Optional[dict] = field(metadata=config(field_name="from"))
    link: Optional[str] = field()
    location: Optional[str] = field()
    name: Optional[str] = field(repr=True)
    place: Optional[
        dict
    ] = (
        field()
    )  # TODO Refer: https://developers.facebook.com/docs/graph-api/reference/place/
    privacy: Optional[str] = field()
    type: Optional[str] = field()
    updated_time: Optional[str] = field()


@dataclass
class AlbumResponse(BaseModel):
    """
    A class representing the result for albums edge.

    Refer: https://developers.facebook.com/docs/graph-api/reference/page/albums
    """

    data: List[Album] = field(repr=True, compare=True)
    paging: Optional[Paging] = field()
