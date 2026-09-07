from .exceptions import UnsupportedFileTypeError


FILE_ROUTES = {

    "csv": "csv_extractor",

    "excel": "excel_extractor",

    "json": "json_extractor",

    "parquet": "parquet_extractor",

    "xml": "xml_extractor",

    "text": "text_extractor",

    "pdf": "pdf_extractor",

    "docx": "docx_extractor",

    "image": "image_extractor"
}


def get_file_route(file_type):
    """
    Return the processing route for a file type.
    """

    route = FILE_ROUTES.get(file_type)

    if route is None:

        raise UnsupportedFileTypeError(
            f"No route available for: {file_type}"
        )

    return route


def route_file(file_info):
    """
    Route a detected file to its extractor.
    """

    file_type = file_info["file_type"]

    route = get_file_route(file_type)

    return {
        "file_type": file_type,
        "route": route
    }