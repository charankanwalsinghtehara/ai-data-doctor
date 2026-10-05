import uuid

from datetime import datetime

from .paths import (

    initialize_storage,

    get_project_directory,

    get_dataset_directory,

    get_report_directory,

    get_model_directory
)

from .json_storage import (

    save_json,

    load_json
)

from .exceptions import (
    ProjectNotFoundError
)


def create_project(
    project_name=None
):
    """
    Create a new AI Data Doctor project.
    """

    initialize_storage()

    project_id = (
        f"project_"
        f"{uuid.uuid4().hex[:12]}"
    )

    project_directory = (
        get_project_directory(
            project_id
        )
    )

    project_directory.mkdir(

        parents=True,

        exist_ok=True
    )

    get_dataset_directory(
        project_id
    ).mkdir(exist_ok=True)

    get_report_directory(
        project_id
    ).mkdir(exist_ok=True)

    get_model_directory(
        project_id
    ).mkdir(exist_ok=True)

    metadata = {

        "project_id":
            project_id,

        "project_name":
            project_name
            or project_id,

        "created_at":
            datetime.now()
            .isoformat(),

        "updated_at":
            datetime.now()
            .isoformat(),

        "status":
            "created"
    }

    metadata_path = (
        project_directory
        / "metadata.json"
    )

    save_json(
        metadata,
        metadata_path
    )

    return metadata


def get_project(
    project_id
):
    """
    Load project metadata.
    """

    project_directory = (
        get_project_directory(
            project_id
        )
    )

    metadata_path = (
        project_directory
        / "metadata.json"
    )

    metadata = load_json(
        metadata_path
    )

    if metadata is None:

        raise ProjectNotFoundError(

            f"Project '{project_id}' "
            f"was not found."
        )

    return metadata


def update_project(
    project_id,
    updates
):
    """
    Update project metadata.
    """

    metadata = get_project(
        project_id
    )

    metadata.update(
        updates
    )

    metadata["updated_at"] = (
        datetime.now()
        .isoformat()
    )

    metadata_path = (

        get_project_directory(
            project_id
        )

        / "metadata.json"
    )

    save_json(
        metadata,
        metadata_path
    )

    return metadata