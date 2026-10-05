class MLError(Exception):
    """Base exception for ML errors."""
    pass


class UnsupportedMLDataError(MLError):
    """Raised when unsupported data is provided."""
    pass


class InvalidTargetError(MLError):
    """Raised when an invalid target is selected."""
    pass


class InsufficientTrainingDataError(MLError):
    """Raised when there is not enough data."""
    pass