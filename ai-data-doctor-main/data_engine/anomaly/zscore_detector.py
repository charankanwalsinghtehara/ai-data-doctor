import pandas as pd


def detect_zscore_outliers(
    series,
    threshold=3
):
    """
    Detect outliers using Z-score.
    """

    clean_series = series.dropna()

    if len(clean_series) < 2:

        return {
            "outlier_count": 0,
            "outlier_indices": [],
            "threshold": threshold
        }

    mean = clean_series.mean()

    std = clean_series.std()

    if std == 0 or pd.isna(std):

        return {
            "outlier_count": 0,
            "outlier_indices": [],
            "threshold": threshold
        }

    z_scores = (
        (series - mean) / std
    )

    mask = (
        z_scores.abs() > threshold
    )

    outlier_indices = (
        series[mask]
        .index
        .tolist()
    )

    return {

        "outlier_count":
            len(outlier_indices),

        "outlier_indices":
            outlier_indices,

        "threshold":
            threshold
    }


def detect_all_zscore_outliers(
    dataframe,
    threshold=3
):
    """
    Detect Z-score anomalies
    in all numerical columns.
    """

    results = {}

    numerical_columns = (
        dataframe
        .select_dtypes(include="number")
        .columns
    )

    for column in numerical_columns:

        results[column] = (
            detect_zscore_outliers(
                dataframe[column],
                threshold
            )
        )

    return results