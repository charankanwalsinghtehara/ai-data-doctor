class IngestionError(Exception):
    """Base exception for ingestion errors."""
    pass


class FileNotFoundError(IngestionError):
    """Raised when the requested file does not exist."""
    pass


class UnsupportedFileTypeError(IngestionError):
    """Raised when the file type is not supported."""
    pass


class InvalidFileError(IngestionError):
    """Raised when the file is invalid."""
    pass


class FileTooLargeError(IngestionError):
    """Raised when the file exceeds the allowed size."""
    pass