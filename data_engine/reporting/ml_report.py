def build_ml_report(
    ml_recommendations=None,
    ml_result=None
):
    """
    Build Machine Learning report.
    """

    report = {

        "available": True,

        "target_candidates": [],

        "training_performed": False
    }

    if ml_recommendations:

        report["target_candidates"] = (
            ml_recommendations.get(
                "target_candidates",
                []
            )
        )

    if ml_result:

        report["training_performed"] = True

        report["target_column"] = (
            ml_result.get(
                "target_column"
            )
        )

        report["problem"] = (
            ml_result.get(
                "problem",
                {}
            )
        )

        report["feature_information"] = (
            ml_result.get(
                "feature_information",
                {}
            )
        )

        report["models"] = (
            ml_result.get(
                "models",
                {}
            )
        )

        report["best_model"] = (
            ml_result.get(
                "best_model",
                {}
            )
        )

        report["saved_model"] = (
            ml_result.get(
                "saved_model"
            )
        )

    return report