"""
    Models for common
"""

from dataclasses import dataclass
from typing import List, Optional

from pyfacebook.models.base import BaseModel, field


@dataclass
class VOIPInfo(BaseModel):
    """
    A class representing the VOIP Info.

    Refer: https://developers.facebook.com/docs/graph-api/reference/voip-info/
    """

    has_mobile_app: Optional[bool] = field(repr=True)
    has_permission: Optional[bool] = field(repr=True)
    is_callable: Optional[bool] = field(repr=True)
    is_callable_webrtc: Optional[bool] = field(repr=True)
    is_pushable: Optional[bool] = field(repr=True)
    reason_code: Optional[int] = field(repr=True)
    reason_description: Optional[str] = field(repr=True)


@dataclass
class PagingCursors(BaseModel):
    """
    A class representing the paging cursors.
    """

    after: Optional[str] = field(repr=True)
    before: Optional[str] = field()


@dataclass
class Paging(BaseModel):
    """

    Refer: https://developers.facebook.com/docs/graph-api/using-graph-api/#paging
    """

    cursors: Optional[PagingCursors] = field()
    previous: Optional[str] = field()
    next: Optional[str] = field(repr=True)


@dataclass
class Privacy(BaseModel):
    """
    A class representing the Privacy.

    Refer: https://developers.facebook.com/docs/graph-api/reference/privacy/
    """

    allow: Optional[str] = field()
    deny: Optional[str] = field()
    description: Optional[str] = field()
    friends: Optional[str] = field()
    networks: Optional[str] = field()
    value: Optional[str] = field(repr=True)


@dataclass
class ReactionSummary(BaseModel):
    """
    A class representing
    """

    total_count: Optional[int] = field()
    viewer_reaction: Optional[str] = field()


@dataclass
class Reactions(BaseModel):
    """
    A class representing the Reactions connection.

    Refer: https://developers.facebook.com/docs/graph-api/reference/post/reactions/
    """

    data: Optional[List[dict]] = field()
    paging: Optional[Paging] = field()
    summary: Optional[ReactionSummary] = field(repr=True)
