class ProfilingError(Exception):
    """Base exception for profiling errors."""
    pass


class UnsupportedDatasetError(ProfilingError):
    """Raised when unsupported data is sent for profiling."""
    pass