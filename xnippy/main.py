"""Manager module for configuring, loading, or creating configuration files.

This module facilitates the management of configuration settings within the application, 
allowing configurations to be handled internally without file creation unless specifically 
requested by the user through CLI to create them in the home folder.
"""

from __future__ import annotations
import yaml
import shutil
from packaging import version
from pathlib import Path
from .fetcher import PlugInFetcher
from typing import TYPE_CHECKING
from .formatter import PathFormatter
from .formatter import IOFormatter
from .raiser import WarnRaiser
if TYPE_CHECKING:
    from .types import SnippetMode, StorageMode, SnippetPath, PlugInSnippetType
    from .types import PlugInFetcherType, VersionType
    from typing import List, Union, Optional

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
    _config_dir: 'Path'
    _fname: str
    _package_name: str
    _package_version: VersionType
    _fetcher: PlugInFetcherType
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
        self._default_dir = self._resolve(package__file__).parent / config_path if config_path else self._resolve(package__file__).parent
        self._local_dir = self._resolve(Path.cwd() / f'.{self._package_name}')
        self._global_dir = self._resolve(self._home_dir / f'.{self._package_name}')
        self._fname = config_filename
        self._package_version = version.parse(package_version)
        self.reload()

    ## Initiation step
    def reload(self) -> None:
        """Loads an existing configuration file or creates a new one if it does not exist, filling the 'config' dictionary with settings."""
        self._set_config_dir()
        config_file = self.config_dir / self._fname
        if not config_file.exists() and self.config_dir == self._default_dir:
            
            comment = "Preparing default configuration. Use 'create_config' method to initialize."
            WarnRaiser(self.reload).config_not_found(self.config_dir, comment=comment)
            config_file = self._resolve(__file__).parent / 'yaml/config.yaml'
        with open(config_file, 'r') as f:
            self.config = yaml.safe_load(f)
        self._reload_plugin_fetcher()
        
    def _set_config_dir(self):
        if isinstance(self.config_created, list):
            self._config_dir = self._local_dir
        elif isinstance(self.config_created, str):
            self._config_dir = self._local_dir if self.config_created == 'local' else self._global_dir
        else:
            self._config_dir = self._default_dir

    def _reload_plugin_fetcher(self) -> None:
        """Retrieves a configured SnippetsFetcher for the specified mode to handle fetching of snippets.

        Args:
            mode (str): The mode that determines which type of fetcher to return. Valid modes are 'plugin', 'preset', 'spec', and 'recipe'.

        Returns:
            SnippetsFetcher: A fetcher configured for fetching snippets of the specified type.
        """
        self._fetcher = PlugInFetcher(repos=self.config['xnippy']['repo'],
                                      package_name=self._package_name,
                                      package_version=self._package_version,
                                      path=self._check_dir())
    
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
        return self._config_dir
        
    def create_config(self, target: StorageMode = 'local', 
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
                WarnRaiser(self.create_config).config_exist_when_create()
                return False
        with open(config_file, 'w') as f:
            yaml.safe_dump(self.config, f, sort_keys=False)
        self.reload()
    
    def delete_config(self, target: StorageMode, yes: bool = False):
        path = self._local_dir if target == 'local' else self._global_dir
        removed = False
        if path.exists():
            if yes:
                shutil.rmtree(path)
                removed = True
            elif IOFormatter.yes_or_no(f'**Caution**: You are about to delete the entire configuration folder at [{path}].\n'
                                       'Are you sure you want to proceed?'):
                shutil.rmtree(path)
                removed = True
        if removed:
            self.reload()
    
    def _check_dir(self) -> SnippetPath:
        """Checks and prepares the directory for the specified snippet type, ensuring it exists.

        Returns:
            Tuple[Path, bool]: A tuple containing the path to the directory and a cache flag indicating
                                if caching is necessary (True if so).
        """
        path, cache = (self.config_dir / 'plugin', False) if self.config_created else (None, True)
        if path and not path.exists():
            path.mkdir()
        return path, cache
        
    @property
    def avail(self) -> List[PlugInSnippetType]:
        """Check list of plugins not installed but available in remote repository"""
        installed = [f'{p.name}=={str(p.version)}' for p in self.installed]
        return [p for p in self._fetcher.remote if f'{p.name}=={str(p.version)}' not in installed]
    
    @property
    def installed(self) -> List[PlugInSnippetType]:
        """Check list of installed plugins."""
        return self._fetcher.local
    
    def get(self, plugin_name: str, 
            plugin_version: Optional[str] = None, 
            remote: bool = False) -> Union[PlugInSnippetType, List[PlugInSnippetType], None]:
        """Return PlugInSnippet object."""
        if plugin_version:
            keyword = f'{plugin_name}=={plugin_version}'
            if remote:
                get_from = {f'{s.name}=={str(s.version)}':s for s in self.avail}
            else:
                get_from = {f'{s.name}=={str(s.version)}':s for s in self.installed}
            if keyword in get_from.keys():
                return get_from[keyword]
            return None
        keyword = plugin_name
        return [s for s in self.installed if keyword == s.name]
    
    def is_installed(self, plugin_name: str, version: Optional[str] = None):
        return True if self.get(plugin_name, version) else False
    
    def install(self, plugin_name: str, 
                plugin_version: Optional[str] = None, 
                yes: bool = False, target: StorageMode = 'local'):
        if not self.config_created:
            WarnRaiser(self.install).config_not_found(self.config_dir)
            if yes or IOFormatter.yes_or_no(f"Do you want to proceed creating '{target}' configuration?"):
                self.create_config(target=target)
        
        plugin = self.get(plugin_name=plugin_name, plugin_version=plugin_version, remote=True)
        plugin_dir, _ = self._check_dir()
        plugin_name = f'{plugin_name}_{plugin_version}' if plugin_name else plugin_name
        if (plugin_dir / plugin_name).exists():
            WarnRaiser(self.install).file_exist()
            if yes or IOFormatter.yes_or_no(f"Do you want to overwrite plugin '{target}' configuration?"):
                plugin.download(dest=plugin_dir, force=yes)
                return True
            return False
        plugin.download(dest=plugin_dir)
        self.reload()
