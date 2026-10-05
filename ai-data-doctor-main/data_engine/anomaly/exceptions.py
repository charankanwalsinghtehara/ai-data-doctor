class AnomalyError(Exception):
    """Base exception for anomaly detection."""
    pass


class UnsupportedAnomalyDataError(AnomalyError):
    """Raised when unsupported data is provided."""
    pass