import pandas as pd


def profile_categorical_column(
    series,
    top_values=10
):
    """
    Generate statistics for a categorical column.
    """

    non_null = series.dropna()

    if len(non_null) == 0:

        return {
            "count": 0,
            "unique_values": 0,
            "most_frequent": None,
            "most_frequent_count": 0,
            "value_distribution": {}
        }

    value_counts = non_null.value_counts()

    most_frequent = value_counts.index[0]
    most_frequent_count = value_counts.iloc[0]

    distribution = (
        value_counts
        .head(top_values)
        .to_dict()
    )

    cleaned_distribution = {}

    for key, value in distribution.items():

        cleaned_distribution[str(key)] = int(value)

    return {
        "count": int(non_null.count()),

        "unique_values":
            int(non_null.nunique()),

        "most_frequent":
            str(most_frequent),

        "most_frequent_count":
            int(most_frequent_count),

        "value_distribution":
            cleaned_distribution
    }


def profile_all_categorical_columns(
    dataframe,
    column_roles
):
    """
    Profile categorical columns based on
    Understanding Engine results.
    """

    results = {}

    for column in dataframe.columns:

        role = column_roles.get(column)

        if role == "categorical":

            results[column] = (
                profile_categorical_column(
                    dataframe[column]
                )
            )

    return results