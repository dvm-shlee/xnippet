from typing import Type, Optional, Union
from typing import Literal, Tuple, List
from pathlib import Path
from .main import Manager
from .fetcher import SnippetFetcher
from .fetcher import PlugInFetcher
from .fetcher.base import Fetcher
from .snippet.base import Snippet
from .snippet import PlugInSnippet
from .snippet import PresetSnippet
from .snippet import RecipeSnippet
from .snippet import SpecSnippet
from packaging.version import _Version as VersionType

class Resource:
    def to_dict(self):
        return self.__dict__

ResourceType = Type[Union[Resource, List[Resource]]]

XnipyManagerType = Type[Manager]

StorageMode = Literal['local', 'global']

FetcherType = Type[Fetcher]

SnippetsFetcherType = Type[SnippetFetcher]

PlugInFetcherType = Type[PlugInFetcher]

SnippetType = Type[Snippet]

SnippetPath = Tuple[Optional[Path], bool]

SnippetMode = Literal[
    'plugin', 'preset', 'spec', 'recipe'
    ]

PlugInSnippetType = Type[PlugInSnippet]

PresetSnippetType = Type[PresetSnippet]

RecipeSnippetType = Type[RecipeSnippet]

SpecSnippetType = Type[SpecSnippet]

__all__ = [
    'ResourceType', 'VersionType',
    'XnipyManagerType', 'StorageMode',
    'FetcherType', 'SnippetsFetcherType', 'PlugInFetcherType',
    'SnippetType', 'SnippetPath', 'SnippetMode',
    'PlugInSnippetType', 
    'PresetSnippetType', 
    'RecipeSnippetType', 
    'SpecSnippetType',
    ]