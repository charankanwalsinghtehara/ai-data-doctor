from pathlib import Path

from data_engine.storage.paths import (
    get_project_directory
)


def get_visualization_directory(
    project_id
):
    """
    Get visualization directory
    for a project.
    """

    directory = (
        get_project_directory(
            project_id
        )
        / "visualizations"
    )

    directory.mkdir(

        parents=True,

        exist_ok=True
    )

    return directory