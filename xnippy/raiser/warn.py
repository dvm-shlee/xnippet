"""This module provide several warning cases and pre-written message to use xnippy easy to handle cases
"""
from __future__ import annotations
from functools import partial
from warnings import warn
from .types import *
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Any
    from typing import Optional


class Warn:
    def __init__(self, 
                 object: Any, 
                 stacklevel: int = 1):
        self._warn = partial(warn, stacklevel=stacklevel, source=object)
    
    def _wrap_message(self, message:str, comment: Optional[str] = None):
        return f"{message} {comment}" if comment else message
    
    def custom(self, message: str, category: Warning = UserWarning):
        return self._warn(message=message, category=category)
        
    def config_not_found(self, config_dir: str, comment: Optional[str] = None) -> None:
        """Handles the absence of a configuration file by preparing a default configuration.

        Args:
            config_dir (str): The path to the directory where the configuration file is expected.

        Raises:
            ConfigNotFound: Warns that the configuration file was not found and defaults are being used.
        """
        message = f"Configuration file not found in '{config_dir}'. " \
                  "Preparing Xnippy's default configuration. Use 'create_config' method to initialize."
        return self._warn(message=self._wrap_message(message, comment), category=ConfigNotFound)
    
    def config_exist_when_create(self, comment: Optional[str] = None):
        message = "Config folder already exists, Skipping creation. Use 'force' argument to overwrite."
        return self._warn(message=self._wrap_message(message, comment), category=FileExistsWarning)
    
    def file_exist(self, filename: str, comment: Optional[str] = None):
        message = f"File '{filename}' already exists."
        return self._warn(message=self._wrap_message(message, comment), category=FileExistsWarning)

    def download_failed(self, comment: Optional[str] = None):
        message = "Download failed."
        return self._warn(message=self._wrap_message(message, comment), cateroty=DownloadFailedWarning)
    
    def invalid_approach(self, comment: Optional[str] = None):
        message = "Invalid approach."
        return self._warn(message=self._wrap_message(message, comment), cateroty=DownloadFailedWarning)
    
        
        

