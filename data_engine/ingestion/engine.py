from .validator import validate_file

from .detector import detect_file_type

from .router import route_file


def ingest_file(file_path):
    """
    Complete ingestion pipeline.

    Steps:
    1. Validate file
    2. Detect file type
    3. Determine processing route
    """

    validation_result = validate_file(file_path)

    file_info = detect_file_type(file_path)

    routing_result = route_file(file_info)

    return {
        "success": True,

        "validation": validation_result,

        "file_info": file_info,

        "routing": routing_result
    }