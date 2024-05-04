from typing import NewType, Type, Optional, Union
from typing import Literal, Tuple, List
from pathlib import Path
from .manager import Manager
from .fetcher import SnippetsFetcher
from .fetcher.base import Fetcher
from .snippet.base import Snippet
from .snippet import PlugInSnippet
from .snippet import PresetSnippet
from .snippet import RecipeSnippet
from .snippet import SpecSnippet
from .formatter.recipe import Resource    
from packaging.version import _Version as VersionType

ResourceType = Type[Union[Resource, List[Resource]]]

ConfigManagerType = Type[Manager]

StorageMode = Literal['local', 'global']

FetcherType = Type[Fetcher]

SnippetsFetcherType = Type[SnippetsFetcher]

SnippetType = Type[Snippet]

SnippetPath = NewType[
    Tuple[Optional(Path), 
          bool]
    ]

SnippetMode = Literal[
    'plugin', 'preset', 'spec', 'recipe'
    ]

PlugInSnippetType = Type[PlugInSnippet]

PresetSnippetType = Type[PresetSnippet]

RecipeSnippetType = Type[RecipeSnippet]

SpecSnippetType = Type[SpecSnippet]

__all__ = [
    'VersionType',
    'ConfigManagerType', 'StorageMode',
    'FetcherType', 'SnippetsFetcherType', 
    'SnippetType', 'SnippetPath', 'SnippetMode', 'FileSnippetMode', 'ConfigSnippetMode',
    'PlugInSnippetType', 'PresetSnippetType', 'RecipeSnippetType', 'SpecSnippetType', 'ConfigSnippetType'
    ]