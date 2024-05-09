"""
This module provides various warning cases with pre-written messages to facilitate easy handling of cases in xnippy.
"""
from __future__ import annotations
import logging
from functools import partial
from warnings import warn
from .types import *
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Any, Optional, Literal


class Warn:
    def __init__(self, object: Any, stacklevel: int = 1):
        self._warn = partial(warn, stacklevel=stacklevel, source=object)
        self._logger = logging.getLogger(object.__name__)
    
    def _wrap_message(self, message: str, comment: Optional[str] = None):
        self._logger.warning("++ %s %s", message, comment)
        return f"{message} {comment}" if comment else message
    
    def custom(self, message: str, category: Warning = UserWarning):
        return self._warn(message=message, category=category)
        
    def config_file(self, config_dir: str, exists: bool, comment: Optional[str] = None) -> None:
        message = f"Configuration file '{config_dir}' already exists." if exists else f"Configuration file '{config_dir}' not found."
        return self._warn(message=self._wrap_message(message, comment), category=ConfigFileWarning)
    
    def file_exists(self, filename: str, comment: Optional[str] = None):
        message = f"File '{filename}' already exists."
        return self._warn(message=self._wrap_message(message, comment), category=FileExistsWarning)

    def connection_failed(self, comment: Optional[str] = None):
        message = "Connection to repository failed."
        return self._warn(message=self._wrap_message(message, comment), category=ConnectionFailedWarning)

    def data_fetch_failed(self, comment: Optional[str] = None):
        message = "Data fetch operation failed."
        return self._warn(message=self._wrap_message(message, comment), category=FetchFailedWarning)

    def download_error(self, comment: Optional[str] = None):
        message = "Download operation failed."
        return self._warn(message=self._wrap_message(message, comment), category=DownloadFailedWarning)
    
    def invalid_method(self, comment: Optional[str] = None):
        message = "The approach used is invalid."
        return self._warn(message=self._wrap_message(message, comment), category=InvalidApproachWarning)
    
    def manifest_noncompliance(self, comment: Optional[str] = None):
        message = "Manifest file does not meet the required standards."
        return self._warn(message=self._wrap_message(message, comment), category=ManifestStandardWarning)
