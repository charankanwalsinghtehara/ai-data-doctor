def build_anomaly_report(
    anomaly_result
):
    """
    Build anomaly detection report.
    """

    if not anomaly_result:

        return {

            "available": False,

            "message":
                "Anomaly detection not available."
        }

    return {

        "available": True,

        "summary":
            anomaly_result.get(
                "summary",
                {}
            ),

        "anomalies":
            anomaly_result.get(
                "anomalies",
                {}
            ),

        "isolation_forest":
            anomaly_result.get(
                "isolation_forest",
                {}
            )
    }