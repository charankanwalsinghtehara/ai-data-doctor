class ExtractionError(Exception):
    """Base exception for extraction errors."""
    pass


class ExtractorNotFoundError(ExtractionError):
    """Raised when no extractor exists for a file type."""
    pass


class FileExtractionError(ExtractionError):
    """Raised when extraction fails."""
    pass