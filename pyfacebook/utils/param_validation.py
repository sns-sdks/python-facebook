"""
    function's to validate parameters.
"""
import logging

from typing import Optional, Union

import pyfacebook

logger = logging.getLogger(__name__)


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
            value = value.split(",")
        elif isinstance(value, (list, tuple)):
            pass
        elif isinstance(value, set):
            logger.warning("Note: The order of the set is unreliable.")
            pass
        else:
            raise pyfacebook.PyFacebookError({
                "message": "Parameter ({0}) must be single str,comma-separated str,list,tuple or set".format(field),
            })

        # loop value list and remove repeat item
        seen = {}
        res = []
        for item in value:
            if item in seen:
                continue
            seen[item] = 1
            res.append(item)
        return ",".join(res)
    except (TypeError, ValueError):
        raise pyfacebook.PyFacebookError({
            "message": "Parameter ({0}) must be single str,comma-separated str,list,tuple or set".format(field),
        })
