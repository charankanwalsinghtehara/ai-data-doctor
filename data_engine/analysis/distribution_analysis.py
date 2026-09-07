import pandas as pd


def interpret_skewness(skewness):

    if abs(skewness) < 0.5:

        return "approximately_symmetric"

    elif skewness >= 0.5:

        return "right_skewed"

    else:

        return "left_skewed"


def analyze_distribution(series):
    """
    Analyze distribution of one numerical column.
    """

    clean_series = series.dropna()

    if clean_series.empty:

        return {
            "available": False
        }

    skewness = float(
        clean_series.skew()
    )

    return {

        "available": True,

        "count":
            int(clean_series.count()),

        "mean":
            round(
                float(clean_series.mean()),
                4
            ),

        "median":
            round(
                float(clean_series.median()),
                4
            ),

        "minimum":
            round(
                float(clean_series.min()),
                4
            ),

        "maximum":
            round(
                float(clean_series.max()),
                4
            ),

        "q1":
            round(
                float(
                    clean_series.quantile(0.25)
                ),
                4
            ),

        "q3":
            round(
                float(
                    clean_series.quantile(0.75)
                ),
                4
            ),

        "skewness":
            round(skewness, 4),

        "distribution_shape":
            interpret_skewness(skewness)
    }


def analyze_all_distributions(dataframe):

    results = {}

    numerical_columns = (
        dataframe.select_dtypes(
            include="number"
        ).columns
    )

    for column in numerical_columns:

        results[column] = (
            analyze_distribution(
                dataframe[column]
            )
        )

    return results