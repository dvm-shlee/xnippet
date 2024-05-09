"""BaseSnippet for provide platform for developing Snippet to configure and/or interface with integrated apps's ecosystem.
"""

from __future__ import annotations
import logging
from xnippet.fetcher.base import Fetcher
from typing import TYPE_CHECKING
from packaging.version import parse
if TYPE_CHECKING:
    from packaging.version import _Version as VersionType
    from logging import Logger

class Snippet(Fetcher):
    package_name: str
    package_version: str
    name: str
    version: VersionType
    type: str
    is_valid: bool
    _logger: Logger = logging.getLogger('xnippetSnippet')
    
    def parse_version(self, version_string):
        self.version = parse(version_string)
