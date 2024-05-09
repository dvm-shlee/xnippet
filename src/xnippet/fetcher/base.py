"""Provides a base Fetcher class for accessing and manipulating content from remote repositories.

This module is designed to facilitate the retrieval of repository data, specifically from GitHub,
by providing methods to authenticate, fetch, and traverse directories. It integrates direct
API requests to handle repository contents and provides utility functions for downloading files
and walking through repository directories recursively.

Classes:
    Fetcher: A base class for fetching content from remote repositories with GitHub API integration.
"""

from __future__ import annotations
import re
import logging
import warnings
import requests
from xnippet.formatter import PathFormatter
from xnippet.raiser import WarnRaiser
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Optional, Union
    from typing import List, Tuple, Generator
    from logging import Logger

class Fetcher(PathFormatter):
    """Base class for fetching remote content with methods to authenticate and navigate repositories.

    The Fetcher class extends the functionality of PathResolver to include methods that handle
    the authentication and retrieval of data from remote GitHub repositories. It provides
    utilities to walk through repository directories, fetch file and directory contents,
    and download files as needed.

    Attributes:
        _auth (Union[List[Tuple[str, str]], Tuple[str, str]]): Authentication credentials for the repository.
        repos (dict): Configuration for the repositories to be accessed.
    """
    _auth: Union[List[Tuple[str, str]], Tuple[str, str]]
    _repos: dict
    _logger: Logger = logging.getLogger(__name__)
    
    @staticmethod
    def is_connected():
        """Check if there is an internet connection available by pinging a known URL.

        Returns:
            bool: True if the connection is successful, False otherwise.
        """
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", UserWarning)
                Fetcher._fetch_from_url("https://api.github.com") # this will get status code 403
        except (requests.ConnectTimeout, requests.ConnectionError, requests.RequestException) as e:
            WarnRaiser(Fetcher.is_connected).connection_failed(comment=e)
            return False
        return True
    
    def _set_auth(self):
        """Set up authentication credentials for accessing configured repositories.

        Extracts and sets authentication details for each repository from the provided configurations.
        """
        if isinstance(self._repos, list):
            self._auth = [self._fetch_auth(repo) for repo in self._repos]
    
    @staticmethod
    def _fetch_auth(repo_dict: dict):
        """Fetch authentication credentials from a repository configuration.

        Args:
            repo_dict (dict): Repository configuration containing 'auth' fields.

        Returns:
            Optional[Tuple[str, str]]: A tuple containing username and token if both are present, otherwise None.
        """
        if 'auth' in repo_dict:
            username = repo_dict['auth']['username']
            token = repo_dict['auth']['token']
            return (username, token) if username and token else None
        return None
    
    @staticmethod
    def _walk_github_repo(repo_url: dict, path: Optional['str'] = None, auth: Optional[Tuple[str, str]] = None):
        """Recursively walk through directories in a GitHub repository to fetch directory and file structure.

        Args:
            repo_url (dict): URL of the GitHub repository.
            path (Optional[str]): Specific path in the repository to start the walk.
            auth (Tuple[str, str]): Authentication credentials for accessing the repository.

        Yields:
            dict: A dictionary containing 'path', 'dirs', and 'files' with their respective URLs.
        """
        Fetcher._logger.debug(" + Entered to Fetcher._walk_github_repo")
        Fetcher._logger.debug(" - repo_url: %s. path: %s, auth=%s", repo_url, path, True if auth else False)
        base_url = Fetcher._decode_github_repo(repo_url=repo_url, path=path)
        return Fetcher._walk_dir(url=base_url, auth=auth)
    
    @staticmethod
    def _walk_dir(url, path='', auth: Optional[Tuple[str, str]] = None):
        """Walk through a specific directory in a repository.

        Args:
            url (str): URL of the directory to walk through.
            path (str): Path relative to the repository root.
            auth (Tuple[str, str]): Authentication credentials for accessing the repository.

        Yields:
            dict: A dictionary containing the path, directories, and files within the directory.
        """
        Fetcher._logger.debug(" + Entered to Fetcher._walk_dir_repo, auth=%s", True if auth else False)
        if contents := Fetcher._fetch_from_url(url=url, auth=auth):
            Fetcher._logger.debug(" - Fetched contents from url: %s", url)
            dirs, files = Fetcher._fetch_directory_contents(contents.json())
            yield {'path':path, 
                    'dirs':{d['name']:d['url'] for d in dirs}, 
                    'files':{f['name']:f['download_url'] for f in files}}

            for dir in dirs:
                new_path = f"{path}/{dir['name']}" if path else dir['name']
                new_url = dir['url']
                yield from Fetcher._walk_dir(url=new_url, path=new_path, auth=auth)
    
    @staticmethod
    def _fetch_directory_contents(contents):
        """Categorize contents of a directory into subdirectories and files.

        Args:
            contents (list): List of contents from a directory.

        Returns:
            tuple: A tuple containing lists of directories and files.
        """
        logger = Fetcher._logger
        logger.debug(" + Fetching contents in directory, and classify them into dirs and files")
        dirs, files = [], []
        for item in contents:
            if item['type'] == 'dir':
                dirs.append(item)
            elif item['type'] == 'file':
                files.append(item)
            logger.debug("  + itemName: %s, type: %s", item['name'], item['type'])
        logger.debug("  :: dirs: %s, files: %s", [d['name'] for d in dirs], [f['name'] for f in files])
        return dirs, files
    
    @staticmethod
    def _decode_github_repo(repo_url: dict, path: Optional['str'] = None):
        """Decode a GitHub repository URL to construct an API endpoint URL.

        Args:
            repo_url (dict): The GitHub repository URL.
            path (Optional[str]): An optional path within the repository.

        Returns:
            str: A constructed API endpoint URL based on the repository details.
        """
        ptrn_github = r'https://(?:[^/]+\.)?github\.com/(?P<owner>[^/]+)/(?P<repo>[^/.]+)(?:\.git)?(?:/(?P<path>.*))?'
        if matched := re.match(ptrn_github, repo_url):
            Fetcher._logger.debug(" + Repo URL pattern matched: %s", matched)
            owner = matched['owner']
            repo = matched['repo']
            if matched['path']:
                path_ = matched['path']
                path = '/'.join([path_, path]) if path_ else path
            url = f"https://api.github.com/repos/{owner}/{repo}/contents"
            Fetcher._logger.debug(" - Decoded URL: %s", url)
            return f"{url}/{path}" if path else url
        Fetcher._logger.debug(" + Repo URL pattern does not match: %s", repo_url)
    
    @staticmethod
    def _fetch_from_url(url: str, auth: Tuple[str, str] = None) -> Optional[requests.Response]:
        """Fetch data from a given URL using optional authentication.

        Args:
            url (str): The URL from which to fetch data.
            auth (Tuple[str, str]): Optional authentication credentials.

        Returns:
            Optional[requests.Response]: The response object if successful, otherwise None.
        """
        Fetcher._logger.debug(" + Sending request to %s", url)
        response = requests.get(url, auth=auth)
        Fetcher._logger.debug(" - Request Status Code: %s", response.status_code)
        if response.status_code == 200:
            Fetcher._logger.debug(" - Returning response object.")
            return response
        else:
            warner = WarnRaiser(Fetcher._fetch_from_url)
            comment = [f"Status Code: {response.status_code}"]
            if response.status_code == 403:
                comment.append("This may be due to an incorrect repository address or exceeding the request limit. "
                               "Consider using an API token for authentication.")
                warner.data_fetch_failed(comment=' '.join(comment))
            Fetcher._logger.debug(" - Returning 'None'.")
            return None

    @staticmethod
    def _download_buffer(url: str,
                         chunk_size: int = 8192,
                         auth: Optional[Tuple[str, str]] = None) -> Union[Generator, bool]:
        """Download file content from a URL in buffered chunks.

        Args:
            url (str): The URL of the file to download.
            chunk_size (int): The size of each chunk in bytes.
            auth (Tuple[str, str]): Optional authentication credentials.

        Returns:
            Union[Generator, bool]: A generator yielding file chunks if successful, False on error.
        """
        try:
            Fetcher._logger.debug(" + Downloading %s [ChunkSize: %s ;auth=%s]", url, chunk_size, True if auth else False)
            response = requests.get(url, stream=True, auth=auth)
            response.raise_for_status()
            Fetcher._logger.debug(" - Success")
            return response.iter_content(chunk_size=chunk_size)
        except requests.RequestException as e:
            
            WarnRaiser(Fetcher._download_buffer).custom(f'Error downloading the file: {e}')
            return False
