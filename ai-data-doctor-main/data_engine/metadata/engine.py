from .file_metadata import (
    get_file_metadata
)

from .dataset_metadata import (
    get_dataset_metadata
)

from .metadata_manager import (
    create_metadata_record
)


def run_metadata_engine(

    file_path,

    dataframe,

    project_id=None,

    project_name=None
):
    """
    Run the complete
    metadata engine.
    """


    file_metadata = (

        get_file_metadata(
            file_path
        )
    )


    dataset_metadata = (

        get_dataset_metadata(
            dataframe
        )
    )


    metadata_record = (

        create_metadata_record(

            file_metadata=file_metadata,

            dataset_metadata=dataset_metadata,

            project_id=project_id,

            project_name=project_name
        )
    )


    return metadata_record