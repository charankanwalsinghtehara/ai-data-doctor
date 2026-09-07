from datetime import datetime

from .paths import (
    get_project_directory
)

from .json_storage import (
    save_json,
    load_json
)


def get_history_file(
    project_id
):

    return (

        get_project_directory(
            project_id
        )

        / "history.json"
    )


def add_history_event(

    project_id,

    event,

    details=None
):
    """
    Add an event to project history.
    """

    history_file = (
        get_history_file(
            project_id
        )
    )

    history = load_json(
        history_file
    )

    if history is None:

        history = []

    history.append({

        "event":
            event,

        "details":
            details or {},

        "timestamp":
            datetime.now()
            .isoformat()
    })

    save_json(
        history,
        history_file
    )

    return history


def get_project_history(
    project_id
):
    """
    Get complete project history.
    """

    history_file = (
        get_history_file(
            project_id
        )
    )

    history = load_json(
        history_file
    )

    return history or []