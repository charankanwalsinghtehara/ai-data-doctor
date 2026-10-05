import pandas as pd


def profile_text_column(series):
    """
    Generate statistics for text data.
    """

    non_null = (
        series.dropna()
        .astype(str)
    )

    if len(non_null) == 0:

        return {
            "count": 0,
            "average_length": 0,
            "minimum_length": 0,
            "maximum_length": 0,
            "empty_strings": 0
        }

    lengths = non_null.str.len()

    empty_strings = (
        non_null.str.strip() == ""
    ).sum()

    return {
        "count": int(len(non_null)),

        "average_length":
            round(
                float(lengths.mean()),
                2
            ),

        "minimum_length":
            int(lengths.min()),

        "maximum_length":
            int(lengths.max()),

        "empty_strings":
            int(empty_strings)
    }


def profile_all_text_columns(
    dataframe,
    column_roles
):
    """
    Profile all text columns.
    """

    results = {}

    for column in dataframe.columns:

        role = column_roles.get(column)

        if role == "text":

            results[column] = (
                profile_text_column(
                    dataframe[column]
                )
            )

    return results