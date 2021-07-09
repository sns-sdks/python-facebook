"""
    Models for place relative.

    Refer: https://developers.facebook.com/docs/graph-api/reference/place/
"""

from dataclasses import dataclass
from typing import Optional

from pyfacebook.models.base import BaseModel, field


@dataclass
class Location(BaseModel):
    city: Optional[str] = field()
    city_id: Optional[str] = field()
    country: Optional[str] = field(repr=True)
    country_code: Optional[str] = field()
    latitude: Optional[int] = field()
    located_in: Optional[str] = field()
    longitude: Optional[float] = field()
    name: Optional[str] = field()
    region: Optional[str] = field()
    region_id: Optional[int] = field()
    state: Optional[str] = field()
    street: Optional[str] = field()
    zip: Optional[str] = field()


@dataclass
class Place(BaseModel):
    """
    A class representing the Place.
    """

    id: Optional[str] = field(repr=True, compare=True)
    location: Optional[Location] = field()
    name: Optional[str] = field(repr=True)
    overall_rating: Optional[float] = field()
