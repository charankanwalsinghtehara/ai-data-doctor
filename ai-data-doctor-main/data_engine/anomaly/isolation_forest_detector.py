import pandas as pd

from sklearn.ensemble import (
    IsolationForest
)


def detect_isolation_forest_anomalies(
    dataframe,
    contamination=0.05
):
    """
    Detect multivariate anomalies using
    Isolation Forest.
    """

    numerical_data = (
        dataframe
        .select_dtypes(include="number")
        .copy()
    )

    if numerical_data.shape[1] == 0:

        return {

            "available": False,

            "message":
                "No numerical columns available.",

            "anomaly_count": 0,

            "anomaly_indices": []
        }

    # Fill missing values
    numerical_data = (
        numerical_data.fillna(
            numerical_data.median()
        )
    )

    # Remove columns that are completely empty
    numerical_data = (
        numerical_data.dropna(
            axis=1,
            how="all"
        )
    )

    if numerical_data.empty:

        return {

            "available": False,

            "message":
                "Insufficient numerical data.",

            "anomaly_count": 0,

            "anomaly_indices": []
        }

    if len(numerical_data) < 5:

        return {

            "available": False,

            "message":
                "At least 5 rows are recommended.",

            "anomaly_count": 0,

            "anomaly_indices": []
        }

    model = IsolationForest(

        contamination=contamination,

        random_state=42
    )

    predictions = model.fit_predict(
        numerical_data
    )

    anomaly_mask = (
        predictions == -1
    )

    anomaly_indices = (
        numerical_data[
            anomaly_mask
        ]
        .index
        .tolist()
    )

    return {

        "available": True,

        "model":
            "IsolationForest",

        "anomaly_count":
            len(anomaly_indices),

        "anomaly_indices":
            anomaly_indices,

        "contamination":
            contamination
    }