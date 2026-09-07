def calculate_anomaly_severity(
    anomaly_map
):
    """
    Calculate severity for each anomaly.
    """

    results = {}

    for index, detections in (
        anomaly_map.items()
    ):

        detection_count = len(
            detections
        )

        if detection_count >= 3:

            severity = "high"

        elif detection_count == 2:

            severity = "medium"

        else:

            severity = "low"

        results[index] = {

            "severity":
                severity,

            "detection_count":
                detection_count,

            "detections":
                detections
        }

    return results


def get_anomaly_summary(
    severity_results
):
    """
    Create anomaly summary.
    """

    summary = {

        "total_anomalies":
            len(severity_results),

        "high": 0,

        "medium": 0,

        "low": 0
    }

    for result in severity_results.values():

        severity = result["severity"]

        summary[severity] += 1

    return summary