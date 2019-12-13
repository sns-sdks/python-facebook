"""
    These are some models for access token.
"""
from typing import List, Optional
from attr import attrs, attrib


@attrs
class AuthAccessToken(object):
    """
    A class representing the auth access token response.

    Refer: https://developers.facebook.com/docs/facebook-login/manually-build-a-login-flow#confirm
    """

    access_token = attrib(default=None, type=Optional[str])
    token_type = attrib(default=None, type=Optional[str])
    expires_in = attrib(default=None, type=Optional[int])
    expires_at = attrib(default=None, type=Optional[int], repr=False)


@attrs
class TokenError(object):
    """
    A class representing the access token error.

    https://developers.facebook.com/docs/graph-api/reference/v5.0/debug_token#Fields
    """
    code = attrib(default=None, type=Optional[int])
    message = attrib(default=None, type=Optional[str])
    sub_code = attrib(default=None, type=Optional[int], repr=False)


@attrs
class Metadata(object):
    """
    A class representing the access token metadata.

    https://developers.facebook.com/docs/graph-api/reference/v5.0/debug_token#Fields
    """
    sso = attrib(default=None, type=Optional[str])
    auth_type = attrib(default=None, type=Optional[str], repr=False)
    auth_nonce = attrib(default=None, type=Optional[str], repr=False)


@attrs
class GranularScope(object):
    """
    A class representing the access token granular scope.

    https://developers.facebook.com/docs/graph-api/reference/v5.0/debug_token#Fields
    """
    scope = attrib(default=None, type=Optional[str])
    target_ids = attrib(default=None, type=Optional[List[str]], repr=False)


@attrs
class AccessToken(object):
    """
    A class representing the access token.

    Refer: https://developers.facebook.com/docs/graph-api/reference/v4.0/debug_token
    """

    app_id = attrib(default=None, type=Optional[str])
    application = attrib(default=None, type=Optional[str], repr=False)
    type = attrib(default=None, type=Optional[str], repr=False)
    error = attrib(default=None, type=Optional[TokenError], repr=False)
    expires_at = attrib(default=None, type=Optional[int], repr=False)
    data_access_expires_at = attrib(default=None, type=Optional[int], repr=False)
    is_valid = attrib(default=None, type=Optional[bool], repr=False)
    issued_at = attrib(default=None, type=Optional[int], repr=False)
    metadata = attrib(default=None, type=Optional[Metadata], repr=False)
    profile_id = attrib(default=None, type=Optional[str], repr=False)
    scopes = attrib(default=None, type=Optional[List[str]], repr=False)
    granular_scopes = attrib(default=None, type=Optional[List[GranularScope]])
    user_id = attrib(default=None, type=Optional[str], repr=False)
