import pandas as pd


def detect_problem_type(
    dataframe,
    target_column
):
    """
    Detect ML problem type.
    """

    series = dataframe[
        target_column
    ]

    unique_count = series.nunique()

    total_rows = len(series)

    # Object/category columns
    if (
        pd.api.types.is_object_dtype(series)
        or pd.api.types.is_categorical_dtype(
            series
        )
        or pd.api.types.is_bool_dtype(series)
    ):

        return {
            "problem_type":
                "classification",

            "reason":
                "Target is categorical."
        }

    # Numerical target
    if (
        pd.api.types.is_numeric_dtype(
            series
        )
    ):

        # Few unique values
        classification_threshold = min(
            20,
            max(5, total_rows * 0.05)
        )

        if (
            unique_count
            <= classification_threshold
        ):

            return {
                "problem_type":
                    "classification",

                "reason":
                    "Numerical target has "
                    "a small number of "
                    "unique values."
            }

        return {

            "problem_type":
                "regression",

            "reason":
                "Target is continuous "
                "numerical data."
        }

    return {

        "problem_type":
            "classification",

        "reason":
            "Default categorical prediction."
    }