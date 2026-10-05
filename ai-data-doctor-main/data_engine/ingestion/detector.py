from pathlib import Path

from .exceptions import UnsupportedFileTypeError


SUPPORTED_FILE_TYPES = {
    ".csv": {
        "file_type": "csv",
        "category": "tabular"
    },

    ".xlsx": {
        "file_type": "excel",
        "category": "tabular"
    },

    ".xls": {
        "file_type": "excel",
        "category": "tabular"
    },

    ".json": {
        "file_type": "json",
        "category": "structured"
    },

    ".parquet": {
        "file_type": "parquet",
        "category": "tabular"
    },

    ".xml": {
        "file_type": "xml",
        "category": "structured"
    },

    ".txt": {
        "file_type": "text",
        "category": "text"
    },

    ".pdf": {
        "file_type": "pdf",
        "category": "document"
    },

    ".docx": {
        "file_type": "docx",
        "category": "document"
    },

    ".png": {
        "file_type": "image",
        "category": "image"
    },

    ".jpg": {
        "file_type": "image",
        "category": "image"
    },

    ".jpeg": {
        "file_type": "image",
        "category": "image"
    }
}


def get_file_extension(file_path):
    """
    Return the lowercase extension of a file.
    """

    return Path(file_path).suffix.lower()


def is_supported_file(file_path):
    """
    Check whether the file extension is supported.
    """

    extension = get_file_extension(file_path)

    return extension in SUPPORTED_FILE_TYPES


def detect_file_type(file_path):
    """
    Detect file type and category.
    """

    file_path = Path(file_path)

    extension = get_file_extension(file_path)

    if extension not in SUPPORTED_FILE_TYPES:

        raise UnsupportedFileTypeError(
            f"Unsupported file type: {extension}"
        )

    file_information = SUPPORTED_FILE_TYPES[extension]

    return {
        "filename": file_path.name,
        "extension": extension,
        "file_type": file_information["file_type"],
        "category": file_information["category"],
        "supported": True
    }