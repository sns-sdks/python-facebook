"""
    tests for custom exceptions
"""

from pyfacebook import LibraryError, FacebookError


def test_error():
    error = {
        "message": "Message describing the error",
        "type": "OAuthException",
        "code": 190,
        "error_subcode": 460,
        "error_user_title": "A title",
        "error_user_msg": "A message",
        "fbtrace_id": "EJplcsCHuLu",
    }

    fb_err = FacebookError(error)

    assert fb_err.code == 190
    assert "FacebookError" in repr(fb_err)

    error = {"message": "error message"}
    lib_err = LibraryError(error)

    assert lib_err.code == -1
    assert "LibraryError" in str(lib_err)
