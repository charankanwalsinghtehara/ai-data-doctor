def generate_final_recommendations(
    quality_result=None,
    cleaning_result=None,
    anomaly_result=None,
    analysis_result=None,
    ml_result=None
):
    """
    Generate final recommendations
    using all available engine results.
    """

    recommendations = []

    # -------------------------
    # DATA QUALITY
    # -------------------------

    if quality_result:

        completeness = (
            quality_result.get(
                "completeness",
                {}
            )
        )

        missing_values = (
            completeness.get(
                "total_missing_values",
                0
            )
        )

        if missing_values > 0:

            recommendations.append({

                "category":
                    "data_quality",

                "priority":
                    "high",

                "message":
                    "Review missing values before "
                    "using the dataset for critical "
                    "decision-making."
            })

        duplicates = (
            quality_result.get(
                "duplicates",
                {}
            )
        )

        duplicate_rows = (
            duplicates.get(
                "duplicate_rows",
                0
            )
        )

        if duplicate_rows > 0:

            recommendations.append({

                "category":
                    "data_quality",

                "priority":
                    "medium",

                "message":
                    "Duplicate records were detected. "
                    "Verify whether they represent "
                    "real repeated observations."
            })

    # -------------------------
    # ANOMALIES
    # -------------------------

    if anomaly_result:

        summary = (
            anomaly_result.get(
                "summary",
                {}
            )
        )

        high_anomalies = (
            summary.get(
                "high",
                0
            )
        )

        if high_anomalies > 0:

            recommendations.append({

                "category":
                    "anomaly",

                "priority":
                    "high",

                "message":
                    "High-severity anomalies were "
                    "detected. Review suspicious "
                    "records before analysis or ML."
            })

    # -------------------------
    # ANALYSIS
    # -------------------------

    if analysis_result:

        insights = (
            analysis_result.get(
                "insights",
                []
            )
        )

        if len(insights) == 0:

            recommendations.append({

                "category":
                    "analysis",

                "priority":
                    "low",

                "message":
                    "No major automatic insights were "
                    "detected. Consider domain-specific "
                    "analysis."
            })

    # -------------------------
    # MACHINE LEARNING
    # -------------------------

    if ml_result:

        best_model = (
            ml_result.get(
                "best_model",
                {}
            )
        )

        best_score = (
            best_model.get(
                "best_score"
            )
        )

        if best_score is not None:

            recommendations.append({

                "category":
                    "machine_learning",

                "priority":
                    "medium",

                "message":
                    (
                        "The best trained model achieved "
                        f"a score of {best_score}. "
                        "Validate the model with more "
                        "data before production use."
                    )
            })

    return recommendations