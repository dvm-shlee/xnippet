"""Manager module for configuring, loading, or creating configuration files.

This module facilitates the management of configuration settings within the application, 
allowing configurations to be handled internally without file creation unless specifically 
requested by the user through CLI to create them in the home folder.
"""

from __future__ import annotations
import yaml
import shutil
import warnings
from packaging import version
from pathlib import Path
from .fetcher import SnippetsFetcher
from typing import TYPE_CHECKING
from .formatter import PathFormatter
from .formatter import IOFormatter
if TYPE_CHECKING:
    from .types import SnippetMode, StorageMode, SnippetPath, SnippetType
    from .types import SnippetsFetcherType, VersionType
    from typing import List, Dict, Union, Optional

class Manager(PathFormatter):
    """Manages the configuration settings for the application.

    This class ensures the existence of the configuration directory, loads or creates the configuration file,
    sets configuration values, and retrieves configuration values. It operates both globally and locally
    depending on the user's choice and the operational context.
    """ 
    config: dict = {}
    _home_dir: 'Path'
    _default_dir: 'Path'
    _local_dir: 'Path'
    _global_dir: 'Path'
    _fname: str
    _package_name: str
    _package_version: VersionType
    _fetchers: Dict[SnippetsFetcherType] = {}
    _compatible_snippets: List[SnippetMode] = ['plugin']
    
    def __init__(self, 
                 package_name: str, 
                 package_version: str, 
                 package__file__: 'Path',
                 config_filename: Optional[str] = None) -> None:
        """Initializes the configuration manager.

        This constructor sets up paths for the home directory, global and local configuration directories,
        and configuration file. It ensures the configuration directory exists and loads or creates the
        configuration based on its presence.

        Args:
            tmpdir (Optional[Path]): Temporary directory for storing configurations, defaults to the home directory.
        """
        self._package_name = package_name
        self._home_dir = self._resolve('~')
        self._default_dir = self._resolve(package__file__).parent
        self._local_dir = self._resolve(Path.cwd() / f'.{self._package_name}')
        self._global_dir = self._resolve(self._home_dir / f'.{self._package_name}')
        self._fname = config_filename or 'config.yaml'
        self._package_version = version.parse(package_version)
        self.reload()

    @property
    def created(self) -> Union[StorageMode, list[str], bool]:
        """"Checks and returns the location where the configuration folder was created.

        Returns:
            Union[Literal['global', 'local'], list[str], bool]: Returns 'global' or 'local' if the config folder was created at that level,
            a list of locations if multiple exist, or False if no config folder is created.
        """
        created = [(f / self._fname).exists() for f in [self._global_dir, self._local_dir]]
        checked = [loc for i, loc in enumerate(['global', 'local']) if created[i]]
        checked = checked.pop() if len(checked) == 1 else checked
        return checked or False

    @property
    def config_dir(self) -> 'Path':
        """Determines and returns the appropriate configuration directory based on the existence and location of the config file.

        Returns:
            Path: Path to the configuration directory based on its existence and scope (global or local).
        """
        if isinstance(self.created, list):
            return self._local_dir
        elif isinstance(self.created, str):
            return self._local_dir if self.created == 'local' else self._global_dir
        return self._default_dir

    def reload(self) -> None:
        """Loads an existing configuration file or creates a new one if it does not exist, filling the 'config' dictionary with settings."""
        with open(self.config_dir / self._fname) as f:
            self.config = yaml.safe_load(f)
        self._reload_fetchers()
    
    def create(self, target: StorageMode = 'local', 
               force: bool = False) -> bool:
        """Creates a configuration file at the specified location.

        Args:
            target (Literal['local', 'global']): Target directory for creating the configuration file, defaults to 'local'.
            force (bool): If True, overwrites the existing configuration file, defaults to False.

        Returns:
            bool: True if the file was created successfully, False otherwise.
        """
        if not self.config:
            self.load()
        config_dir = self._local_dir if target == 'local' else self._global_dir
        config_dir.mkdir(exist_ok=True)
        config_file = config_dir / self._fname
        if config_file.exists():
            if not force:
                self._warnings_exists()
                return False
        with open(config_dir / self._fname, 'w') as f:
            yaml.safe_dump(self.config, f, sort_keys=False)

    def remove(self, target: StorageMode, yes: bool = False):
        path = self._local_dir if target == 'local' else self._global_dir
        if path.exists():
            if yes:
                shutil.rmtree(path)
            elif IOFormatter.yes_or_no(f'**Caution**: You are about to delete the entire configuration folder at [{path}].\n'
                                       'Are you sure you want to proceed?'):
                shutil.rmtree(path)

    def get_fetcher(self, mode: SnippetMode) -> SnippetsFetcherType:
        """Returns the appropriate fetcher based on the mode.

        Args:
            mode (Literal['plugin', 'preset', 'spec', 'recipe']): The mode determining which type of fetcher to return.

        Returns:
            SnippetsFetcher: An instance of SnippetsFetcher configured for the specified mode.
        """
        return self._fetchers[mode]

    def _get_snippet_fetcher(self, mode: SnippetMode) -> SnippetsFetcherType:
        """Retrieves a configured SnippetsFetcher for the specified mode to handle fetching of snippets.

        Args:
            mode (Literal['plugin', 'preset', 'spec', 'recipe']): The specific category of snippets to fetch.

        Returns:
            SnippetsFetcher: A fetcher configured for fetching snippets of the specified type.
        """
        return SnippetsFetcher(repos=self.config['snippets']['repo'],
                               mode=mode,
                               path=self._check_dir(mode))
    
    def _check_dir(self, type_: SnippetMode) -> SnippetPath:
        """Checks and prepares the directory for the specified snippet type, ensuring it exists.

        Args:
            type_ (Literal['plugin', 'preset', 'spec', 'recipe']): The type of snippet for which the directory is checked.

        Returns:
            Tuple[Path, bool]: A tuple containing the path to the directory and a cache flag indicating
                                if caching is necessary (True if so).
        """
        path, cache = (self.config_dir / type_, False) if self.created else (None, True)
        if path and not path.exists():
            path.mkdir()
        return path, cache
    
    def _reload_fetchers(self):
        for mode in self._compatible_snippets:
            self._fetchers[mode] = self._get_snippet_fetcher(mode)
        
    def avail(self, mode: SnippetMode) -> SnippetsFetcherType:
        fetcher = self.get_fetcher(mode)
        return {'remote': fetcher.remote,
                'local': fetcher.local}
    
    def installed(self, mode: SnippetMode) -> SnippetsFetcherType:
        return self.get_fetcher(mode).local
    
    def is_installed(self, 
                     mode: SnippetMode, 
                     snippet: SnippetType) -> bool:
        return any(s.name == snippet.name for s in self.installed(mode))
    
    def download(self, 
                 mode: SnippetMode, 
                 snippet_name: str,
                 snippet_version: str,
                 destination: Optional[Union[Path, str]] = None):
        """Download snippet by name from selected mode"""
        if not destination and not self.config_dir.exists():
            self._warnings_not_exists()
            return None
        
        destination = self._resolve(destination) if destination else (self.config_dir / mode)
        destination.mkdir(exist_ok=True)
        # check local
        fetcher: SnippetsFetcherType = self.get_fetcher[mode]
        print(f"++ Fetching avail {mode} snippets from remote repository...")
        avail = [s for s in fetcher.remote]
        
    @staticmethod
    def _warnings_exists():
        warnings.warn("Config folder already exists, please use 'force' option if you want overwrite.",
                      UserWarning)
    
    @staticmethod
    def _warnings_not_exists():
        warnings.warn("Config folder does not exist, please use 'create' option if you want create.",
                      UserWarning)