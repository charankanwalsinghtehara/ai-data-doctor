from pathlib import Path


BASE_STORAGE_DIRECTORY = Path(
    "storage"
)


PROJECTS_DIRECTORY = (
    BASE_STORAGE_DIRECTORY
    / "projects"
)


def initialize_storage():
    """
    Create the main storage directories.
    """

    PROJECTS_DIRECTORY.mkdir(

        parents=True,

        exist_ok=True
    )


def get_project_directory(
    project_id
):
    """
    Return the directory for a project.
    """

    return (
        PROJECTS_DIRECTORY
        / project_id
    )


def get_dataset_directory(
    project_id
):

    return (
        get_project_directory(
            project_id
        )
        / "datasets"
    )


def get_report_directory(
    project_id
):

    return (
        get_project_directory(
            project_id
        )
        / "reports"
    )


def get_model_directory(
    project_id
):

    return (
        get_project_directory(
            project_id
        )
        / "models"
    )