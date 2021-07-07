"""
    tests for params utils
"""

import pytest

from pyfacebook import LibraryError
from pyfacebook.utils.params_utils import enf_comma_separated


def test_enf_comma_separated():
    assert enf_comma_separated("fields", "f1") == "f1"
    assert enf_comma_separated("fields", ["f1", "f2"]) == "f1,f2"
    assert enf_comma_separated("fields", ["f1", "f2", "f2"]) == "f1,f2"
    assert enf_comma_separated("fields", ("f1", "f2")) == "f1,f2"

    with pytest.raises(LibraryError):
        enf_comma_separated("id", 1)

    with pytest.raises(LibraryError):
        enf_comma_separated("id", [None, None])
