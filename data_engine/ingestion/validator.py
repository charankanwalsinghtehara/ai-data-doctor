from pathlib import Path

from .exceptions import (
    FileNotFoundError,
    InvalidFileError,
    FileTooLargeError
)


MAX_FILE_SIZE_MB = 100


def validate_file_exists(file_path):
    """
    Check whether the file exists.
    """

    path = Path(file_path)

    if not path.exists():

        raise FileNotFoundError(
            f"File does not exist: {file_path}"
        )

    return True


def validate_file_is_not_directory(file_path):
    """
    Make sure the path points to a file.
    """

    path = Path(file_path)

    if not path.is_file():

        raise InvalidFileError(
            f"The provided path is not a file: {file_path}"
        )

    return True


def validate_file_not_empty(file_path):
    """
    Check whether the file contains data.
    """

    path = Path(file_path)

    file_size = path.stat().st_size

    if file_size == 0:

        raise InvalidFileError(
            "The uploaded file is empty."
        )

    return True


def get_file_size_bytes(file_path):
    """
    Return file size in bytes.
    """

    path = Path(file_path)

    return path.stat().st_size


def get_file_size_mb(file_path):
    """
    Return file size in MB.
    """

    size_bytes = get_file_size_bytes(file_path)

    return round(
        size_bytes / (1024 * 1024),
        2
    )


def validate_file_size(file_path):
    """
    Check whether the file exceeds the allowed size.
    """

    size_mb = get_file_size_mb(file_path)

    if size_mb > MAX_FILE_SIZE_MB:

        raise FileTooLargeError(
            f"File size is {size_mb} MB. "
            f"Maximum allowed size is "
            f"{MAX_FILE_SIZE_MB} MB."
        )

    return True


def validate_file(file_path):
    """
    Run all file validation checks.
    """

    validate_file_exists(file_path)

    validate_file_is_not_directory(file_path)

    validate_file_not_empty(file_path)

    validate_file_size(file_path)

    return {
        "valid": True,
        "file_size_bytes": get_file_size_bytes(file_path),
        "file_size_mb": get_file_size_mb(file_path)
    }