def make_decisions(
    health_result,
    risk_result,
    dataframe,
    ml_result=None
):
    """
    Make intelligent decisions
    based on dataset condition.
    """

    decisions = []

    health_score = health_result[
        "health_score"
    ]

    overall_risk = risk_result[
        "overall_risk"
    ]

    # -------------------------
    # DATA CLEANING DECISION
    # -------------------------

    if health_score < 50:

        decisions.append({

            "action":
                "clean_data",

            "priority":
                "critical",

            "reason":
                "Dataset health is too low."
        })

    elif health_score < 70:

        decisions.append({

            "action":
                "review_data_quality",

            "priority":
                "high",

            "reason":
                "Dataset quality needs improvement."
        })

    # -------------------------
    # ML TRAINING DECISION
    # -------------------------

    if overall_risk == "critical":

        decisions.append({

            "action":
                "block_ml_training",

            "priority":
                "critical",

            "reason":
                "Critical data risks may produce unreliable models."
        })

    elif len(dataframe) < 30:

        decisions.append({

            "action":
                "warn_small_dataset",

            "priority":
                "high",

            "reason":
                "Dataset is too small for reliable ML."
        })

    else:

        decisions.append({

            "action":
                "ml_training_allowed",

            "priority":
                "normal",

            "reason":
                "Dataset passed basic ML readiness checks."
        })

    # -------------------------
    # MODEL IMPROVEMENT
    # -------------------------

    if ml_result:

        best_model = ml_result.get(
            "best_model",
            {}
        )

        best_score = best_model.get(
            "best_score"
        )

        if (
            best_score is not None
            and best_score < 0.50
        ):

            decisions.append({

                "action":
                    "improve_model",

                "priority":
                    "high",

                "reason":
                    "Current model performance is low."
            })

    return decisions