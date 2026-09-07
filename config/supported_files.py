SUPPORTED_EXTENSIONS = {

    ".csv",

    ".xlsx",

    ".xls",

    ".json",

    ".parquet"
}


BLOCKED_EXTENSIONS = {

    ".exe",

    ".bat",

    ".cmd",

    ".msi",

    ".dll",

    ".py",

    ".js",

    ".sh",

    ".ps1",

    ".zip",

    ".rar"
}


FILE_TYPE_NAMES = {

    ".csv": "CSV",

    ".xlsx": "Excel Workbook",

    ".xls": "Excel Workbook",

    ".json": "JSON",

    ".parquet": "Parquet"
}


def is_supported_file(
    extension
):

    return extension.lower() in SUPPORTED_EXTENSIONS


def get_file_type_name(
    extension
):

    return FILE_TYPE_NAMES.get(

        extension.lower(),

        "Unknown"
    )