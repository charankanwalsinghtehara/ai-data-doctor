import shutil

from data_engine.storage.paths import (
    get_project_directory
)

from .exceptions import (
    ExportError
)


def export_project_zip(
    project_id,
    output_directory
):
    """
    Create ZIP archive
    of the complete project.
    """

    try:

        project_directory = (
            get_project_directory(
                project_id
            )
        )

        zip_base_path = (

            output_directory

            / "project_export"
        )

        archive_path = (
            shutil.make_archive(

                str(zip_base_path),

                "zip",

                root_dir=str(
                    project_directory
                )
            )
        )

        return archive_path

    except Exception as error:

        raise ExportError(
            f"Project ZIP export failed: {error}"
        )