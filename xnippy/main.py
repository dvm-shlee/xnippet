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
from .raiser import WarnRaiser
if TYPE_CHECKING:
    from .types import SnippetMode, StorageMode, SnippetPath, SnippetType
    from .types import SnippetsFetcherType, VersionType
    from typing import List, Dict, Union, Optional

class Xnippy(PathFormatter):
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
                 package__file__: Union['Path', str],
                 config_path: Optional[str] = None,
                 config_filename: str = 'config.yaml') -> None:
        """Initializes the configuration manager.

        This constructor sets up paths for the home directory, global and local configuration directories,
        and configuration file. It ensures the configuration directory exists and loads or creates the
        configuration based on its presence.

        Args:
            tmpdir (Optional[Path]): Temporary directory for storing configurations, defaults to the home directory.
        """
        self._package_name = package_name
        self._home_dir = self._resolve('~')
        self._default_dir = self._resolve(config_path) if config_path else self._resolve(package__file__).parent
        self._local_dir = self._resolve(Path.cwd() / f'.{self._package_name}')
        self._global_dir = self._resolve(self._home_dir / f'.{self._package_name}')
        self._fname = config_filename
        self._package_version = version.parse(package_version)
        self.reload_config()

    def reload_config(self) -> None:
        """Loads an existing configuration file or creates a new one if it does not exist, filling the 'config' dictionary with settings."""
        config_file = self.config_dir / self._fname
        if not config_file.exists() and self.config_dir == self._default_dir:
            warnings.warn(f"Config file is not exists in '{self.config_dir}', preparing Xnippy's default configuration.", 
                          UserWarning)
            config_file = self._resolve(__file__).parent / 'yaml/config.yaml'
        with open(config_file, 'r') as f:
            self.config = yaml.safe_load(f)
        self._reload_fetchers()

    @property
    def config_created(self) -> Union[StorageMode, list[str], bool]:
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
        if isinstance(self.config_created, list):
            return self._local_dir
        elif isinstance(self.config_created, str):
            return self._local_dir if self.config_created == 'local' else self._global_dir
        return self._default_dir
    
    def create_confnig(self, target: StorageMode = 'local', 
                       force: bool = False) -> bool:
        """Creates a configuration file at the specified target location.

        Args:
            target (str): Specifies the target directory ('local' or 'global') for creating the configuration file. Defaults to 'local'.
            force (bool): If set to True, the existing configuration file will be overwritten. Defaults to False.

        Returns:
            bool: Returns True if the file was successfully created, otherwise False.
        """
        config_dir = self._local_dir if target == 'local' else self._global_dir
        config_dir.mkdir(exist_ok=True)
        config_file = config_dir / self._fname
        if config_file.exists():
            if not force:
                WarnRaiser(self.create_confnig).config_exist_when_create()
                return False
        with open(config_dir / self._fname, 'w') as f:
            yaml.safe_dump(self.config, f, sort_keys=False)
    
    def delete_confnig(self, target: StorageMode, yes: bool = False):
        path = self._local_dir if target == 'local' else self._global_dir
        if path.exists():
            if yes:
                shutil.rmtree(path)
            elif IOFormatter.yes_or_no(f'**Caution**: You are about to delete the entire configuration folder at [{path}].\n'
                                       'Are you sure you want to proceed?'):
                shutil.rmtree(path)
    
    def get_fetcher(self, mode: SnippetMode) -> SnippetsFetcherType:
        """Returns the appropriate fetcher based on the specified mode.

        Args:
            mode (str): The mode that determines which type of fetcher to return. Valid modes are 'plugin', 'preset', 'spec', and 'recipe'.

        Returns:
            SnippetsFetcher: An instance of SnippetsFetcher configured to operate in the specified mode.
        """
        return self._fetchers[mode]

    def _get_snippet_fetcher(self, mode: SnippetMode) -> SnippetsFetcherType:
        """Retrieves a configured SnippetsFetcher for the specified mode to handle fetching of snippets.

        Args:
            mode (str): The mode that determines which type of fetcher to return. Valid modes are 'plugin', 'preset', 'spec', and 'recipe'.

        Returns:
            SnippetsFetcher: A fetcher configured for fetching snippets of the specified type.
        """
        return SnippetsFetcher(repos=self.config['plugin']['repo'],
                               mode=mode,
                               path=self._check_dir(mode))
    
    def _check_dir(self, mode: SnippetMode) -> SnippetPath:
        """Checks and prepares the directory for the specified snippet type, ensuring it exists.

        Args:
            mode (str): The mode that determines which type of fetcher to return. Valid modes are 'plugin', 'preset', 'spec', and 'recipe'.

        Returns:
            Tuple[Path, bool]: A tuple containing the path to the directory and a cache flag indicating
                                if caching is necessary (True if so).
        """
        path, cache = (self.config_dir / mode, False) if self.config_created else (None, True)
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
    
    # def download(self, 
    #              mode: SnippetMode, 
    #              snippet_name: str,
    #              snippet_version: str,
    #              destination: Optional[Union[Path, str]] = None):
    #     """Download snippet by name from selected mode"""
    #     if not destination and not self.config_dir.exists():
    #         WarnRaiser(self.download).config_not_found()
    #         return None
        
    #     destination = self._resolve(destination) if destination else (self.config_dir / mode)
    #     destination.mkdir(exist_ok=True)
    #     # check local
    #     fetcher: SnippetsFetcherType = self.get_fetcher[mode]
    #     print(f"++ Fetching avail {mode} snippets from remote repository...")
    #     avail = [s for s in fetcher.remote]
