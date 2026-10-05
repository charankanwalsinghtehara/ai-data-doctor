import pandas as pd

from .config import (

    MIN_ROWS,

    MIN_COLUMNS
)

from .exceptions import (
    DatasetValidationError
)


def validate_dataframe_type(
    dataframe
):

    if not isinstance(
        dataframe,
        pd.DataFrame
    ):

        raise DatasetValidationError(

            "Extracted data is not "
            "a Pandas DataFrame."
        )

    return True


def validate_dataframe_not_empty(
    dataframe
):

    if dataframe.empty:

        raise DatasetValidationError(

            "Dataset is empty."
        )

    return True


def validate_minimum_rows(
    dataframe
):

    row_count = len(
        dataframe
    )

    if row_count < MIN_ROWS:

        raise DatasetValidationError(

            f"Dataset must contain at least "
            f"{MIN_ROWS} row."
        )

    return row_count


def validate_minimum_columns(
    dataframe
):

    column_count = len(
        dataframe.columns
    )

    if column_count < MIN_COLUMNS:

        raise DatasetValidationError(

            f"Dataset must contain at least "
            f"{MIN_COLUMNS} column."
        )

    return column_count


def validate_duplicate_columns(
    dataframe
):

    duplicate_columns = (

        dataframe.columns[
            dataframe.columns.duplicated()
        ]

        .tolist()
    )

    if duplicate_columns:

        raise DatasetValidationError(

            "Duplicate column names found: "

            + ", ".join(

                map(
                    str,
                    duplicate_columns
                )
            )
        )

    return True


def validate_dataset(
    dataframe
):
    """
    Run complete dataset validation.
    """

    validate_dataframe_type(
        dataframe
    )

    validate_dataframe_not_empty(
        dataframe
    )

    rows = validate_minimum_rows(
        dataframe
    )

    columns = validate_minimum_columns(
        dataframe
    )

    validate_duplicate_columns(
        dataframe
    )

    return {

        "valid": True,

        "rows": rows,

        "columns": columns,

        "duplicate_columns": False
    }