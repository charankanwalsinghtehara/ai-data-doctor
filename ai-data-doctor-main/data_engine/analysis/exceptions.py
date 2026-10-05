class AnalysisError(Exception):
    """Base exception for analysis errors."""
    pass


class UnsupportedAnalysisDataError(AnalysisError):
    """Raised when unsupported data is provided."""
    pass