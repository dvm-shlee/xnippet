from typing import Type, Optional, Union
from typing import Literal, Tuple, List
from pathlib import Path
from .manager import Manager
from .fetcher import SnippetsFetcher
from .fetcher import PlugInFetcher
from .fetcher.base import Fetcher
from .snippet import SimpleSnippet
from .snippet import PlugInSnippet
from packaging.version import _Version as VersionType

class Resource:
    def to_dict(self):
        return self.__dict__

ResourceType = Type[Union[Resource, List[Resource]]]

XnippetManagerType = Type[Manager]

StorageMode = Literal['local', 'global']

FetcherType = Type[Fetcher]

SnippetsFetcherType = Type[SnippetsFetcher]

PlugInFetcherType = Type[PlugInFetcher]

SnippetPath = Tuple[Optional[Path], bool]

SnippetMode = Literal[
    'plugin', 'preset', 'spec', 'recipe'
    ]

SimpleSnippetType = Type[SimpleSnippet]

PlugInSnippetType = Type[PlugInSnippet]


__all__ = [
    'ResourceType', 'VersionType',
    'XnippetManagerType', 'StorageMode',
    'FetcherType', 'SnippetsFetcherType', 'PlugInFetcherType', 'SnippetPath', 'SnippetMode',
    'SimpleSnippetType', 
    'PlugInSnippetType', 
    ]