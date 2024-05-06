"""Provides a PlugInSnippet class that allows for plugin source code or code loaded in memory
to be imported as a Python module. This extends the functionality of the brkraw module at the
application level.

This class facilitates the quick testing of code without the need for environment setup for plugin downloads.

Changes:
    2024.5.1: Initial design and implementation of the PlugIn Snippet architecture

Author: Sung-Ho Lee (shlee@unc.edu)
"""

from __future__ import annotations
import re
import yaml
import inspect
from pathlib import Path
from tqdm import tqdm
from .base import Snippet
from xnippy.raiser import WarnRaiser
from xnippy.module import ModuleLoader
from xnippy.module import ModuleInstaller
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Tuple, Dict, Optional, Union
    

class PlugIn(Snippet):
    """Handles the inspection and management of plugins, either locally or from remote sources.
    
    This class supports dynamic loading of plugins into memory for immediate use without the need for disk storage,
    facilitating rapid development and testing of plugin functionalities.
    
    Attributes:
        _contents: Dict = {"path": path of currnet plugin,
                           "files": list of paths or download urls of file contents,
                           "dirs": list of paths or access urls of diretory contents}
    """
    _required_key: list = ['plugin', 'source', 'dependencies'] #, 'package']
    _remote: bool
    _activated: bool
    _dependencies_tested: bool = False 
    _auth: Tuple[str, str]
    _data: Dict = {}
    _contents: Dict
    _repository: Optional[str]
    _include: Dict = {}
    
    def __init__(self, 
                 contents: dict, 
                 auth: Optional[Tuple[str, str]] = None, 
                 remote: bool = False,
                 repository: Optional[str] = None):
        """Initializes the plugin with specified contents, authentication for remote access, and remote status.

        Args:
            contents (dict): Contains keys of path, dirs, and files, similar to os.walk but structured as a dictionary.
                             Each directory and file is also mapped as a key (filename) to a value (path or download_url).
            auth (Tuple[str, str], optional): Credentials for using the GitHub API if needed.
            remote (bool): True if the plugin is loaded remotely, False otherwise.
        """
        self._auth = auth
        self._contents = contents
        self._remote = remote
        self._repository = repository if remote else None
        self._content_parser()

    ## Preparation step: starts
    def _content_parser(self):
        """Parses the contents of the plugin based on its current state (local or remote).

        This method sets the plugin's parameters and determines its validity based on the availability
        and correctness of the required data.
        """
        if len(self._contents['files']) == 0:
            self.is_valid = False
            return None
        self._parse_files()
        self._set_params()
        
    def _parse_files(self):
        """Parse manifest from contents and load."""
        for filename, file_loc in self._contents['files'].items():
            if filename.lower() == 'manifest.yaml':
                self._load_manifest(file_loc)
            
    def _load_manifest(self, file_loc: Union[str, Path]):
        """Loads the plugin's manifest from a remote URL.

        Args:
            download_url (str): The URL from which to download the manifest.

        This method fetches and parses the plugin's manifest file, setting flags based on the contents.
        """
        if self._remote:
            bytes_data = b''.join(self._download_buffer(file_loc, auth=self._auth))
            self._manifest = yaml.safe_load(bytes_data)
        else:
            with open(file_loc, 'r') as f:
                self._manifest = yaml.safe_load(f)
        if any(k not in list(self._manifest.keys()) for k in self._required_key):
            comment = ["Please verify the manifest file's structure. Ensure it includes all required keys: ",
                       "'package', 'plugin', 'source', 'dependencies'. For more details, refer to the documentation: ",
                       "https://github.com/xoani/xnippy/blob/master/examples/docs/PLUGIN.md"]
            WarnRaiser('self._load_manifest').compliance_warning(comment=''.join(comment))
            self.is_valid = False
        else:
            self.is_valid = True
            
    def _set_params(self):
        try:
            info = self._manifest['plugin']
            self.parse_version(info['version'])
            self.name = info['name']
            self.package = info['package'] if 'package' in info.keys() else None
            self.is_valid = True
        except (KeyError, AttributeError):
            self.is_valid = False
        self._activated = False if self._remote else True
    ## Preperation step: ends

    ## Execution step: starts
    def run(self, skip_dependency_check: bool = False, *args, **kwargs):
        """Sets the plugin's parameters and ensures dependencies are resolved and the module is loaded.

        This method acts as a setup routine by testing dependencies, downloading necessary files,
        and dynamically importing the module and call module with given input arguments.

        Args:
            skip_dependency_check (bool): If True, skips the dependency check.
            *args: Variable length argument list for the dynamically imported module.
            **kwargs: Arbitrary keyword arguments for the dynamically imported module.

        Returns:
            The result of calling the imported module with provided arguments.

        Raises:
            ValueError: If the provided arguments do not match the required function signature.
        """
        if not self._activated:
            self.download()
        sig = inspect.signature(self._imported_object)
        try:
            # This will raise a TypeError if the arguments do not match the function signature
            sig.bind(*args, **kwargs)
        except TypeError as e:
            raise TypeError(f"Argument mismatch for the imported module: {e}")
        if not self._dependencies_tested and not skip_dependency_check:
            self.resolve_dependencies()
        return self._imported_object(*args, **kwargs)
    
    ## execution start
    def download(self, dest: Optional[Path] = None, force: bool = False):
        """Downloads the plugin to a specified destination or loads it directly into memory if no destination is provided.
        This method also checks if the file already exists at the destination and optionally overwrites it based on the 'force' parameter.

        Args:
            dest (Path, optional): The file system destination where the plugin files will be saved.
                                If None, files are loaded into memory.
            force (bool, optional): If True, existing files at the destination will be overwritten.
                                    Defaults to False.
        """
        if not self._remote:
            WarnRaiser(self._activated).download_failed(comment="The plugin is already available locally and cannot be downloaded again.")
            return False
        print(f"\n++ Downloading remote module to '{dest or 'memory'}'.")
        files = self._contents['files'] if dest else self._get_module_files()
        for filename, download_url in tqdm(files.items(), desc=' -Files', ncols=80):
            if dest:
                # The plugin will be downloaded on the folder with the name
                plugin_path: Path = (Path(dest).resolve() / f'{self.name}_{str(self.version)}')
                plugin_path.mkdir(exist_ok=True)
                plugin_file: Path = plugin_path / filename
                if plugin_file.exists() and not force:
                    WarnRaiser(self.download).file_exist(filename, comment="Skipping download. Use 'force=True' to overwrite.")
                    continue
                with open(plugin_file, 'wb') as f:
                    for chunk in self._download_buffer(download_url, auth=self._auth):
                        f.write(chunk)
            else:
                # When downloading to memory
                self._data[filename] = b''.join(self._download_buffer(download_url, auth=self._auth))
                self._activated = True  # Mark the module as loaded
    
    def resolve_dependencies(self):
        """Checks and installs any missing dependencies specified in the plugin's manifest file."""
        ptrn = r'(\w+)\s*(>=|<=|==|!=|>|<)\s*([0-9]+(?:\.[0-9]+)*)?'
        deps = self._manifest['dependencies']
        print(f"++ Resolving python module dependencies...\n  -> {deps}")
        for module in tqdm(deps, desc=' -Dependencies', ncols=80):
            if matched := re.match(ptrn, module):
                self._status = None
                module_name, version_constraint, version = matched.groups()
                ModuleInstaller().install(module_name=module_name,
                                          version_constraint=version_constraint, 
                                          version=version)
        self._dependencies_tested = True

    def _get_module_files(self):
        return {f:url for f, url in self._contents['files'].items() if f.endswith('.py')} 
    
    @property
    def _imported_object(self):
        """Dynamically imports the module from loaded data.

        This method uses the information from the manifest to import the specified module and method dynamically.

        Returns:
            The imported method from the module.
        """
        # run include dependency
        include = self._manifest['source']['include']
        if isinstance(include, str):
            include = [include]
        for filename in include:
            if filename.endswith('.py'):
                mloc = self._data[filename] if self._remote else self._contents['files'][filename]
                loader = ModuleLoader(mloc)
                module_name = filename.replace(".py", "")
                module = loader.get_module(module_name)
                self._include[module_name] = module
        
        # load entry point
        source = self._manifest['source']['entry_point']
        ptrn = r'(?P<filename>[a-zA-Z0-9_-]+\.py)(?::(?P<target>[a-zA-Z][a-zA-Z0-9\_\-]*))?'
        if matched := re.match(ptrn, source):
            filename, target = matched.groups()
            mloc = self._data[filename] if self._remote else self._contents['files'][filename]
            loader = ModuleLoader(mloc)
            module = loader.get_module(self.name)
            self._include[self.name] = module
            return getattr(module, target)
        
    def __repr__(self):
        if self.is_valid:
            repr = f"PlugInSnippet<{self.package}>::{self.name}=={self.version}"
            if self._remote:
                repr += '+InMemory' if self._activated else f'+Remote[{self._repository}]'
            return repr
        else:
            return "PlugInSnippet<?>::InValidPlugin"
