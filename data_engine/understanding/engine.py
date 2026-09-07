import pandas as pd

from .exceptions import UnsupportedDataError

from .data_type_detector import (
    detect_dataframe_data_types
)

from .column_classifier import (
    classify_all_columns
)

from .semantic_detector import (
    detect_all_semantic_types
)

from .target_detector import (
    detect_target_column
)

from .dataset_classifier import (
    classify_dataset
)


def understand_dataset(dataframe):
    """
    Complete data understanding pipeline.
    """

    if not isinstance(
        dataframe,
        pd.DataFrame
    ):

        raise UnsupportedDataError(
            "Understanding Engine currently "
            "supports Pandas DataFrames only."
        )

    if dataframe.empty:

        raise UnsupportedDataError(
            "Cannot understand an empty dataset."
        )

    data_types = (
        detect_dataframe_data_types(
            dataframe
        )
    )

    column_roles = (
        classify_all_columns(
            dataframe
        )
    )

    semantic_types = (
        detect_all_semantic_types(
            dataframe
        )
    )

    target_candidates = (
        detect_target_column(
            dataframe
        )
    )

    dataset_info = (
        classify_dataset(
            dataframe
        )
    )

    columns = {}

    for column in dataframe.columns:

        columns[column] = {

            "technical_type":
                data_types[column],

            "role":
                column_roles[column],

            "semantic_type":
                semantic_types[column],

            "missing_values":
                int(
                    dataframe[column]
                    .isna()
                    .sum()
                ),

            "unique_values":
                int(
                    dataframe[column]
                    .nunique()
                )
        }

    return {

        "success": True,

        "dataset": {
            "rows": int(dataframe.shape[0]),
            "columns": int(dataframe.shape[1])
        },

        "dataset_classification":
            dataset_info,

        "columns":
            columns,

        "possible_target_columns":
            target_candidates
    }