"""Snippet for Spec converter"""

from __future__ import annotations
from .base import Snippet
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Optional, Tuple

class Spec(Snippet):
    def __init__(self,
                 contents: dict, 
                 auth: Optional[Tuple[str, str]] = None, 
                 remote: bool = False):
        raise NotImplementedError
