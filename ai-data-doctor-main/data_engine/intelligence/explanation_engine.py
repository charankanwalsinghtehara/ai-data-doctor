def explain_dataset_condition(
    health_result,
    risk_result,
    ml_readiness
):
    """
    Generate a human-readable
    explanation of dataset condition.
    """

    health_score = (
        health_result[
            "health_score"
        ]
    )

    health_status = (
        health_result[
            "status"
        ]
    )

    overall_risk = (
        risk_result[
            "overall_risk"
        ]
    )

    ml_status = (
        ml_readiness[
            "status"
        ]
    )

    explanation = []

    explanation.append(
        f"The dataset health score is "
        f"{health_score}/100, "
        f"which is classified as "
        f"{health_status}."
    )

    explanation.append(
        f"The overall data risk level is "
        f"{overall_risk}."
    )

    if ml_status == "ready":

        explanation.append(
            "The dataset appears suitable for "
            "basic machine learning experimentation."
        )

    elif ml_status == "partially_ready":

        explanation.append(
            "The dataset can be used for ML, "
            "but data quality improvements are recommended."
        )

    else:

        explanation.append(
            "The dataset is currently not recommended "
            "for reliable machine learning."
        )

    return {

        "summary":
            " ".join(explanation),

        "health_status":
            health_status,

        "risk_level":
            overall_risk,

        "ml_status":
            ml_status
    }