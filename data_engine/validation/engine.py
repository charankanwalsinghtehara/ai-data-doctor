from .file_validator import (
    validate_file
)

from .security_validator import (
    run_security_validation
)

from .dataset_validator import (
    validate_dataset
)


def run_file_validation(
    file_path
):
    """
    Validate file before ingestion.
    """

    security_result = (
        run_security_validation(
            file_path
        )
    )

    file_result = (
        validate_file(
            file_path
        )
    )

    return {

        "security":
            security_result,

        "file":
            file_result
    }


def run_dataset_validation(
    dataframe
):
    """
    Validate extracted dataset.
    """

    return validate_dataset(
        dataframe
    )


def run_validation_engine(
    file_path=None,
    dataframe=None
):
    """
    Run complete validation engine.
    """

    results = {

        "validation": {}
    }

    if file_path is not None:

        results["validation"][
            "file_validation"
        ] = (

            run_file_validation(
                file_path
            )
        )

    if dataframe is not None:

        results["validation"][
            "dataset_validation"
        ] = (

            run_dataset_validation(
                dataframe
            )
        )

    return results