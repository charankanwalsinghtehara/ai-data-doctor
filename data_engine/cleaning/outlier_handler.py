import pandas as pd


def calculate_iqr_bounds(series):
    """
    Calculate IQR outlier boundaries.
    """

    clean_series = series.dropna()

    if len(clean_series) == 0:

        return None, None

    q1 = clean_series.quantile(0.25)

    q3 = clean_series.quantile(0.75)

    iqr = q3 - q1

    lower_bound = (
        q1 - 1.5 * iqr
    )

    upper_bound = (
        q3 + 1.5 * iqr
    )

    return lower_bound, upper_bound


def detect_outliers(series):
    """
    Detect outliers using IQR.
    """

    lower_bound, upper_bound = (
        calculate_iqr_bounds(series)
    )

    if lower_bound is None:

        return {
            "outlier_count": 0,
            "lower_bound": None,
            "upper_bound": None
        }

    mask = (
        (series < lower_bound)
        |
        (series > upper_bound)
    )

    outlier_count = int(mask.sum())

    return {
        "outlier_count": outlier_count,
        "lower_bound": float(lower_bound),
        "upper_bound": float(upper_bound)
    }


def cap_outliers(series):
    """
    Cap outliers to IQR boundaries.
    """

    lower_bound, upper_bound = (
        calculate_iqr_bounds(series)
    )

    if lower_bound is None:

        return series, 0

    original_series = series.copy()

    capped_series = series.clip(
        lower=lower_bound,
        upper=upper_bound
    )

    changes = int(
        (original_series != capped_series)
        .sum()
    )

    return capped_series, changes


def handle_outliers(dataframe):
    """
    Detect and cap numerical outliers.
    """

    cleaned_dataframe = dataframe.copy()

    results = {}

    numerical_columns = (
        cleaned_dataframe
        .select_dtypes(
            include="number"
        )
        .columns
    )

    for column in numerical_columns:

        detection = detect_outliers(
            cleaned_dataframe[column]
        )

        outlier_count = (
            detection["outlier_count"]
        )

        if outlier_count > 0:

            cleaned_series, changes = (
                cap_outliers(
                    cleaned_dataframe[column]
                )
            )

            cleaned_dataframe[column] = (
                cleaned_series
            )

        else:

            changes = 0

        results[column] = {

            **detection,

            "values_modified":
                changes
        }

    return cleaned_dataframe, results