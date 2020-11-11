from attr import attrs, attrib
from typing import Optional

__all__ = [
    "PyFacebookError", "ErrorCode", "ErrorMessage",
    "PyFacebookException", "PyFacebookDeprecationWaring"
]


class PyFacebookError(Exception):
    """ Base class for PyFacebook errors"""

    @property
    def message(self):
        """ return the error's first arg """
        return self.args[0]  # pragma: no cover


class ErrorCode:
    HTTP_ERROR = 10000
    MISSING_PARAMS = 10001
    INVALID_PARAMS = 10002
    NOT_SUPPORT_METHOD = 10010


@attrs
class ErrorMessage(object):
    code = attrib(default=None, type=Optional[str])
    message = attrib(default=None, type=Optional[str])
    error_type = attrib(default="PyFacebookException", type=Optional[str])


class PyFacebookException(Exception):
    """
    Library exception class.

    Show internal error and api response error.
    """

    def __init__(self, data):
        self.message = None
        self.type = None
        self.code = None
        self.fbtrace_id = None
        self.error_type = None
        self.initial(data)

    def initial(self, data):
        """
        Args:
             data (dict,ErrorMessage):
                1. Internal error data is an instance of ErrorMessage.
                2. Api response error is dict.
                   Refer: https://developers.facebook.com/docs/graph-api/using-graph-api/error-handling
        """
        if isinstance(data, ErrorMessage):
            self.message = data.message
            self.error_type = data.error_type
            self.type = data.error_type
            self.code = data.code
        elif isinstance(data, dict):
            self.error_type = "FacebookException"
            self.message = data.get("message")
            self.type = data.get("type")
            self.code = data.get("code")
            self.fbtrace_id = data.get("fbtrace_id")

    def __repr__(self):
        return (
            "{0}(code={1},type={2},message={3})".format(
                self.error_type, self.code, self.type, self.message
            )
        )

    def __str__(self):
        return self.__repr__()


class PyFacebookDeprecationWaring(DeprecationWarning):
    pass
