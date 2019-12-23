"""
    function's to validate parameters.
"""
import logging

from typing import Optional, Union

import pyfacebook


def enf_comma_separated(
        field,  # type: str
        value,  # type: Optional[Union[str, list, tuple, set]]
):
    # type: (...) -> str
    """
    Check to see if field's value type belong to correct type.
    If it is, return api need value, otherwise, raise a PyYouTubeException.

    Args:
        field (str):
            Name of the field you want to do check.
        value (str, list, tuple, set, Optional)
            Value for the field.

    Returns:
        Api needed string
    """
    try:
        if isinstance(value, str):
            return value
        elif isinstance(value, (list, tuple, set)):
            if isinstance(value, set):
                logging.warning("Note: The order of the set is unreliable.")
            return ",".join(value)
        else:
            raise pyfacebook.PyFacebookError({
                "message": "Parameter ({0}) must be single str,comma-separated str,list,tuple or set".format(field),
            })
    except (TypeError, ValueError):
        raise pyfacebook.PyFacebookError({
            "message": "Parameter ({0}) must be single str,comma-separated str,list,tuple or set".format(field),
        })
