class QualityError(Exception):
    """Base exception for data quality errors."""
    pass


class UnsupportedQualityDataError(QualityError):
    """Raised when unsupported data is sent."""
    pass