from pathlib import Path

from .config import (
    BLOCKED_EXTENSIONS
)

from .exceptions import (
    SecurityValidationError
)


def validate_extension_security(
    file_path
):
    """
    Check blocked extensions.
    """

    path = Path(
        file_path
    )

    extension = (
        path.suffix.lower()
    )

    if extension in BLOCKED_EXTENSIONS:

        raise SecurityValidationError(

            f"Blocked file type: "
            f"{extension}"
        )

    return True


def validate_filename(
    file_path
):
    """
    Validate suspicious filenames.
    """

    path = Path(
        file_path
    )

    filename = path.name

    suspicious_patterns = [

        "..",

        "\x00"
    ]

    for pattern in suspicious_patterns:

        if pattern in filename:

            raise SecurityValidationError(

                "Suspicious filename detected."
            )

    return True


def run_security_validation(
    file_path
):
    """
    Run all security checks.
    """

    validate_extension_security(
        file_path
    )

    validate_filename(
        file_path
    )

    return {

        "security_status":
            "passed"
    }