import pandas as pd

from .exceptions import (
    UnsupportedDatasetError
)

from .dataset_profiler import (
    profile_dataset
)

from .numerical_profiler import (
    profile_all_numerical_columns
)

from .categorical_profiler import (
    profile_all_categorical_columns
)

from .text_profiler import (
    profile_all_text_columns
)

from .missing_profiler import (
    profile_missing_values
)

from .duplicate_profiler import (
    profile_duplicates
)

from .column_profiler import (
    profile_columns
)


def profile_dataset_complete(
    dataframe,
    understanding_result
):
    """
    Complete automatic dataset profiling pipeline.
    """

    if not isinstance(
        dataframe,
        pd.DataFrame
    ):

        raise UnsupportedDatasetError(
            "Profiling Engine supports "
            "Pandas DataFrames only."
        )

    dataset_profile = (
        profile_dataset(dataframe)
    )

    column_roles = {}

    for column, info in (
        understanding_result["columns"]
        .items()
    ):

        column_roles[column] = (
            info["role"]
        )

    numerical_profile = (
        profile_all_numerical_columns(
            dataframe
        )
    )

    categorical_profile = (
        profile_all_categorical_columns(
            dataframe,
            column_roles
        )
    )

    text_profile = (
        profile_all_text_columns(
            dataframe,
            column_roles
        )
    )

    missing_profile = (
        profile_missing_values(
            dataframe
        )
    )

    duplicate_profile = (
        profile_duplicates(
            dataframe
        )
    )

    column_profiles = (
        profile_columns(
            dataframe,
            understanding_result
        )
    )

    return {
        "success": True,

        "dataset":
            dataset_profile,

        "numerical":
            numerical_profile,

        "categorical":
            categorical_profile,

        "text":
            text_profile,

        "missing_values":
            missing_profile,

        "duplicates":
            duplicate_profile,

        "column_profiles":
            column_profiles
    }