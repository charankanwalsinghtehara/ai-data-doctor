import pandas as pd


def normalize_value(value):

    return (
        str(value)
        .strip()
        .lower()
    )


def check_categorical_consistency(series):
    """
    Check categorical values for formatting
    inconsistencies.
    """

    non_null = series.dropna()

    if non_null.empty:

        return {
            "consistent": True,
            "possible_inconsistencies": []
        }

    normalized_map = {}

    for value in non_null.unique():

        normalized = normalize_value(value)

        if normalized not in normalized_map:

            normalized_map[normalized] = []

        normalized_map[
            normalized
        ].append(str(value))

    inconsistencies = []

    for normalized, originals in (
        normalized_map.items()
    ):

        if len(originals) > 1:

            inconsistencies.append({

                "normalized_value":
                    normalized,

                "different_versions":
                    originals
            })

    return {

        "consistent":
            len(inconsistencies) == 0,

        "possible_inconsistencies":
            inconsistencies
    }


def check_consistency(
    dataframe,
    understanding_result
):
    """
    Check consistency for categorical columns.
    """

    results = {}

    for column in dataframe.columns:

        column_info = (
            understanding_result["columns"]
            .get(column, {})
        )

        role = column_info.get(
            "role"
        )

        if role == "categorical":

            results[column] = (
                check_categorical_consistency(
                    dataframe[column]
                )
            )

    return results
