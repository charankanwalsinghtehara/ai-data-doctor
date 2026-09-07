def detect_iqr_outliers(series):
    """
    Detect outliers using the IQR method.
    """

    clean_series = series.dropna()

    if clean_series.empty:

        return {
            "outlier_count": 0,
            "outlier_indices": [],
            "lower_bound": None,
            "upper_bound": None
        }

    q1 = clean_series.quantile(0.25)

    q3 = clean_series.quantile(0.75)

    iqr = q3 - q1

    lower_bound = q1 - (1.5 * iqr)

    upper_bound = q3 + (1.5 * iqr)

    mask = (
        (series < lower_bound)
        |
        (series > upper_bound)
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

        "lower_bound":
            float(lower_bound),

        "upper_bound":
            float(upper_bound)
    }


def detect_all_iqr_outliers(dataframe):
    """
    Detect IQR outliers in every numerical column.
    """

    results = {}

    numerical_columns = (
        dataframe
        .select_dtypes(include="number")
        .columns
    )

    for column in numerical_columns:

        results[column] = (
            detect_iqr_outliers(
                dataframe[column]
            )
        )

    return results