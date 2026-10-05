import pandas as pd


def recommend_analysis(
    dataframe
):
    """
    Recommend useful
    data analysis operations.
    """

    recommendations = []


    numeric_columns = (

        dataframe.select_dtypes(
            include=["number"]
        ).columns
    )


    categorical_columns = (

        dataframe.select_dtypes(
            include=["object", "category"]
        ).columns
    )


    datetime_columns = (

        dataframe.select_dtypes(
            include=["datetime"]
        ).columns
    )


    # =========================
    # NUMERIC
    # =========================

    if len(numeric_columns) > 0:

        recommendations.append(
            "descriptive_statistics"
        )

        recommendations.append(
            "correlation_analysis"
        )

        recommendations.append(
            "distribution_analysis"
        )


    # =========================
    # CATEGORICAL
    # =========================

    if len(categorical_columns) > 0:

        recommendations.append(
            "category_distribution"
        )


    # =========================
    # TIME DATA
    # =========================

    if len(datetime_columns) > 0:

        recommendations.append(
            "time_series_analysis"
        )


    # =========================
    # LARGE DATASET
    # =========================

    if len(dataframe) > 1000:

        recommendations.append(
            "anomaly_detection"
        )


    return recommendations