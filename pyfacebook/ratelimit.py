import json
import logging
from collections import defaultdict
from dataclasses import dataclass
from json.decoder import JSONDecodeError
from typing import List, Optional

from requests.models import CaseInsensitiveDict

logger = logging.getLogger(__name__)


@dataclass
class PercentSecond(object):
    """
    A class representing for percent and sleep seconds mapping.
    If less percent will sleep seconds.
    """

    percent: int
    seconds: int


@dataclass
class RateLimitHeader(object):
    """
    A class representing the rate limit header.
    Refer: https://developers.facebook.com/docs/graph-api/overview/rate-limiting#headers
    """

    call_count: int = 0
    total_cputime: int = 0
    total_time: int = 0
    call_volume: int = (
        0  # IG basic display has returned this, but have no docs for this.
    )
    cpu_time: int = 0  # IG basic display has returned this, but have no docs for this.
    acc_id_util_pct: int = 0  # only for X-Ad-Account-Usage
    type: Optional[str] = None  # only for Business Use Case Rate Limits
    estimated_time_to_regain_access: Optional[
        str
    ] = None  # only for Business Use Case Rate Limits
    reset_time_duration: Optional[int] = None  # only for X-Ad-Account-Usage
    ads_api_access_tier: Optional[
        str
    ] = None  # for X-Ad-Account-Usage and Business Use Case Rate Limits

    def max_percent(self):
        return max(
            self.call_count,
            self.total_cputime,
            self.total_time,
            self.call_volume,
            self.cpu_time,
            self.acc_id_util_pct,
        )


class RateLimit(object):
    """
    A class representing the rate limit.
    Refer: https://developers.facebook.com/docs/graph-api/overview/rate-limiting
    """

    DEFAULT_TIME_WINDOW = 60 * 60

    def __init__(self):
        """
        Instantiates the RateLimitObject. Takes a json dict as
        kwargs and maps to the object's dictionary. So for something like:

        {
            "app": {
                "call_count": 28,         //Percentage of calls made
                "total_time": 25,         //Percentage of total time
                "total_cputime": 25       //Percentage of total CPU time
            },
            "business: {
                "business-object-id": {
                    "rate-limit-type": {
                        "type": "pages",                          //Type of BUC rate limit logic being applied.
                        "call_count": 100,                        //Percentage of calls made.
                        "total_cputime": 25,                      //Percentage of the total CPU time that has been used.
                        "total_time": 25,                         //Percentage of the total time that has been used.
                        "estimated_time_to_regain_access": 19,    //Time in minutes to regain access.
                        "ads_api_access_tier": "standard_access"  //Tiers allows your app to access the Marketing API. standard_access enables lower rate limiting.
                    }
                }
            },
            ad_account: {
                "acc_id_util_pct": 9.67,   //Percentage of calls made for this ad account.
                "reset_time_duration": 100,   //Time duration (in seconds) it takes to reset the current rate limit score.
                "ads_api_access_tier": 'standard_access'   //Tiers allows your app to access the Marketing API. standard_access enables lower rate limiting.
            }
        }

        The RateLimit object will have an attribute 'resources' from which you
        can perform a lookup like:
            api.rate_limit.get_limit()
        or:
            api.rate_limit.get_limit(object_id="123456", endpoint="pages")
        and a RateLimitHeader instance will be returned.
        """
        self.resources = {
            "app": RateLimitHeader(),
            "business": defaultdict(lambda: defaultdict(RateLimitHeader)),
            "ad_account": RateLimitHeader(),
        }

    @staticmethod
    def parse_headers(headers: CaseInsensitiveDict, key: str) -> Optional[dict]:
        """
        Get rate limit information from header for key.
        :param headers: Response headers
        :param key: rate limit key
        :return:
        """
        usage = headers.get(key)
        if usage:
            try:
                data = json.loads(usage)
                return data
            except JSONDecodeError as ex:
                logger.error(
                    f"Exception in parse {key} data error. Usage is: {usage}. errors: {ex}"
                )
                return None
        return None

    def set_limit(self, headers: CaseInsensitiveDict):
        """
        Get rate limit data from response headers. And update to instance.
        :param headers: Response headers
        :return: None
        """
        app_usage = self.parse_headers(headers, "x-app-usage")
        if app_usage is not None:
            self.resources["app"] = RateLimitHeader(**app_usage)

        business_usage = self.parse_headers(headers, "x-business-use-case-usage")
        if business_usage is not None:
            for business_id, items in business_usage.items():
                for item in items:
                    self.resources["business"][business_id][
                        item["type"]
                    ] = RateLimitHeader(**item)

        ad_account_usage = self.parse_headers(headers, "x-ad-account-usage")
        if ad_account_usage is not None:
            self.resources["ad_account"] = RateLimitHeader(**ad_account_usage)

    def get_limit(
        self,
        object_id: Optional[str] = None,
        rate_limit_type: Optional[str] = None,
        ad_account_limit: bool = False,
    ) -> RateLimitHeader:
        """
        Get a business user case rate limit for object with type or get app rate limit data.

        :param object_id: business object id
        :param rate_limit_type: rate limit type, like pages,instagram,ads_insights...
            All type at https://developers.facebook.com/docs/graph-api/overview/rate-limiting#headers-2
        :param ad_account_limit: Whether to return x-Ad-Account-Usage limit.
        :return: RateLimitHeader object containing rate limit information.
        """
        if all([object_id, rate_limit_type]):
            return self.resources["business"][object_id][rate_limit_type]
        if ad_account_limit:
            return self.resources["ad_account"]
        return self.resources["app"]

    def get_max_percent(self) -> int:
        # TODO Now only check app usage.
        app_usage = self.resources["app"]
        percent = app_usage.max_percent()
        return percent

    def get_sleep_seconds(
        self, sleep_data: Optional[List[PercentSecond]] = None
    ) -> int:
        """
        Get seconds to sleep in requests.

        :param sleep_data:
            the dict for case percent to sleep seconds. ex:
            [
                PercentSecond(percent=20,seconds=2),
                PercentSecond(percent=50,seconds=3),
                PercentSecond(percent=90,seconds=10),
                PercentSecond(percent=100,seconds=1800),
            ]
        :return: sleep seconds
        """
        if isinstance(sleep_data, list):
            max_percent = self.get_max_percent()
            for ps in sleep_data:
                if max_percent <= ps.percent:
                    return ps.seconds
            return 60 * 10  # sleep 10 minutes
        # Default sleep seconds is 0
        return 0
