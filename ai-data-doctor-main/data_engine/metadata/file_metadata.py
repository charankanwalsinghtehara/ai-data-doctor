from pathlib import Path

from datetime import datetime


def get_file_metadata(
    file_path
):
    """
    Collect metadata about
    the uploaded file.
    """

    path = Path(
        file_path
    )

    if not path.exists():

        raise FileNotFoundError(
            f"File not found: {file_path}"
        )


    file_size_bytes = (
        path.stat().st_size
    )


    file_size_mb = (
        file_size_bytes
        / (1024 * 1024)
    )


    modified_time = (
        datetime.fromtimestamp(
            path.stat().st_mtime
        )
    )


    return {

        "file_name":
            path.name,

        "file_path":
            str(
                path.resolve()
            ),

        "file_extension":
            path.suffix.lower(),

        "file_size_bytes":
            file_size_bytes,

        "file_size_mb":
            round(
                file_size_mb,
                2
            ),

        "last_modified":
            modified_time.isoformat()
    }