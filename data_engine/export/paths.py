from data_engine.storage.paths import (
    get_project_directory
)


def get_export_directory(
    project_id
):
    """
    Get export directory
    for a project.
    """

    directory = (
        get_project_directory(
            project_id
        )
        / "exports"
    )

    directory.mkdir(
        parents=True,
        exist_ok=True
    )

    return directory