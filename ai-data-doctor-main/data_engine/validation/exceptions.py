class ValidationError(Exception):
    """Base exception for validation errors."""
    pass


class FileValidationError(ValidationError):
    """Raised when file validation fails."""
    pass


class DatasetValidationError(ValidationError):
    """Raised when dataset validation fails."""
    pass


class SecurityValidationError(ValidationError):
    """Raised when security validation fails."""
    pass