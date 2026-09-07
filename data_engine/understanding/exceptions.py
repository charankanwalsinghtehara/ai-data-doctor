class UnderstandingError(Exception):
    """Base exception for data understanding errors."""
    pass


class UnsupportedDataError(UnderstandingError):
    """Raised when the data cannot be understood."""
    pass