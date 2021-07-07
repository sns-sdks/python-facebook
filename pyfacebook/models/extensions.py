"""
    Models for common
"""

from dataclasses import dataclass
from typing import Optional

from pyfacebook.models.base import BaseModel, field


@dataclass
class Location(BaseModel):
    """
    A class representing the location.

    Refer: https://developers.facebook.com/docs/graph-api/reference/location/
    """

    city: Optional[str] = field(repr=True)
    city_id: Optional[int] = field()
    country: Optional[str] = field()
    latitude: Optional[float] = field()
    located_in: Optional[str] = field()
    longitude: Optional[float] = field()
    name: Optional[str] = field()
    region: Optional[str] = field()
    region_id: Optional[int] = field()
    state: Optional[str] = field()
    street: Optional[str] = field()
    zip: Optional[str] = field()


@dataclass
class VOIPInfo(BaseModel):
    """
    A class representing the VOIP Info.

    Refer: https://developers.facebook.com/docs/graph-api/reference/voip-info/
    """

    has_mobile_app: Optional[bool] = field(repr=True)
    has_permission: Optional[bool] = field(repr=True)
    is_callable: Optional[bool] = field(repr=True)
    is_callable_webrtc: Optional[bool] = field(repr=True)
    is_pushable: Optional[bool] = field(repr=True)
    reason_code: Optional[int] = field(repr=True)
    reason_description: Optional[str] = field(repr=True)
