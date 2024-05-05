class ConfigNotFound(UserWarning):
    """Custom warning to indicate that a configuration file was not found."""
    pass

class FileExistsWarning(UserWarning):
    """Custom warning to indicate that the configuration file exists, subject to overwrite."""
    pass

class DownloadFailedWarning(UserWarning):
    """Custom warning to indicate that attempt download is failed."""
    pass

class InvalidApproachWarning(UserWarning):
    """Custom warning to indicate that attemp of invalid approach."""