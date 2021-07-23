"""
    Models for event.

    Refer: https://developers.facebook.com/docs/graph-api/reference/event
"""

from dataclasses import dataclass
from typing import List, Optional

from pyfacebook.models.base import BaseModel, field
from pyfacebook.models.image import CoverPhoto


@dataclass
class EventTime(BaseModel):
    """
    A class representing for the time of child event.
    """

    id: Optional[str] = field(repr=True, compare=True)
    start_time: Optional[str] = field(repr=True)
    ticket_uri: Optional[str] = field()
    end_time: Optional[str] = field(repr=True)


@dataclass
class Event(BaseModel):
    """
    A class representing the Event.
    """

    id: Optional[str] = field(repr=True, compare=True)
    attending_count: Optional[int] = field()
    can_guests_invite: Optional[bool] = field()
    category: Optional[str] = field()
    cover: Optional[CoverPhoto] = field()
    created_time: Optional[str] = field()
    declined_count: Optional[int] = field()
    description: Optional[str] = field()
    discount_code_enabled: Optional[bool] = field()
    end_time: Optional[str] = field()
    event_times: Optional[List[EventTime]] = field()
    guest_list_enabled: Optional[bool] = field()
    interested_count: Optional[int] = field()
    is_canceled: Optional[bool] = field()
    is_draft: Optional[bool] = field()
    is_online: Optional[bool] = field()
    is_page_owned: Optional[bool] = field()
    maybe_count: Optional[int] = field()
    name: Optional[str] = field(repr=True)
    noreply_count: Optional[int] = field()
    online_event_format: Optional[str] = field()
    online_event_third_party_url: Optional[str] = field()
    owner: Optional[dict] = field()
    parent_group: Optional[
        dict
    ] = (
        field()
    )  # TODO Refer: https://developers.facebook.com/docs/graph-api/reference/group/
    place: Optional[
        dict
    ] = (
        field()
    )  # TODO Refer: https://developers.facebook.com/docs/graph-api/reference/place/
    scheduled_publish_time: Optional[str] = field()
    start_time: Optional[str] = field(repr=True)
    ticket_uri: Optional[str] = field()
    ticket_uri_start_sales_time: Optional[str] = field()
    ticketing_privacy_uri: Optional[str] = field()
    ticketing_terms_uri: Optional[str] = field()
    timezone: Optional[str] = field()
    type: Optional[str] = field()
    updated_time: Optional[str] = field()
