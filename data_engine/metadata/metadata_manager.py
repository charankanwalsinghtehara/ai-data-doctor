from datetime import datetime


def create_metadata_record(

    file_metadata,

    dataset_metadata,

    project_id=None,

    project_name=None
):
    """
    Create one complete
    metadata record.
    """

    return {

        "metadata_version":
            "1.0",

        "generated_at":
            datetime.now().isoformat(),


        # =========================
        # PROJECT
        # =========================

        "project": {

            "project_id":
                project_id,

            "project_name":
                project_name
        },


        # =========================
        # FILE
        # =========================

        "file":
            file_metadata,


        # =========================
        # DATASET
        # =========================

        "dataset":
            dataset_metadata
    }