def combine_anomaly_results(
    iqr_results,
    zscore_results,
    isolation_result
):
    """
    Combine anomaly detection methods.
    """

    anomaly_map = {}

    # IQR anomalies
    for column, result in (
        iqr_results.items()
    ):

        for index in result[
            "outlier_indices"
        ]:

            if index not in anomaly_map:

                anomaly_map[index] = []

            anomaly_map[index].append({
                "method": "IQR",
                "column": column
            })

    # Z-score anomalies
    for column, result in (
        zscore_results.items()
    ):

        for index in result[
            "outlier_indices"
        ]:

            if index not in anomaly_map:

                anomaly_map[index] = []

            anomaly_map[index].append({
                "method": "Z_SCORE",
                "column": column
            })

    # Isolation Forest anomalies
    if isolation_result.get(
        "available"
    ):

        for index in isolation_result[
            "anomaly_indices"
        ]:

            if index not in anomaly_map:

                anomaly_map[index] = []

            anomaly_map[index].append({
                "method":
                    "ISOLATION_FOREST",

                "column":
                    "MULTIVARIATE"
            })

    return anomaly_map