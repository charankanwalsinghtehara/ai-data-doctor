class CleaningError(Exception):
    """Base exception for cleaning errors."""
    pass


class UnsupportedCleaningDataError(CleaningError):
    """Raised when unsupported data is provided."""
    pass