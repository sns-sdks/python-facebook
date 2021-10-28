"""
    Exceptions for library
"""


class PyFacebookException(Exception):
    """Base class for exceptions in this module."""

    pass


class LibraryError(PyFacebookException):
    """
    A class for library error template.
    """

    def __init__(self, kwargs: dict):
        self.code = -1  # error code in library inside
        self.message = "exception in library"
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        msg = ",".join(
            [f"{k}={v}" for k, v in self.__dict__.items() if not k.startswith("_")]
        )
        return f"{self.__class__.__name__}({msg})"

    def __str__(self):
        return self.__repr__()


class FacebookError(LibraryError):
    """
    A class representing facebook error response
    Refer: https://developers.facebook.com/docs/graph-api/using-graph-api/error-handling

    Common fields are: message,code,error_subcode,error_user_msg,error_user_title,fbtrace_id
    """

    def __init__(self, kwargs: dict):
        self._data = kwargs
        error = kwargs["error"]
        super().__init__(kwargs=error)


class PyFacebookDeprecationWaring(DeprecationWarning):
    pass
