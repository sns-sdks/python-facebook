"""
    Model class for page.

    Refer: https://developers.facebook.com/docs/graph-api/reference/page
"""
from dataclasses import dataclass
from typing import List, Optional

from pyfacebook.models.base import BaseModel, field
from pyfacebook.models.extensions import VOIPInfo
from pyfacebook.models.place import Location
from pyfacebook.models.image import CoverPhoto, Picture


@dataclass
class PageCategory(BaseModel):
    """
    A class representing page category.

    Refer: https://developers.facebook.com/docs/graph-api/reference/page-category/
    """

    id: Optional[str] = field(repr=True, compare=True)
    api_enum: Optional[str] = field()
    fb_page_categories: Optional[List["PageCategory"]] = field()
    name: Optional[str] = field(repr=True)


@dataclass
class MailingAddress(BaseModel):
    """
    A class representing mailing address.

    Refer: https://developers.facebook.com/docs/graph-api/reference/mailing-address/
    """

    id: Optional[str] = field(repr=True, compare=True)
    city: Optional[str] = field(repr=True)
    city_page: Optional["Page"] = field()
    country: Optional[str] = field()
    postal_code: Optional[str] = field()
    region: Optional[str] = field()
    street1: Optional[str] = field()
    street2: Optional[str] = field()


@dataclass
class Engagement(BaseModel):
    """
    A class representing the Engagement.

    Refer: https://developers.facebook.com/docs/graph-api/reference/engagement/
    """

    count: Optional[int] = field()
    count_string: Optional[str] = field()
    count_string_with_like: Optional[str] = field()
    count_string_without_like: Optional[str] = field()
    social_sentence: Optional[str] = field()
    social_sentence_with_like: Optional[str] = field()
    social_sentence_without_like: Optional[str] = field()


@dataclass
class PageParking(BaseModel):
    """
    A class representing the page parking.
    Refer: https://developers.facebook.com/docs/graph-api/reference/page-parking/
    """

    lot: Optional[int] = field(repr=True)
    street: Optional[int] = field(repr=True)
    valet: Optional[int] = field(repr=True)


@dataclass
class PageRestaurantServices(BaseModel):
    """
    A class representing the page restaurant services.

    Refer: https://developers.facebook.com/docs/graph-api/reference/page-restaurant-services/
    """

    catering: Optional[bool] = field(repr=True)
    delivery: Optional[bool] = field(repr=True)
    groups: Optional[bool] = field(repr=True)
    kids: Optional[bool] = field(repr=True)
    outdoor: Optional[bool] = field(repr=True)
    pickup: Optional[bool] = field(repr=True)
    reserve: Optional[bool] = field(repr=True)
    takeout: Optional[bool] = field(repr=True)
    waiter: Optional[bool] = field(repr=True)
    walkins: Optional[bool] = field(repr=True)


@dataclass
class PageRestaurantSpecialties(BaseModel):
    """
    A class representing the Page Restaurant Specialties.

    Refer: https://developers.facebook.com/docs/graph-api/reference/page-restaurant-specialties/
    """

    breakfast: Optional[int] = field(repr=True)
    coffee: Optional[int] = field(repr=True)
    dinner: Optional[int] = field(repr=True)
    drinks: Optional[int] = field(repr=True)
    lunch: Optional[int] = field(repr=True)


@dataclass
class PagePaymentOptions(BaseModel):
    """
    A class representing the Page Payment Options.

    Refer: https://developers.facebook.com/docs/graph-api/reference/page-payment-options/
    """

    amex: Optional[int] = field(repr=True)
    cash_only: Optional[int] = field()
    discover: Optional[int] = field()
    mastercard: Optional[int] = field()
    visa: Optional[int] = field()


@dataclass
class PageStartDate(BaseModel):
    """
    A class representing the Page Start Date.

    Refer: https://developers.facebook.com/docs/graph-api/reference/page-start-date/
    """

    day: Optional[int] = field(repr=True)
    month: Optional[int] = field(repr=True)
    year: Optional[int] = field(repr=True)


@dataclass
class PageStartInfo(BaseModel):
    """
    A class representing the Page Start Info.

    Refer: https://developers.facebook.com/docs/graph-api/reference/page-start-info/
    """

    date: Optional[PageStartDate] = field(repr=True)
    type: Optional[str] = field(repr=True)


@dataclass
class Page(BaseModel):
    """
    A class representing page.
    """

    id: Optional[str] = field(repr=True, compare=True)
    about: Optional[str] = field()
    access_token: Optional[str] = field()
    ad_campaign: Optional[dict] = field()
    affiliation: Optional[str] = field()
    app_id: Optional[str] = field()
    artists_we_like: Optional[str] = field()
    attire: Optional[str] = field()
    awards: Optional[str] = field()
    band_interests: Optional[str] = field()
    band_members: Optional[str] = field()
    best_page: Optional[dict] = field()
    bio: Optional[str] = field()
    birthday: Optional[str] = field()
    booking_agent: Optional[str] = field()
    built: Optional[str] = field()
    business: Optional[dict] = field()
    can_checkin: Optional[bool] = field()
    can_post: Optional[bool] = field()
    category: Optional[str] = field()
    category_list: Optional[List[PageCategory]] = field()
    checkins: Optional[int] = field()
    company_overview: Optional[str] = field()
    connected_instagram_account: Optional[dict] = field()
    connected_page_backed_instagram_account: Optional[dict] = field()
    contact_address: Optional[MailingAddress] = field()
    copyright_attribution_insights: Optional[dict] = field()
    copyright_whitelisted_ig_partners: Optional[List[str]] = field()
    country_page_likes: Optional[int] = field()
    cover: Optional[CoverPhoto] = field()
    culinary_team: Optional[str] = field()
    current_location: Optional[str] = field()
    delivery_and_pickup_option_info: Optional[List[str]] = field()
    description: Optional[str] = field()
    description_html: Optional[str] = field()
    differently_open_offerings: Optional[dict] = field()
    directed_by: Optional[str] = field()
    display_subtext: Optional[str] = field()
    displayed_message_response_time: Optional[str] = field()
    emails: Optional[List[str]] = field()
    engagement: Optional[Engagement] = field()
    fan_count: Optional[int] = field()
    featured_video: Optional[dict] = field()
    features: Optional[str] = field()
    followers_count: Optional[int] = field()
    food_styles: Optional[List[str]] = field()
    founded: Optional[str] = field()
    general_info: Optional[str] = field()
    general_manager: Optional[str] = field()
    genre: Optional[str] = field()
    global_brand_page_name: Optional[str] = field()
    global_brand_root_id: Optional[str] = field()
    has_added_app: Optional[bool] = field()
    has_transitioned_to_new_page_experience: Optional[bool] = field()
    has_whatsapp_business_number: Optional[bool] = field()
    has_whatsapp_number: Optional[bool] = field()
    hometown: Optional[str] = field()
    hours: Optional[dict] = field()
    impressum: Optional[str] = field()
    influences: Optional[str] = field()
    instagram_business_account: Optional[dict] = field()
    instant_articles_review_status: Optional[str] = field()
    is_always_open: Optional[bool] = field()
    is_chain: Optional[bool] = field()
    is_community_page: Optional[bool] = field()
    is_eligible_for_branded_content: Optional[bool] = field()
    is_messenger_bot_get_started_enabled: Optional[bool] = field()
    is_messenger_platform_bot: Optional[bool] = field()
    is_owned: Optional[bool] = field()
    is_permanently_closed: Optional[bool] = field()
    is_published: Optional[bool] = field()
    is_unclaimed: Optional[bool] = field()
    is_webhooks_subscribed: Optional[bool] = field()
    leadgen_tos_acceptance_time: Optional[str] = field()
    leadgen_tos_accepted: Optional[bool] = field()
    leadgen_tos_accepting_user: Optional[dict] = field()  # TODO
    link: Optional[str] = field()
    location: Optional[Location] = field()
    members: Optional[str] = field()
    merchant_id: Optional[str] = field()
    merchant_review_status: Optional[str] = field()
    messenger_ads_default_icebreakers: Optional[List[str]] = field()
    messenger_ads_default_page_welcome_message: Optional[dict] = field()
    messenger_ads_default_quick_replies: Optional[List[str]] = field()
    messenger_ads_quick_replies_type: Optional[str] = field()
    mission: Optional[str] = field()
    mpg: Optional[str] = field()
    name: Optional[str] = field(repr=True)
    name_with_location_descriptor: Optional[str] = field()
    network: Optional[str] = field()
    new_like_count: Optional[int] = field()
    offer_eligible: Optional[bool] = field()
    overall_star_rating: Optional[float] = field()
    page_token: Optional[str] = field()
    parent_page: Optional["Page"] = field()
    parking: Optional[PageParking] = field()
    payment_options: Optional[PagePaymentOptions] = field()
    personal_info: Optional[str] = field()
    personal_interests: Optional[str] = field()
    pharma_safety_info: Optional[str] = field()
    phone: Optional[str] = field()
    pickup_options: Optional[List[str]] = field()
    place_type: Optional[str] = field()
    plot_outline: Optional[str] = field()
    preferred_audience: Optional[dict] = field()
    press_contact: Optional[dict] = field()
    price_range: Optional[dict] = field()
    products: Optional[dict] = field()
    promotion_eligible: Optional[bool] = field()
    promotion_ineligible_reason: Optional[dict] = field()
    public_transit: Optional[dict] = field()
    rating_count: Optional[dict] = field()
    recipient: Optional[dict] = field()
    record_label: Optional[dict] = field()
    release_date: Optional[dict] = field()
    restaurant_services: Optional[PageRestaurantServices] = field()
    restaurant_specialties: Optional[PageRestaurantSpecialties] = field()
    schedule: Optional[str] = field()
    screenplay_by: Optional[str] = field()
    season: Optional[str] = field()
    single_line_address: Optional[str] = field()
    starring: Optional[str] = field()
    start_info: Optional[PageStartInfo] = field()
    store_code: Optional[str] = field()
    store_location_descriptor: Optional[str] = field()
    store_number: Optional[int] = field()
    studio: Optional[str] = field()
    supports_donate_button_in_live_video: Optional[bool] = field()
    supports_instant_articles: Optional[bool] = field()
    talking_about_count: Optional[int] = field()
    temporary_status: Optional[str] = field()
    unread_message_count: Optional[int] = field()
    unread_notif_count: Optional[int] = field()
    unseen_message_count: Optional[int] = field()
    username: Optional[str] = field()
    verification_status: Optional[str] = field()
    voip_info: Optional[VOIPInfo] = field()
    website: Optional[str] = field()
    were_here_count: Optional[int] = field()
    whatsapp_number: Optional[str] = field()
    written_by: Optional[str] = field()

    # common connection
    picture: Optional[Picture] = field()
