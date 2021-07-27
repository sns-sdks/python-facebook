"""
    Model class for user.

    Refer: https://developers.facebook.com/docs/graph-api/reference/user
"""

from dataclasses import dataclass
from typing import List, Optional

from dataclasses_json import config

from pyfacebook.models.base import BaseModel, field
from pyfacebook.models.image import Picture


@dataclass
class UserAgeRange(BaseModel):
    """
    A class representing user age range.

    Refer: https://developers.facebook.com/docs/graph-api/reference/age-range/
    """

    max: Optional[int] = field(repr=True)
    min: Optional[int] = field(repr=True)


@dataclass
class UserExperience(BaseModel):
    """
    A class representing user experience.

    Refer: https://developers.facebook.com/docs/graph-api/reference/experience/
    """

    id: Optional[str] = field(repr=True, compare=True)
    name: Optional[str] = field(repr=True)
    description: Optional[str] = field()
    _from: Optional[dict] = field(metadata=config(field_name="from"))
    _with: Optional[List[dict]] = field(metadata=config(field_name="with"))


@dataclass
class User(BaseModel):
    id: Optional[str] = field(repr=True, compare=True)
    about: Optional[str] = field()
    age_range: Optional[UserAgeRange] = field()
    birthday: Optional[str] = field()
    email: Optional[str] = field()
    favorite_athletes: Optional[List[UserExperience]] = field()
    favorite_teams: Optional[List[UserExperience]] = field()
    first_name: Optional[str] = field()
    gender: Optional[str] = field()
    hometown: Optional[dict] = field()
    inspirational_people: Optional[List[UserExperience]] = field()
    install_type: Optional[str] = field()
    installed: Optional[bool] = field()
    is_guest_user: Optional[bool] = field()
    languages: Optional[List[UserExperience]] = field()
    last_name: Optional[str] = field()
    link: Optional[str] = field()
    location: Optional[dict] = field()
    meeting_for: Optional[List[str]] = field()
    middle_name: Optional[str] = field()
    name: Optional[str] = field(repr=True)
    name_format: Optional[str] = field()
    payment_pricepoints: Optional[dict] = field()
    profile_pic: Optional[str] = field()
    quotes: Optional[str] = field()
    shared_login_upgrade_required_by: Optional[str] = field()
    short_name: Optional[str] = field()
    significant_other: Optional[dict] = field()
    supports_donate_button_in_live_video: Optional[bool] = field()
    video_upload_limits: Optional[dict] = field()

    # connections fields
    picture: Optional[Picture] = field()
