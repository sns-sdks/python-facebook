import json
import logging
from collections import defaultdict
from six import iteritems

from attr import attrs, attrib
from typing import List, Optional
from requests.models import CaseInsensitiveDict

try:
    from json.decoder import JSONDecodeError  # pragma: no cover
except ImportError:  # pragma: no cover
    JSONDecodeError = ValueError  # pragma: no cover

logger = logging.getLogger(__name__)


@attrs
class PercentSecond(object):
    """
    This is a data class for percent and sleep seconds mapping.
    """
    percent = attrib(type=int)
    seconds = attrib(type=int)


@attrs
class RateLimitData(object):
    """
    This A class representing the rate limit data.
    Refer: https://developers.facebook.com/docs/graph-api/overview/rate-limiting#headers
    """
    call_count = attrib(default=0, type=int)
    call_volume = attrib(default=0, type=int)
    cpu_time = attrib(default=0, type=int)
    total_cputime = attrib(default=0, type=int)
    total_time = attrib(default=0, type=int)
    type = attrib(default=None, type=Optional[str])
    estimated_time_to_regain_access = attrib(default=None, type=Optional[str])

    def max_percent(self):
        return max(self.call_count, self.total_cputime, self.total_time)


class RateLimit(object):
    """
    app's rate limit message.
    Refer: https://developers.facebook.com/docs/graph-api/overview/rate-limiting#application-level-rate-limiting
    """
    DEFAULT_TIME_WINDOW = 60 * 60

    def __init__(self):
        """
        Instantiates the RateLimitObject. Takes a json dict as
        kwargs and maps to the object's dictionary. So for something like:

        {
            "app": {
                "call_count": 10,
                "total_cputime": 5,
                "total_time": 4,
            },
            "business: {
                "business-object-id": {
                    "rate-limit-type": {
                        "call_count": 10,
                        "total_cputime": 5,
                        "total_time": 4,
                        "type": "pages",
                        "estimated_time_to_regain_access": 0
                    }
                }
            }
        }

        The RateLimit object will have an attribute 'resources' from which you
        can perform a lookup like:
            api.rate_limit.get_limit()
        or:
            api.rate_limit.get_limit(object_id="123456", endpoint="pages")
        and a RateLimitData instance will be returned.
        """
        self.resources = {
            "app": RateLimitData(),
            "business": defaultdict(lambda: defaultdict(RateLimitData))
        }

    @staticmethod
    def parse_headers(headers, key):
        # type: (CaseInsensitiveDict, str) -> Optional[dict]
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
            except (TypeError, JSONDecodeError) as ex:
                logger.error("Exception in parse {0} data error. Usage is: {1}. errors: {2}".format(key, usage, ex))
                return None
        return None

    def set_limit(self, headers):
        # type: (CaseInsensitiveDict) -> None
        """
        Get rate limit data from response headers. And update to instance.
        :param headers: Response headers
        :return: None
        """
        app_usage = self.parse_headers(headers, "x-app-usage")
        if app_usage is not None:
            self.resources["app"] = RateLimitData(**app_usage)

        business_usage = self.parse_headers(headers, "x-business-use-case-usage")
        if business_usage is not None:
            for business_id, items in iteritems(business_usage):
                for item in items:
                    self.resources["business"][business_id][item["type"]] = RateLimitData(**item)

    def get_limit(self, object_id=None, endpoint=None):
        # type: (Optional[str], Optional[str]) -> RateLimitData
        """
        Get a RateLimitData object for given type.
        :param object_id: business object id
        :param endpoint: rate limit type
        :return: RateLimitData object containing rate limit information.
        """
        if all([object_id, endpoint]):
            return self.resources["business"][object_id][endpoint]

        return self.resources["app"]

    def get_max_percent(self):
        # TODO only check app usage now.
        app_usage = self.resources["app"]
        percent = app_usage.max_percent()
        return percent

    def get_sleep_seconds(self, sleep_data=None):
        # type: (Optional[List[PercentSecond]]) -> int
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
        # Default sleep seconds is 2
        return 2
