import pandas as pd

from .exceptions import (
    UnsupportedAnomalyDataError
)

from .iqr_detector import (
    detect_all_iqr_outliers
)

from .zscore_detector import (
    detect_all_zscore_outliers
)

from .isolation_forest_detector import (
    detect_isolation_forest_anomalies
)

from .multivariate_detector import (
    combine_anomaly_results
)

from .severity_scorer import (
    calculate_anomaly_severity,
    get_anomaly_summary
)


def detect_anomalies(
    dataframe
):
    """
    Complete anomaly detection pipeline.
    """

    if not isinstance(
        dataframe,
        pd.DataFrame
    ):

        raise UnsupportedAnomalyDataError(
            "Anomaly Engine supports "
            "Pandas DataFrames only."
        )

    # IQR Detection
    iqr_results = (
        detect_all_iqr_outliers(
            dataframe
        )
    )

    # Z-score Detection
    zscore_results = (
        detect_all_zscore_outliers(
            dataframe
        )
    )

    # Isolation Forest
    isolation_result = (
        detect_isolation_forest_anomalies(
            dataframe
        )
    )

    # Combine all detections
    anomaly_map = (
        combine_anomaly_results(
            iqr_results,
            zscore_results,
            isolation_result
        )
    )

    # Calculate severity
    severity_results = (
        calculate_anomaly_severity(
            anomaly_map
        )
    )

    # Summary
    summary = (
        get_anomaly_summary(
            severity_results
        )
    )

    return {

        "success": True,

        "iqr":
            iqr_results,

        "zscore":
            zscore_results,

        "isolation_forest":
            isolation_result,

        "anomalies":
            severity_results,

        "summary":
            summary
    }