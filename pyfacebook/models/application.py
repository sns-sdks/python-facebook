"""
    Models for application.

    Refer: https://developers.facebook.com/docs/graph-api/reference/application
"""

from dataclasses import dataclass
from typing import Any, List, Optional

from pyfacebook.models.base import BaseModel, field
from pyfacebook.models.extensions import Paging


@dataclass
class ApplicationObjectStoreURLs(BaseModel):
    """
    A class representing the Application Object Store URLs.

    Refer: https://developers.facebook.com/docs/graph-api/reference/application-object-store-urls/
    """

    amazon_app_store: Optional[str] = field()
    fb_canvas: Optional[str] = field()
    fb_gameroom: Optional[str] = field()
    google_play: Optional[str] = field(repr=True)
    instant_game: Optional[str] = field()
    itunes: Optional[str] = field(repr=True)
    itunes_ipad: Optional[str] = field()
    windows_10_store: Optional[str] = field()


@dataclass
class ApplicationRestrictionInfo(BaseModel):
    """
    A class representing the Application Restriction Info.

    Refer: https://developers.facebook.com/docs/graph-api/reference/application-restriction-info/
    """

    age: Optional[str] = field(repr=True)
    age_distribution: Optional[str] = field()
    location: Optional[str] = field()
    type: Optional[str] = field(repr=True)


@dataclass
class Application(BaseModel):
    """
    A class representing the Application.
    """

    id: Optional[str] = field(repr=True, compare=True)
    aam_rules: Optional[str] = field()
    an_ad_space_limit: Optional[int] = field()
    an_platforms: Optional[List[str]] = field()
    app_domains: Optional[List[str]] = field()
    app_events_config: Optional[dict] = field()  # TODO
    app_install_tracked: Optional[bool] = field()
    app_name: Optional[str] = field()
    app_signals_binding_ios: Optional[List[dict]] = field()  # TODO
    app_type: Optional[int] = field()
    auth_dialog_data_help_url: Optional[str] = field()
    auth_dialog_headline: Optional[str] = field()
    auth_dialog_perms_explanation: Optional[str] = field()
    auth_referral_default_activity_privacy: Optional[str] = field()
    auth_referral_enabled: Optional[int] = field()
    auth_referral_extended_perms: Optional[List[str]] = field()
    auth_referral_friend_perms: Optional[List[str]] = field()
    auth_referral_response_type: Optional[str] = field()
    auth_referral_user_perms: Optional[List[str]] = field()
    business: Optional[
        dict
    ] = (
        field()
    )  # TODO Refer: https://developers.facebook.com/docs/marketing-api/reference/business/
    canvas_fluid_height: Optional[bool] = field()
    canvas_fluid_width: Optional[int] = field()
    canvas_url: Optional[str] = field()
    category: Optional[str] = field()
    client_config: Optional[dict] = field()
    company: Optional[str] = field()
    configured_ios_sso: Optional[str] = field()
    contact_email: Optional[str] = field()
    created_time: Optional[str] = field()
    creator_uid: Optional[str] = field()
    daily_active_users: Optional[int] = field()
    daily_active_users_rank: Optional[int] = field()
    deauth_callback_url: Optional[str] = field()
    default_share_mode: Optional[str] = field()
    description: Optional[str] = field()
    financial_id: Optional[str] = field()
    hosting_url: Optional[str] = field()
    icon_url: Optional[str] = field()
    ios_bundle_id: Optional[List[str]] = field()
    ios_supports_native_proxy_auth_flow: Optional[bool] = field()
    ios_supports_system_auth: Optional[bool] = field()
    ipad_app_store_id: Optional[str] = field()
    iphone_app_store_id: Optional[str] = field()
    is_eligible_for_value_optimization: Optional[bool] = field()
    latest_sdk_version: Optional[Any] = field()  # TODO
    link: Optional[str] = field(repr=True)
    logging_token: Optional[str] = field()
    logo_url: Optional[str] = field()
    migrations: Optional[dict] = field()
    mobile_profile_section_url: Optional[str] = field()
    mobile_web_url: Optional[str] = field()
    monthly_active_users: Optional[int] = field()
    monthly_active_users_rank: Optional[int] = field()
    name: Optional[str] = field()
    namespace: Optional[str] = field()
    object_store_urls: Optional[ApplicationObjectStoreURLs] = field()
    page_tab_default_name: Optional[str] = field()
    page_tab_url: Optional[str] = field()
    photo_url: Optional[str] = field()
    privacy_policy_url: Optional[str] = field()
    profile_section_url: Optional[str] = field()
    property_id: Optional[str] = field()
    real_time_mode_devices: Optional[List[str]] = field()
    restrictions: Optional[ApplicationRestrictionInfo] = field()
    restrictive_data_filter_params: Optional[str] = field()
    secure_canvas_url: Optional[str] = field()
    secure_page_tab_url: Optional[str] = field()
    server_ip_whitelist: Optional[str] = field()
    social_discovery: Optional[int] = field()
    subcategory: Optional[str] = field()
    suggested_events_setting: Optional[str] = field()
    supported_platforms: Optional[List[str]] = field()
    terms_of_service_url: Optional[str] = field()
    url_scheme_suffix: Optional[str] = field()
    user_support_email: Optional[str] = field()
    user_support_url: Optional[str] = field()
    website_url: Optional[str] = field()
    weekly_active_users: Optional[int] = field()


@dataclass
class ApplicationTestAccount(BaseModel):
    """
    A class representing the test account for the application.

    Refer: https://developers.facebook.com/docs/graph-api/reference/test-account/
    """

    id: Optional[str] = field(repr=True, compare=True)
    login_url: Optional[str] = field(repr=True)
    access_token: Optional[str] = field()


@dataclass
class ApplicationAccountsResponse(BaseModel):
    """
    A class representing the application edge accounts response.

    Refer: https://developers.facebook.com/docs/graph-api/reference/application/accounts/
    """

    data: Optional[List[ApplicationTestAccount]] = field(repr=True)
    paging: Optional[Paging] = field()
