def assess_dataset_health(
    dataframe,
    quality_result=None,
    anomaly_result=None
):
    """
    Calculate overall dataset health.
    """

    score = 100

    issues = []

    total_rows = len(dataframe)

    total_cells = (
        dataframe.shape[0]
        *
        dataframe.shape[1]
    )

    # -------------------------
    # MISSING VALUES
    # -------------------------

    missing_values = int(
        dataframe.isna().sum().sum()
    )

    if total_cells > 0:

        missing_percentage = (
            missing_values
            /
            total_cells
        ) * 100

    else:

        missing_percentage = 0

    if missing_percentage > 30:

        score -= 40

        issues.append(
            "Very high percentage of missing values."
        )

    elif missing_percentage > 15:

        score -= 25

        issues.append(
            "High percentage of missing values."
        )

    elif missing_percentage > 5:

        score -= 10

        issues.append(
            "Moderate missing values detected."
        )

    # -------------------------
    # DUPLICATES
    # -------------------------

    duplicate_count = int(
        dataframe.duplicated().sum()
    )

    if total_rows > 0:

        duplicate_percentage = (
            duplicate_count
            /
            total_rows
        ) * 100

    else:

        duplicate_percentage = 0

    if duplicate_percentage > 20:

        score -= 20

        issues.append(
            "High number of duplicate rows."
        )

    elif duplicate_percentage > 5:

        score -= 10

        issues.append(
            "Duplicate rows detected."
        )

    # -------------------------
    # ANOMALIES
    # -------------------------

    high_anomalies = 0

    if anomaly_result:

        summary = anomaly_result.get(
            "summary",
            {}
        )

        high_anomalies = summary.get(
            "high",
            0
        )

    if high_anomalies > 10:

        score -= 20

        issues.append(
            "Large number of high severity anomalies."
        )

    elif high_anomalies > 0:

        score -= 10

        issues.append(
            "High severity anomalies detected."
        )

    # -------------------------
    # DATASET SIZE
    # -------------------------

    if total_rows < 20:

        score -= 15

        issues.append(
            "Dataset is very small."
        )

    elif total_rows < 100:

        score -= 5

        issues.append(
            "Dataset size is limited."
        )

    # Prevent negative score

    score = max(
        0,
        min(100, score)
    )

    # -------------------------
    # HEALTH STATUS
    # -------------------------

    if score >= 85:

        status = "excellent"

    elif score >= 70:

        status = "good"

    elif score >= 50:

        status = "fair"

    elif score >= 30:

        status = "poor"

    else:

        status = "critical"

    return {

        "health_score":
            score,

        "status":
            status,

        "issues":
            issues,

        "metrics": {

            "missing_values":
                missing_values,

            "missing_percentage":
                round(
                    missing_percentage,
                    2
                ),

            "duplicate_rows":
                duplicate_count,

            "duplicate_percentage":
                round(
                    duplicate_percentage,
                    2
                ),

            "high_severity_anomalies":
                high_anomalies
        }
    }