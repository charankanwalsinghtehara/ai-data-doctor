from .paths import (
    get_report_directory
)

from .json_storage import (
    save_json,
    load_json
)


def save_final_report(
    report,
    project_id
):
    """
    Save final report.
    """

    report_directory = (
        get_report_directory(
            project_id
        )
    )

    file_path = (
        report_directory
        / "final_report.json"
    )

    return save_json(
        report,
        file_path
    )


def save_intelligence_result(
    intelligence_result,
    project_id
):
    """
    Save Intelligence Engine results.
    """

    report_directory = (
        get_report_directory(
            project_id
        )
    )

    file_path = (
        report_directory
        / "intelligence.json"
    )

    return save_json(

        intelligence_result,

        file_path
    )


def load_final_report(
    project_id
):
    """
    Load final report.
    """

    file_path = (

        get_report_directory(
            project_id
        )

        / "final_report.json"
    )

    return load_json(
        file_path
    )


def load_intelligence_result(
    project_id
):
    """
    Load Intelligence results.
    """

    file_path = (

        get_report_directory(
            project_id
        )

        / "intelligence.json"
    )

    return load_json(
        file_path
    )