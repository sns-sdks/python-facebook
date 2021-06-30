"""
    Exceptions for library
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Ex:
    pass


class PyFacebookException(Exception):
    pass
