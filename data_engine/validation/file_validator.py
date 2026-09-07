from pathlib import Path

from .config import (

    SUPPORTED_EXTENSIONS,

    MAX_FILE_SIZE_MB
)

from .exceptions import (
    FileValidationError
)


def validate_file_exists(
    file_path
):
    """
    Check whether the file exists.
    """

    path = Path(
        file_path
    )

    if not path.exists():

        raise FileValidationError(

            f"File does not exist: "
            f"{file_path}"
        )

    if not path.is_file():

        raise FileValidationError(

            f"Path is not a file: "
            f"{file_path}"
        )

    return True


def validate_file_extension(
    file_path
):
    """
    Validate file extension.
    """

    path = Path(
        file_path
    )

    extension = (
        path.suffix.lower()
    )

    if extension not in SUPPORTED_EXTENSIONS:

        supported = ", ".join(
            sorted(
                SUPPORTED_EXTENSIONS
            )
        )

        raise FileValidationError(

            f"Unsupported file type: "
            f"{extension}. "
            f"Supported types: {supported}"
        )

    return extension


def validate_file_size(
    file_path
):
    """
    Validate maximum file size.
    """

    path = Path(
        file_path
    )

    file_size_bytes = (
        path.stat().st_size
    )

    file_size_mb = (
        file_size_bytes
        / (1024 * 1024)
    )

    if file_size_mb > MAX_FILE_SIZE_MB:

        raise FileValidationError(

            f"File size is "
            f"{file_size_mb:.2f} MB. "
            f"Maximum allowed size is "
            f"{MAX_FILE_SIZE_MB} MB."
        )

    return {

        "size_bytes":
            file_size_bytes,

        "size_mb":
            round(
                file_size_mb,
                2
            )
    }


def validate_file(
    file_path
):
    """
    Run complete file validation.
    """

    validate_file_exists(
        file_path
    )

    extension = (
        validate_file_extension(
            file_path
        )
    )

    size_info = (
        validate_file_size(
            file_path
        )
    )

    return {

        "valid": True,

        "file_path":
            str(file_path),

        "extension":
            extension,

        **size_info
    }