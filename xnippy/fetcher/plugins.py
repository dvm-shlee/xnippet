from __future__ import annotations
from .snippets import Snippets as SnippetFetcher
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Optional
    from typing import List
    from xnippy.types import SnippetType, SnippetPath, StorageMode

class PlugIns(SnippetFetcher):
    """Manages the aggregation of PlugIn snippets."""
    def __init__(self,
                 repos: List[dict],
                 package_name: str,
                 package_version: str,
                 path: SnippetPath = (None, False)):
        super().__init__(repos=repos, 
                         package_name=package_name, 
                         package_version=package_version, 
                         mode='plugin', 
                         path=path)
        
    