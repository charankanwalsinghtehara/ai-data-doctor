def normalize_category_value(value):
    """
    Normalize one categorical value.
    """

    if not isinstance(value, str):

        return value

    return (
        value
        .strip()
        .lower()
    )


def normalize_categorical_column(
    series
):
    """
    Normalize values in one categorical column.
    """

    original_series = series.copy()

    normalized_series = (
        series.apply(
            normalize_category_value
        )
    )

    changes = int(
        (original_series != normalized_series)
        .sum()
    )

    return normalized_series, changes


def normalize_categories(
    dataframe,
    understanding_result
):
    """
    Normalize all categorical columns.
    """

    cleaned_dataframe = dataframe.copy()

    results = {}

    for column in cleaned_dataframe.columns:

        column_info = (
            understanding_result["columns"]
            .get(column, {})
        )

        role = column_info.get("role")

        if role != "categorical":

            continue

        normalized_series, changes = (
            normalize_categorical_column(
                cleaned_dataframe[column]
            )
        )

        cleaned_dataframe[column] = (
            normalized_series
        )

        results[column] = {
            "normalized_values": changes
        }

    return cleaned_dataframe, results