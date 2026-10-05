
from .project_manager import (
    create_project
)

from .dataset_storage import (
    save_original_dataset,
    save_cleaned_dataset
)

from .report_storage import (
    save_final_report,
    save_intelligence_result
)

from .history_manager import (
    add_history_event
)


# ==========================================
# CREATE DATA PROJECT
# ==========================================

def create_data_project(
    project_name=None
):
    """
    Create a new AI Data Doctor project.
    """

    project = create_project(
        project_name
    )

    project_id = project["project_id"]

    add_history_event(
        project_id,
        "project_created",
        {
            "project_name":
                project["project_name"]
        }
    )

    return project


# ==========================================
# SAVE PROJECT RESULTS
# ==========================================

def save_project_results(
    project_id,
    original_dataframe=None,
    cleaned_dataframe=None,
    final_report=None,
    intelligence_result=None
):
    """
    Save all important AI Data Doctor
    project results.
    """

    saved_results = {}


    # ======================================
    # ORIGINAL DATASET
    # ======================================

    if original_dataframe is not None:

        saved_results[
            "original_dataset"
        ] = save_original_dataset(

            original_dataframe,

            project_id
        )


    # ======================================
    # CLEANED DATASET
    # ======================================

    if cleaned_dataframe is not None:

        saved_results[
            "cleaned_dataset"
        ] = save_cleaned_dataset(

            cleaned_dataframe,

            project_id
        )


    # ======================================
    # FINAL REPORT
    # ======================================

    if final_report is not None:

        saved_results[
            "final_report"
        ] = save_final_report(

            final_report,

            project_id
        )


    # ======================================
    # INTELLIGENCE RESULT
    # ======================================

    if intelligence_result is not None:

        saved_results[
            "intelligence"
        ] = save_intelligence_result(

            intelligence_result,

            project_id
        )


    # ======================================
    # HISTORY
    # ======================================

    add_history_event(

        project_id,

        "project_results_saved",

        {
            "saved_items":
                list(
                    saved_results.keys()
                )
        }
    )


    return {

        "success": True,

        "project_id": project_id,

        "saved_results":
            saved_results
    }

