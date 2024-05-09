class ConfigFileWarning(UserWarning):
    """Custom warning to indicate that a configuration file was not found."""
    pass

class FileExistsWarning(UserWarning):
    """Custom warning to indicate that the configuration file exists, subject to overwrite."""
    pass

class DownloadFailedWarning(UserWarning):
    """Custom warning to indicate that attempt download is failed."""
    pass

class FetchFailedWarning(UserWarning):
    pass

class InvalidApproachWarning(UserWarning):
    """Custom warning to indicate that attemp of invalid approach."""
    pass
    
class ManifestStandardWarning(UserWarning):
    """Warning raised when the manifest does not comply with the required standards.

    This warning is used to indicate deviations from expected configuration standards
    in the manifest file. It helps in identifying and debugging issues related to
    compliance with predefined specifications or requirements.
    """
    pass

class ConnectionFailedWarning(UserWarning):
    pass