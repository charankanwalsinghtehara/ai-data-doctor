def generate_intelligent_recommendations(
    health_result,
    risks,
    decisions,
    dataframe
):
    """
    Generate recommendations
    based on intelligence results.
    """

    recommendations = []

    # -------------------------
    # MISSING DATA
    # -------------------------

    missing_percentage = (
        health_result["metrics"][
            "missing_percentage"
        ]
    )

    if missing_percentage > 0:

        recommendations.append({

            "category":
                "missing_data",

            "recommendation":
                "Review missing values and determine "
                "whether imputation or removal is appropriate.",

            "priority":
                "high"
                if missing_percentage > 15
                else "medium"
        })

    # -------------------------
    # DUPLICATES
    # -------------------------

    duplicate_count = (
        health_result["metrics"][
            "duplicate_rows"
        ]
    )

    if duplicate_count > 0:

        recommendations.append({

            "category":
                "duplicates",

            "recommendation":
                "Verify duplicate records before deleting them.",

            "priority":
                "medium"
        })

    # -------------------------
    # SMALL DATASET
    # -------------------------

    if len(dataframe) < 100:

        recommendations.append({

            "category":
                "dataset_size",

            "recommendation":
                "Collect more data for stronger statistical "
                "analysis and machine learning.",

            "priority":
                "medium"
        })

    # -------------------------
    # RISKS
    # -------------------------

    for risk in risks:

        recommendations.append({

            "category":
                risk["risk"],

            "recommendation":
                risk["message"],

            "priority":
                risk["level"]
        })

    # -------------------------
    # DECISIONS
    # -------------------------

    for decision in decisions:

        if decision["action"] == "block_ml_training":

            recommendations.append({

                "category":
                    "machine_learning",

                "recommendation":
                    "Fix critical data quality problems "
                    "before training ML models.",

                "priority":
                    "critical"
            })

        elif decision["action"] == "improve_model":

            recommendations.append({

                "category":
                    "machine_learning",

                "recommendation":
                    "Try feature engineering, collect more data, "
                    "and tune model hyperparameters.",

                "priority":
                    "high"
            })

    return recommendations