"""Provides functionality to manage and synchronize snippets across local and remote sources.

This module defines a `Snippets` class which aggregates snippets from various sources,
handles their synchronization, and ensures that the snippets are up-to-date according to
user-specified modes (plugin, preset, recipe, schema). It supports operations on snippets
fetched from both local file systems and remote repositories, offering features to check
connectivity, fetch content, and validate snippet integrity.

Classes:
    Snippets: Manages the aggregation and synchronization of snippets based on specified modes.
"""

from __future__ import annotations
import os
import warnings
import logging
from pathlib import Path
from .base import Fetcher
from xnippet.raiser import WarnRaiser
from xnippet.snippet import SimpleSnippet, PlugInSnippet
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Optional
    from typing import List
    from xnippet.types import SimpleSnippetType, SnippetMode, SnippetPath, StorageMode, VersionType
    from logging import Logger
    

class Snippets(Fetcher):
    """Manages the aggregation of snippets from various sources based on the specified mode.

    This class integrates local and remote snippet sources, handling their fetching, storing,
    and updating based on connectivity and cache settings.
    """
    path: Optional[Path]
    mode: SnippetMode
    package_name: str
    package_version: VersionType
    is_cache: bool
    _fetched: bool = False
    _remote_snippets: List[SimpleSnippetType] = []
    _local_snippets: List[SimpleSnippetType] = []
    _logger: Logger = logging.getLogger(__name__)
    
    def __init__(self, 
                 repos: dict,
                 package_name: str,
                 package_version: VersionType,
                 mode: SnippetMode,
                 path: SnippetPath = (None, False)
                 ) -> None:
        """Initializes the Snippets object with specified repository configurations and operational mode.

        Args:
            repos (dict): A dictionary containing repository configurations.
            mode (Literal['plugin', 'preset', 'spec', 'recipe']): The operational mode determining the type of snippets to manage.
            path (Tuple[Optional[Path], bool], optional): A tuple containing the path to local storage and a boolean indicating cache usage.
        """
        self._repos = self._inspect_repos(repos)
        self.package_name = package_name
        self.package_version = package_version
        self.mode = mode
        self.path = self._resolve(path[0]) if path[0] else path[0]
        self.is_cache = path[1]
        self._set_auth()
        self._fetch_local_contents()
        
    @staticmethod
    def _inspect_repos(repos):
        inspected = {}
        for i, repo in enumerate(repos):
            Snippets._logger.debug(" + Check repo id: %d", i)
            name = repo.get('name')
            url = repo.get('url')
            
            if not name or not url:
                message = f" Given repo '{name}' in configuration file does not comply with the expected configuration."
                WarnRaiser(Snippets._inspect_repos).custom(message, UserWarning)
                inspected[name] = None
            else:
                Snippets._logger.debug(" + name: %s, url: %s", name, url)
                inspected[name] = repo

        # Filter out None values and return the list of valid repos
        filtered_repo = [repo for repo in inspected.values() if repo is not None]
        if not filtered_repo:
            message = "No valid repo configurations found; nothing to download."
            WarnRaiser(Snippets._inspect_repos).custom(message, UserWarning)
        return filtered_repo
        
    def _fetch_local_contents(self) -> Optional[list]:
        """Fetches snippets from local storage based on the current mode and path settings.

        Gathers contents from the specified directory and converts them into snippets. This operation
        is skipped if caching mode is enabled. (This means the Xnippet initiated with dedicate space to download Sneppits.)

        Returns:
            Optional[list]: Returns None if caching is enabled, otherwise returns a list of fetched local contents.
        """
        if self.is_cache:
            return None
        contents = []
        for path, dirs, files in os.walk(self.path):
            child = {'path':self._resolve(path), 
                     'dirs':{d:self._resolve(path) / d for d in dirs}, 
                     'files':{f:self._resolve(path) / f for f in files}}
            contents.append(child)
        self._convert_contents_to_snippets([contents], remote=False)
            
    def _fetch_remote_contents(self) -> None:
        """Fetches snippets from remote repositories if connected and not previously fetched.

        Retrieves snippet data from remote sources as specified by the repository configuration
        and converts them into snippet objects. Updates the fetched status upon completion.
        """
        if self._repos:
            if contents := [self._walk_github_repo(repo_url=repo['url'],
                                                   path=repo[self.mode]['path'],
                                                   auth=self._auth[i]) for i, repo in enumerate(self._repos)]:
                self._convert_contents_to_snippets(contents=contents, remote=True)
            self._fetched = True
            
    def _convert_contents_to_snippets(self, contents: list, remote: bool = False) -> None:
        """Converts fetched contents from either local or remote sources into snippet objects.

        Iterates over fetched contents, creating snippet objects which are then stored appropriately
        based on their validation status.

        Args:
            contents (list): List of contents fetched from either local or remote sources.
            remote (bool, optional): Flag indicating whether the contents are from remote sources.
        """
        snippets = []
        for repo_id, content in enumerate(contents):
            for c in content:
                if remote:
                    snippets.append(self._snippet(contents=c, auth=self._auth[repo_id], remote=remote, repository=self._repos[repo_id]['name']))
                    storage = self._remote_snippets
                else:
                    snippets.append(self._snippet(contents=c, remote=remote))
                    storage = self._local_snippets
        for s in snippets:            
            if s.is_valid and s.name not in [s_.name for s_ in storage]:
                storage.append(s)
                        
    @property
    def _snippet(self):
        """Determines the snippet class based on the operational mode.

        Returns:
            Type[Snippet]: Returns the class type corresponding to the operational mode (Plugin, Preset, Schema, Recipe).
        """
        if self.mode == 'plugin':
            return PlugInSnippet
        elif self.mode == 'simple':
            return SimpleSnippet
    
    @property
    def remote(self):
        """Access the remote snippets if available. Fetches the snippets from a remote source if not already fetched
        and if a network connection is available.

        Returns:
            Any: The remote snippets if available and connected, otherwise None.

        Raises:
            Warning: If the connection to fetch remote snippets fails.
        """
        if self._remote_snippets:
            return self._remote_snippets
        else:
            if self.is_connected():
                self._fetch_remote_contents()
                return self._remote_snippets
            else:
                warnings.warn("Connection failed. Please check your network settings.")
                return None
    
    @property
    def local(self):
        self._fetch_local_contents()
        return self._local_snippets

    @property
    def is_up_to_date(self):
        return self._fetched
