"""
    Models for user likes .
    Refer: https://developers.facebook.com/docs/graph-api/reference/user/likes/
    
"""
from dataclasses import dataclass
from typing import List, Optional

from pyfacebook.models.base import BaseModel, field
from pyfacebook.models.extensions import Paging


@dataclass
class Likes(BaseModel):
    """
    A class representing user likes

    """

    id: Optional[str] = field(repr=True, compare=True)
    name: Optional[str] = field(repr=True)
    created_time: Optional[str] = field()
    

@dataclass
class LikesResponse(BaseModel):
    """
    A class representing Likes
    """
    data: List[Likes] = field(repr=True, compare=True)
    paging: Optional[Paging] = field()
