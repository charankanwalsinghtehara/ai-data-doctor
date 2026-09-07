
from sklearn.metrics import (

    accuracy_score,

    precision_score,

    recall_score,

    f1_score,

    mean_absolute_error,

    mean_squared_error,

    r2_score
)

import numpy as np


def evaluate_classification_model(
    model,
    X_test,
    y_test
):

    predictions = model.predict(
        X_test
    )

    return {

        "accuracy":
            round(
                float(
                    accuracy_score(
                        y_test,
                        predictions
                    )
                ),
                4
            ),

        "precision":
            round(
                float(
                    precision_score(
                        y_test,
                        predictions,
                        average="weighted",
                        zero_division=0
                    )
                ),
                4
            ),

        "recall":
            round(
                float(
                    recall_score(
                        y_test,
                        predictions,
                        average="weighted",
                        zero_division=0
                    )
                ),
                4
            ),

        "f1_score":
            round(
                float(
                    f1_score(
                        y_test,
                        predictions,
                        average="weighted",
                        zero_division=0
                    )
                ),
                4
            )
    }


def evaluate_regression_model(
    model,
    X_test,
    y_test
):

    predictions = model.predict(
        X_test
    )

    mse = mean_squared_error(
        y_test,
        predictions
    )

    rmse = np.sqrt(mse)

    return {

        "mae":
            round(
                float(
                    mean_absolute_error(
                        y_test,
                        predictions
                    )
                ),
                4
            ),

        "mse":
            round(
                float(mse),
                4
            ),

        "rmse":
            round(
                float(rmse),
                4
            ),

        "r2_score":
            round(
                float(
                    r2_score(
                        y_test,
                        predictions
                    )
                ),
                4
            )
    }


def evaluate_models(
    trained_models,
    prepared_data,
    problem_type
):
    """
    Evaluate all successfully trained models.
    """

    results = {}

    for model_name, information in (
        trained_models.items()
    ):

        if not information["success"]:

            results[model_name] = {

                "success": False,

                "error":
                    information["error"]
            }

            continue

        model = information["model"]

        try:

            if (
                problem_type
                == "classification"
            ):

                metrics = (
                    evaluate_classification_model(

                        model,

                        prepared_data["X_test"],

                        prepared_data["y_test"]
                    )
                )

            else:

                metrics = (
                    evaluate_regression_model(

                        model,

                        prepared_data["X_test"],

                        prepared_data["y_test"]
                    )
                )

            results[model_name] = {

                "success": True,

                "metrics": metrics
            }

        except Exception as error:

            results[model_name] = {

                "success": False,

                "error":
                    str(error)
            }

    return results