"""
    function's to validate parameters.
"""

from typing import Optional, Union

from pyfacebook.exceptions import LibraryError


def enf_comma_separated(field: str, value: Optional[Union[str, list, tuple]]):
    """
    Check to see if field's value type belong to correct type.
    If it is, return api need value, otherwise, raise a LibraryError.
    :param field: Name of the field you want to do check.
    :param value: Values for the field.
    :return: Api needed string
    """
    try:
        # if value point with string, not check.
        if isinstance(value, str):
            value = [value]
        elif isinstance(value, (list, tuple)):
            pass
        else:
            raise LibraryError(
                {
                    "message": f"Parameter ({field}) must be single str,comma-separated str,list or tuple",
                }
            )

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
        raise LibraryError(
            {
                "message": f"Parameter ({field}) must be single str,comma-separated str,list or tuple",
            }
        )
