def recommend_ml_task(
    dataframe,
    target_candidates
):
    """
    Recommend ML task.
    """

    if dataframe.empty:

        return {

            "ml_recommended":
                False,

            "reason":
                "Dataset is empty."
        }


    if len(dataframe) < 20:

        return {

            "ml_recommended":
                False,

            "reason":
                "Dataset is too small for reliable ML."
        }


    if not target_candidates:

        return {

            "ml_recommended":
                False,

            "reason":
                "No clear target column detected."
        }


    best_target = (
        target_candidates[0]
    )


    target_column = (
        best_target["column"]
    )


    unique_values = (
        dataframe[target_column]
        .nunique()
    )


    if unique_values <= 20:

        task_type = (
            "classification"
        )

        recommended_models = [

            "Logistic Regression",

            "Random Forest Classifier",

            "Decision Tree Classifier"
        ]

    else:

        task_type = (
            "regression"
        )

        recommended_models = [

            "Linear Regression",

            "Random Forest Regressor",

            "Decision Tree Regressor"
        ]


    return {

        "ml_recommended":
            True,

        "target_column":
            target_column,

        "task_type":
            task_type,

        "recommended_models":
            recommended_models
    }