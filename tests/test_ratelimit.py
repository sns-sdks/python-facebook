from requests.models import CaseInsensitiveDict
from pyfacebook import RateLimit, PercentSecond


def test_parse_headers():
    headers = CaseInsensitiveDict({"key": "None"})
    assert RateLimit.parse_headers(headers, key="key") is None
    assert RateLimit.parse_headers(headers, key="key-null") is None


def test_app_limit():
    headers = CaseInsensitiveDict(
        {"x-app-usage": '{"call_count":91,"total_cputime":15,"total_time":12}'}
    )
    r = RateLimit()
    r.set_limit(headers)

    assert r.get_limit().total_cputime == 15
    assert r.get_limit().max_percent() == 91
    assert r.get_max_percent() == 91
    assert r.get_sleep_seconds() == 0

    mapping = [PercentSecond(10, 1), PercentSecond(20, 2)]
    assert r.get_sleep_seconds(sleep_data=mapping) == 600

    headers = CaseInsensitiveDict(
        {"x-app-usage": '{"call_count":16,"total_cputime":15,"total_time":12}'}
    )
    r.set_limit(headers)
    assert r.get_sleep_seconds(sleep_data=mapping) == 2


def test_business_limit():
    headers = CaseInsensitiveDict(
        {
            "x-business-use-case-usage": '{"112130216863063":[{"type":"pages","call_count":1,"total_cputime":1,"total_time":1,"estimated_time_to_regain_access":0}]}'
        }
    )

    r = RateLimit()
    r.set_limit(headers)

    assert r.get_limit("112130216863063", "pages").call_count == 1
