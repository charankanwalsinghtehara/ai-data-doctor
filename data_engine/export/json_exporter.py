from data_engine.storage.json_storage import (
    save_json
)

from .exceptions import (
    ExportError
)


def export_json(
    data,
    output_directory,
    filename="data_doctor_report.json"
):
    """
    Export data as JSON.
    """

    try:

        file_path = (
            output_directory
            / filename
        )

        save_json(
            data,
            file_path
        )

        return str(file_path)

    except Exception as error:

        raise ExportError(
            f"JSON export failed: {error}"
        )