def assess_data_risks(
    health_result,
    anomaly_result=None,
    ml_result=None
):
    """
    Identify risks in the dataset.
    """

    risks = []

    health_score = health_result.get(
        "health_score",
        0
    )

    # -------------------------
    # HEALTH RISK
    # -------------------------

    if health_score < 30:

        risks.append({

            "risk":
                "dataset_health",

            "level":
                "critical",

            "message":
                "Dataset health is critical."
        })

    elif health_score < 50:

        risks.append({

            "risk":
                "dataset_health",

            "level":
                "high",

            "message":
                "Dataset quality is poor."
        })

    elif health_score < 70:

        risks.append({

            "risk":
                "dataset_health",

            "level":
                "medium",

            "message":
                "Dataset needs improvement."
        })

    # -------------------------
    # ANOMALY RISK
    # -------------------------

    if anomaly_result:

        summary = anomaly_result.get(
            "summary",
            {}
        )

        high_count = summary.get(
            "high",
            0
        )

        if high_count > 10:

            risks.append({

                "risk":
                    "anomalies",

                "level":
                    "critical",

                "message":
                    "Large number of serious anomalies detected."
            })

        elif high_count > 0:

            risks.append({

                "risk":
                    "anomalies",

                "level":
                    "high",

                "message":
                    "High severity anomalies require review."
            })

    # -------------------------
    # ML PERFORMANCE RISK
    # -------------------------

    if ml_result:

        best_model = ml_result.get(
            "best_model",
            {}
        )

        best_score = best_model.get(
            "best_score"
        )

        if best_score is not None:

            if best_score < 0.30:

                risks.append({

                    "risk":
                        "model_performance",

                    "level":
                        "critical",

                    "message":
                        "Model performance is extremely low."
                })

            elif best_score < 0.50:

                risks.append({

                    "risk":
                        "model_performance",

                    "level":
                        "high",

                    "message":
                        "Model performance needs improvement."
                })

    return risks


def calculate_overall_risk(
    risks
):
    """
    Calculate the overall system risk.
    """

    if not risks:

        return "low"

    levels = [
        risk["level"]
        for risk in risks
    ]

    if "critical" in levels:

        return "critical"

    if "high" in levels:

        return "high"

    if "medium" in levels:

        return "medium"

    return "low"