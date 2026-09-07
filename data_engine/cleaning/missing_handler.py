import pandas as pd


def handle_numerical_missing(
    series
):
    """
    Fill numerical missing values using median.
    """

    missing_before = int(
        series.isna().sum()
    )

    if missing_before == 0:

        return series, {
            "method": "none",
            "filled_values": 0
        }

    median_value = series.median()

    if pd.isna(median_value):

        return series, {
            "method": "unable_to_fill",
            "filled_values": 0
        }

    cleaned_series = series.fillna(
        median_value
    )

    return cleaned_series, {
        "method": "median",
        "fill_value": float(median_value),
        "filled_values": missing_before
    }


def handle_categorical_missing(
    series
):
    """
    Fill categorical missing values using mode.
    """

    missing_before = int(
        series.isna().sum()
    )

    if missing_before == 0:

        return series, {
            "method": "none",
            "filled_values": 0
        }

    mode_values = series.mode()

    if len(mode_values) == 0:

        fill_value = "Unknown"

    else:

        fill_value = mode_values.iloc[0]

    cleaned_series = series.fillna(
        fill_value
    )

    return cleaned_series, {
        "method": "mode",
        "fill_value": str(fill_value),
        "filled_values": missing_before
    }


def handle_text_missing(
    series
):
    """
    Fill text missing values.
    """

    missing_before = int(
        series.isna().sum()
    )

    cleaned_series = series.fillna(
        "Unknown"
    )

    return cleaned_series, {
        "method": "unknown_label",
        "fill_value": "Unknown",
        "filled_values": missing_before
    }


def handle_missing_values(
    dataframe,
    understanding_result
):
    """
    Handle missing values based on
    detected column roles.
    """

    cleaned_dataframe = dataframe.copy()

    results = {}

    for column in cleaned_dataframe.columns:

        series = cleaned_dataframe[column]

        column_info = (
            understanding_result["columns"]
            .get(column, {})
        )

        role = column_info.get(
            "role",
            "text"
        )

        missing_count = int(
            series.isna().sum()
        )

        if missing_count == 0:

            results[column] = {
                "method": "none",
                "filled_values": 0
            }

            continue

        if role == "numerical":

            cleaned_series, details = (
                handle_numerical_missing(
                    series
                )
            )

        elif role in [
            "categorical",
            "boolean"
        ]:

            cleaned_series, details = (
                handle_categorical_missing(
                    series
                )
            )

        else:

            cleaned_series, details = (
                handle_text_missing(
                    series
                )
            )

        cleaned_dataframe[column] = (
            cleaned_series
        )

        results[column] = details

    return cleaned_dataframe, results