class UnsupportedPlatformError(Exception):
    """Raised when the platform or architecture is unsupported."""
    pass

class InitialisationError(Exception):
    """Raised when the creation of a new client fails."""
    pass
