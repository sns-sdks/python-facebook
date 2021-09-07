"""
    Models for business.

    Refer: https://developers.facebook.com/docs/marketing-api/reference/business/
"""

from dataclasses import dataclass
from typing import List, Optional

from pyfacebook.models.base import BaseModel, field
from pyfacebook.models.extensions import Paging


@dataclass
class Business(BaseModel):
    """
    A class representing the Business.
    """

    id: Optional[str] = field(repr=True, compare=True)
    block_offline_analytics: Optional[bool] = field()
    collaborative_ads_managed_partner_business_info: Optional[dict] = field()
    collaborative_ads_managed_partner_eligibility: Optional[dict] = field()
    created_by: Optional[dict] = field()
    created_time: Optional[str] = field()
    extended_updated_time: Optional[str] = field()
    is_hidden: Optional[bool] = field()
    link: Optional[str] = field()
    name: Optional[str] = field(repr=True)
    payment_account_id: Optional[str] = field()
    primary_page: Optional[dict] = field()
    profile_picture_uri: Optional[str] = field()
    timezone_id: Optional[int] = field()
    two_factor_type: Optional[str] = field()
    updated_by: Optional[dict] = field()
    updated_time: Optional[str] = field()
    verification_status: Optional[str] = field()
    vertical: Optional[str] = field()
    vertical_id: Optional[int] = field()
    permitted_roles: Optional[List[str]] = field()


@dataclass
class BusinessResponse(BaseModel):
    """
    A class representing the result for businesses edge.

    Refer: https://developers.facebook.com/docs/graph-api/reference/user/businesses/
    """

    data: List[Business] = field(repr=True, compare=True)
    paging: Optional[Paging] = field()
