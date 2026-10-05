import pandas as pd

from .exceptions import (

    UnsupportedMLDataError,

    InvalidTargetError,

    InsufficientTrainingDataError
)

from .target_detector import (
    get_recommended_targets
)

from .problem_detector import (
    detect_problem_type
)

from .data_preprocessor import (
    prepare_ml_data
)

from .model_trainer import (
    train_models
)

from .model_evaluator import (
    evaluate_models
)

from .model_selector import (
    select_best_model
)

from .model_saver import (
    save_model
)


def get_ml_recommendations(
    dataframe
):
    """
    Analyze dataset and recommend
    possible ML targets.
    """

    if not isinstance(
        dataframe,
        pd.DataFrame
    ):

        raise UnsupportedMLDataError(
            "ML Engine supports "
            "Pandas DataFrames only."
        )

    candidates = (
        get_recommended_targets(
            dataframe
        )
    )

    return {

        "success": True,

        "target_candidates":
            candidates
    }


def train_ml_pipeline(

    dataframe,

    target_column,

    save_best_model=True
):
    """
    Complete automated ML pipeline.
    """

    if not isinstance(
        dataframe,
        pd.DataFrame
    ):

        raise UnsupportedMLDataError(
            "ML Engine supports "
            "Pandas DataFrames only."
        )

    if target_column not in dataframe.columns:

        raise InvalidTargetError(
            f"Target column "
            f"'{target_column}' "
            f"does not exist."
        )

    if len(dataframe) < 10:

        raise InsufficientTrainingDataError(
            "At least 10 rows are required "
            "for basic ML training."
        )

    # Detect problem type
    problem_result = (
        detect_problem_type(
            dataframe,
            target_column
        )
    )

    problem_type = (
        problem_result[
            "problem_type"
        ]
    )

    # Prepare data
    prepared_data = (
        prepare_ml_data(
            dataframe,
            target_column
        )
    )

    # Train models
    trained_models = (
        train_models(
            prepared_data,
            problem_type
        )
    )

    # Evaluate models
    evaluation_results = (
        evaluate_models(

            trained_models,

            prepared_data,

            problem_type
        )
    )

    # Select best model
    best_model_result = (
        select_best_model(

            evaluation_results,

            problem_type
        )
    )

    saved_model_path = None

    # Save best model
    if (

        save_best_model

        and

        best_model_result[
            "best_model"
        ]
        is not None
    ):

        best_model_name = (
            best_model_result[
                "best_model"
            ]
        )

        best_model = (
            trained_models[
                best_model_name
            ]["model"]
        )

        saved_model_path = (
            save_model(

                best_model,

                best_model_name
            )
        )

    return {

        "success": True,

        "target_column":
            target_column,

        "problem":
            problem_result,

        "feature_information": {

            "numerical_columns":
                prepared_data[
                    "numerical_columns"
                ],

            "categorical_columns":
                prepared_data[
                    "categorical_columns"
                ]
        },

        "models":
            evaluation_results,

        "best_model":
            best_model_result,

        "saved_model":
            saved_model_path
    }