"""
    tests for api base
"""


def test_resource(fb_api):
    assert fb_api.user.access_token == "token"
    assert fb_api.user.app_id == "123456"
    assert fb_api.user.app_secret == "xxxxx"
    assert fb_api.user.client
