class StorageError(Exception):
    """Base exception for storage errors."""
    pass


class ProjectNotFoundError(StorageError):
    """Raised when a project does not exist."""
    pass


class StorageFileError(StorageError):
    """Raised when a storage operation fails."""
    pass