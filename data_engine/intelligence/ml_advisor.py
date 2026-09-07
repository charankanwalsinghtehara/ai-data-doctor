def analyze_ml_readiness(
    dataframe,
    health_result
):
    """
    Analyze whether the dataset
    is suitable for ML.
    """

    rows = len(dataframe)

    columns = len(dataframe.columns)

    health_score = (
        health_result[
            "health_score"
        ]
    )

    issues = []

    recommendations = []

    readiness_score = 100

    # Dataset size

    if rows < 30:

        readiness_score -= 40

        issues.append(
            "Dataset is extremely small."
        )

    elif rows < 100:

        readiness_score -= 20

        issues.append(
            "Dataset is relatively small."
        )

    # Number of features

    if columns < 2:

        readiness_score -= 40

        issues.append(
            "Dataset has insufficient features."
        )

    # Data health

    if health_score < 50:

        readiness_score -= 30

        issues.append(
            "Poor data quality may affect ML performance."
        )

    elif health_score < 70:

        readiness_score -= 15

        issues.append(
            "Data quality should be improved."
        )

    readiness_score = max(
        0,
        min(100, readiness_score)
    )

    if readiness_score >= 80:

        status = "ready"

        recommendations.append(
            "Dataset is suitable for basic ML experimentation."
        )

    elif readiness_score >= 60:

        status = "partially_ready"

        recommendations.append(
            "Improve dataset quality before serious ML training."
        )

    else:

        status = "not_ready"

        recommendations.append(
            "Dataset requires improvement before reliable ML."
        )

    return {

        "ml_readiness_score":
            readiness_score,

        "status":
            status,

        "issues":
            issues,

        "recommendations":
            recommendations
    }